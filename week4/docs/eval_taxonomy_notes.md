# Eval Taxonomy Notes — Week 4 Monday

## Eval Types

- Unit eval: test one component (e.g., retriever only)
- System eval: test end-to-end (input → answer)
- Reference-based: needs expected_output (ground truth)
- Referenceless: no gold answer needed — better for production monitoring

## Why BLEU/ROUGE fail for LLMs

BLEU and ROUGE fail for LLMs because they rely on exact lexical overlap and n-gram matching, which do not capture semantic meaning, paraphrasing, or contextual understanding.

BLUE penalizes rewording, synonym use, or different sentence structures—even if the meaning is identical—leading to misleadingly low scores for valid paraphrases.

ROUGE fails to recognize semantic equivalence and can reward verbose or repetitive outputs that include reference phrases, even if the rest is nonsensical or hallucinated.

BLEU/ROUGE assume ONE correct answer exists
LLM outputs can be correct in many ways:

- "Paris is the capital of France"
- "France's capital city is Paris"
- "The French capital is Paris"

BLEU scores all three differently against each other.
LLM-as-a-judge scores them all as equally correct.

## The 5 RAG Metrics

| Metric               | Measures                      | Component | Needs Ground Truth? |
| -------------------- | ----------------------------- | --------- | ------------------- |
| Faithfulness         | No hallucinations             | Generator | No                  |
| Answer Relevancy     | Answer addresses question     | Generator | No                  |
| Contextual Relevancy | Retrieved chunks are on-topic | Retriever | No                  |
| Contextual Precision | Relevant chunks ranked first  | Retriever | Yes                 |
| Contextual Recall    | Context has all needed info   | Retriever | Yes                 |

## My questions / unclear areas

How do we know when it is good to have custom inputs how do I know if any type of metric is missing which we should have and how to link test cases to evals not sure what is the difference. Is a test case just data and evaluation is the assertion? and how to know if we have good coverage of test cases

Q1: "Is a test case just data and evaluation is the assertion?"
Software Testing You Know:
─────────────────────────────────────────────
Test Case = input data + expected output
Assertion = assert actual_output == expected_output

LLM Evaluation Equivalent:
─────────────────────────────────────────────
LLMTestCase = input + actual_output + expected_output + context
Metric = the "assertion" — but fuzzy, not binary

# Traditional SDET:

assert response.status_code == 200 ← binary ✅/❌

# LLM Evaluation:

FaithfulnessMetric.measure(test_case) ← score 0.0 to 1.0
metric.is_successful() ← threshold-based ✅/❌

Q2:How do I know if a metric is missing?
Ask yourself:
─────────────────────────────────────────────────────────

1. Can the answer be on-topic but fabricated?
   → If yes: add FaithfulnessMetric

2. Can the answer be faithful but not address the question?
   → If yes: add AnswerRelevancyMetric

3. Can the retriever return garbage chunks?
   → If yes: add ContextualRelevancyMetric

4. Are some chunks more important than others?
   → If yes: add ContextualPrecisionMetric

5. Could key info be missing from retrieved chunks?
   → If yes: add ContextualRecallMetric

6. Do you have domain-specific rules not captured above?
   → If yes: add G-Eval with custom criteria

refusal_quality = GEval(
name="RefusalQuality",
criteria=(
"If the question cannot be answered from the context, "
"the answer should clearly say so without guessing. "
"Penalize answers that attempt to answer out-of-scope questions."
),
evaluation_params=[
LLMTestCaseParams.INPUT,
LLMTestCaseParams.ACTUAL_OUTPUT,
LLMTestCaseParams.RETRIEVAL_CONTEXT,
],
threshold=0.7,
)

Q3: How to link test cases to evals?

# Step 1: Test case = DATA CONTAINER

test_case = LLMTestCase(
input="What is Naive RAG?", # ← question asked
actual_output="Naive RAG is the earliest...", # ← what RAG answered
expected_output="Naive RAG is the first...", # ← ground truth
retrieval_context=["chunk1...", "chunk2..."], # ← what retriever found
)

# Step 2: Metric = ASSERTION ENGINE

metric = FaithfulnessMetric(threshold=0.7)
metric.measure(test_case) # ← runs the judge LLM

# Step 3: Result = VERDICT

print(metric.score) # 0.0 to 1.0
print(metric.is_successful()) # True/False (threshold applied)
print(metric.reason) # Why the judge gave this score

# Exact SDET parallel:

# test_case = test data

# metric = assertion

# .measure() = test execution

# .score = actual result

# .is_successful() = pass/fail

Q4: How to know if we have good coverage of test cases?

## Coverage Checklist

### Input Type Coverage:

- [ ] Simple factual question ("What is X?")
- [ ] Comparison question ("How does X differ from Y?")
- [ ] Multi-hop question ("What connects X to Z via Y?")
- [ ] Out-of-scope question (not in document)
- [ ] Adversarial question (injection, trick, vague)

### Failure Mode Coverage (from YOUR Break Your RAG!):

- [ ] Buried content (deep in document)
- [ ] Vague query (no entity specified)
- [ ] Prompt injection
- [ ] Multi-part question
- [ ] Exact fact question

### Answer Quality Coverage:

- [ ] At least 1 question with perfect expected answer
- [ ] At least 1 question where answer should be "I don't know"
- [ ] At least 1 multi-sentence expected answer
- [ ] At least 1 question where retrieval should fail

For a 10-question dataset:

- 4 normal in-scope factual
- 2 reasoning/comparison
- 2 out-of-scope (should refuse)
- 2 edge cases (adversarial/tricky)

= basic coverage across all failure modes

## Test Case vs Metric (SDET Mapping)

| SDET Concept | LLM Eval Equivalent               |
| ------------ | --------------------------------- |
| Test data    | LLMTestCase                       |
| Assertion    | Metric (FaithfulnessMetric, etc.) |
| assert ==    | metric.is_successful()            |
| Test result  | metric.score (0.0–1.0)            |
| Test reason  | metric.reason (judge explanation) |
| Test suite   | evaluate([test_cases], [metrics]) |

Key difference: LLM assertions are probabilistic (scored),
not binary (pass/fail), because correct answers have many valid forms.

## When to add a custom G-Eval metric:

1. You found a failure mode not covered by 5 standard metrics
2. You have domain-specific rules (safety, compliance, tone)
3. You need to evaluate refusal behavior specifically
4. Standard metrics score something as passing that clearly shouldn't

## Coverage rule of thumb:

- Normal in-scope: 40% of dataset
- Reasoning/comparison: 20%
- Out-of-scope (refusals): 20%
- Adversarial/edge cases: 20%
