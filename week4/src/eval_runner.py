from deepeval.test_case import LLMTestCase
from metrics import category_metrics
from test_cases import TEST_CASES
from rag_loader import load_rag, build_rag_chain, run_rag
import os
import csv


def build_test_case(
    question: str,
    actual_output: str,
    expected_output: str,
    retrieval_context: list[str],
) -> LLMTestCase:
    return LLMTestCase(
        input=question,
        actual_output=actual_output,
        expected_output=expected_output,
        retrieval_context=retrieval_context,
    )


def run_eval():
    print("\n" + "=" * 65)
    print("WEEK 4 — EVAL RESULTS")
    print("=" * 65)

    retriever, llm = load_rag()
    chain = build_rag_chain(llm)

    results = []

    for i, td in enumerate(TEST_CASES, 1):
        print(f"\n[Test {i}] ID: {td['id']} | Category: {td['category']}")
        print(f"  Q: {td['question']}")

        actual_output, retrieval_context = run_rag(chain, retriever, td["question"])
        print(
            f"  → Answer     : {actual_output[:120]}{'...' if len(actual_output) > 120 else ''}"
        )
        print(f"  → Ctx chunks : {len(retrieval_context)}")

        test_case = build_test_case(
            question=td["question"],
            actual_output=actual_output,
            expected_output=td["expected_output"],
            retrieval_context=retrieval_context,
        )

        metrics = category_metrics.get(td["category"], [])

        row = {
            "id": td["id"],
            "category": td["category"],
            "question": td["question"],
            "actual_output": actual_output,
            "expected_output": td["expected_output"],
            "retrieval_context": " ||| ".join(retrieval_context),  # readable separator
        }

        # Add one column per metric — score AND pass separately:
        metric_passed = []
        for metric in metrics:
            col = (
                metric.name
                if hasattr(metric, "name") and metric.name
                else metric.__class__.__name__
            )
            try:
                metric.measure(test_case)
                icon = "✅" if metric.is_successful() else "❌"
                reason = metric.reason or "No reason provided"
                print(f"  {icon} {col:<30} : {metric.score:.3f} | {reason[:80]}")
                row[f"{col}_score"] = round(metric.score, 3)
                row[f"{col}_pass"] = metric.is_successful()
                metric_passed.append(metric.is_successful())
            except Exception as e:
                print(f"  ⚠️  {col:<30} : ERROR — {str(e)[:80]}")
                row[f"{col}_score"] = "ERROR"
                row[f"{col}_pass"] = False
                metric_passed.append(False)

        row["overall_pass"] = all(metric_passed)
        results.append(row)

    os.makedirs("results", exist_ok=True)
    if results:
        all_fields = list(dict.fromkeys(key for row in results for key in row.keys()))

        with open("results/eval_results.csv", "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=all_fields,
                extrasaction="ignore",
                restval="",  # empty string for missing metric columns
            )
            writer.writeheader()
            writer.writerows(results)
        print("\n✅ Eval complete. Results saved to results/eval_results.csv")
    else:
        print("\n⚠️  No results to save.")
        return

    total = len(results)
    passed = sum(1 for r in results if r["overall_pass"])
    print(f"\n{'='*65}")
    print(f"SUMMARY: {passed}/{total} passed ({passed/total*100:.0f}%)")
    print(f"{'='*65}")

    by_category = {}
    for r in results:
        cat = r["category"]
        by_category.setdefault(cat, {"pass": 0, "total": 0})
        by_category[cat]["total"] += 1
        if r["overall_pass"]:
            by_category[cat]["pass"] += 1

    for cat, counts in by_category.items():
        icon = "✅" if counts["pass"] == counts["total"] else "⚠️ "
        print(f"  {icon} {cat:<25} {counts['pass']}/{counts['total']}")


if __name__ == "__main__":
    run_eval()
