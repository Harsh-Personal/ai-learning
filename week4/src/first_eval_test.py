# src/first_eval_test.py
"""
first_eval_test.py — Week 4, Wednesday (Part 2)
First DeepEval integration test on the RAG chain.
Runs AnswerRelevancyMetric + FaithfulnessMetric on 3 test cases.
Prints scores + judge reasoning so you understand what the judge sees.
"""
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from rag_chain import build_vectorstore, build_rag_chain, run_rag

TEST_QUESTIONS = [
    {
        "input": "What is LCEL and why is it preferred over older LangChain syntax?",
        "expected_output": (
            "LCEL uses the pipe operator to compose chains declaratively. "
            "It is preferred because it supports streaming, async, and batch processing "
            "and replaces deprecated classes like RetrievalQA.from_chain_type."
        ),
        "category": "normal — in-scope, factual",
    },
    {
        "input": "What are the five key metrics for evaluating a RAG system?",
        "expected_output": (
            "The five key RAG metrics are: Faithfulness, Answer Relevancy, "
            "Contextual Relevancy, Contextual Precision, and Contextual Recall."
        ),
        "category": "normal — in-scope, list",
    },
    {
        "input": "What is the capital of France?",
        "expected_output": "I don't know based on the provided context.",
        "category": "edge case — out-of-scope question",
    },
]


def run_first_eval():
    vectorstore = build_vectorstore(collection_name="first_eval")
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    chain = build_rag_chain()

    # verbose_mode=True — shows the judge's internal reasoning (valuable for learning)
    answer_relevancy = AnswerRelevancyMetric(threshold=0.5, verbose_mode=True)
    faithfulness = FaithfulnessMetric(threshold=0.5, verbose_mode=True)

    print("\n" + "=" * 65)
    print("WEEK 4 — FIRST EVAL TEST")
    print("=" * 65)

    for i, td in enumerate(TEST_QUESTIONS, 1):
        print(f"\n[Test {i}] Category: {td['category']}")
        print(f"  Q: {td['input']}")

        answer, context_list = run_rag(chain, retriever, td["input"])
        print(f"  → Answer     : {answer[:120]}{'...' if len(answer) > 120 else ''}")
        print(f"  → Ctx chunks : {len(context_list)}")

        test_case = LLMTestCase(
            input=td["input"],
            actual_output=answer,
            expected_output=td["expected_output"],
            retrieval_context=context_list,
        )

        answer_relevancy.measure(test_case)
        faithfulness.measure(test_case)

        ar_icon = "✅" if answer_relevancy.is_successful() else "❌"
        f_icon = "✅" if faithfulness.is_successful() else "❌"
        print(
            f"  {ar_icon} AnswerRelevancy : {answer_relevancy.score:.3f} | {answer_relevancy.reason[:100]}"
        )
        print(
            f"  {f_icon} Faithfulness    : {faithfulness.score:.3f} | {faithfulness.reason[:100]}"
        )

    print(
        "\n✅ First eval complete. Check verbose_mode output above for judge reasoning."
    )


if __name__ == "__main__":
    run_first_eval()
