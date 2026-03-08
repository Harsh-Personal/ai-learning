## Critical Finding: AnswerRelevancy Fails on Correct Refusals

Test case: "What is the capital of France?"
RAG answer: "I don't know based on the provided context."
AnswerRelevancy: 0.0 ← MISLEADING
Faithfulness: 1.0 ← TECHNICALLY CORRECT BUT UNINFORMATIVE

Root cause:
AnswerRelevancyMetric measures: "Does answer address the question?"
It cannot distinguish:

- BAD: wrong/hallucinated answer (0.0 — genuinely bad)
- GOOD: correct refusal (0.0 — falsely penalized)

Fix: Add RefusalQuality G-Eval metric for out-of-scope test cases

## Metric Selection Rule (learned from Test 3):

Always match metric to question TYPE:
| Question Type | Right Metrics |
|-------------------|--------------------------------------------|
| In-scope factual | AnswerRelevancy + Faithfulness + CtxRecall |
| Out-of-scope | RefusalQuality (custom G-Eval) |
| Comparison | AnswerRelevancy + TechnicalAccuracy |
| Adversarial | RefusalQuality + Faithfulness |

Using AnswerRelevancy on out-of-scope questions = measuring
the wrong thing. Garbage in → garbage signal out.
