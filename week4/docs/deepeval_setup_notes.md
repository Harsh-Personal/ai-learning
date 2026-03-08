# DeepEval Setup Notes — Week 4 Tuesday

## What LLM-as-a-Judge means

DeepEval sends your `actual_output` + `retrieval_context` to an OpenAI model,
which then scores the output based on the metric's criteria.

## Key observations from explore_deepeval.py

- Faithful vs hallucinated: scores were 1.0 vs 0.0
- G-Eval reason: The response directly answers the question by defining RAG as Retrieval-Augmented Generation, briefly explaining its two main components (retrieval and generation), and mentioning its purpose (reducing hallucinations). The explanation is concise, focused, and avoids unnecessary details, fully aligning with the evaluation steps.
- Surprising findings: Perfect score

## Metric parameters cheatsheet

| Metric                    | Required LLMTestCase fields                              |
| ------------------------- | -------------------------------------------------------- |
| AnswerRelevancyMetric     | input, actual_output                                     |
| FaithfulnessMetric        | input, actual_output, retrieval_context                  |
| ContextualRelevancyMetric | input, actual_output, retrieval_context                  |
| ContextualPrecisionMetric | input, actual_output, expected_output, retrieval_context |
| ContextualRecallMetric    | input, actual_output, expected_output, retrieval_context |
| GEval                     | depends on evaluation_params you define                  |

Insights:
The judge didn't score the answer as a whole.
It broke the answer into STATEMENTS first, then scored each one.

Statement 1: "LCEL is a declarative syntax for composing chains"
→ Verdict: YES (directly answers the question)

Statement 2: "LCEL supports streaming by default"
→ Verdict: IDK (feature, not core definition)

Statement 3: "LCEL supports async by default"
→ Verdict: IDK (same — supporting info, not direct answer)

Final score = relevant statements ÷ total statements:

2 YES + 1 IDK → still scored 1.0 because IDK ≠ irrelevant
Only "NO" verdicts would lower the score

This is why: score = 1.0 doesn't mean "every sentence was perfect"
It means: "no irrelevant or harmful statements found"

Output:
--- Demo 1: AnswerRelevancyMetric ---

---

Answer Relevancy Verbose Logs

---

Statements:
[
"LangChain Expression Language (LCEL) is a declarative syntax for composing chains using the pipe operator.",
"LCEL supports streaming by default.",
"LCEL supports async by default."
]

Verdicts:
[
{
"verdict": "yes",
"reason": null
},
{
"verdict": "idk",
"reason": "While this provides a feature of LCEL, it is not a direct definition or explanation of what
LCEL is, but could be considered supporting information."
},
{
"verdict": "idk",
"reason": "This statement describes a feature of LCEL rather than directly answering what LCEL is, so it
is supporting information."
}
]

Score: 1.0
Reason: Great job! The answer is fully relevant and directly addresses the question about LangChain LCEL with no
irrelevant information.

======================================================================
Score : 1.000
Pass : True
Reason : Great job! The answer is fully relevant and directly addresses the question about LangChain LCEL with no irrelevant information.

--- Demo 2: FaithfulnessMetric ---
[Faithful Case] Score=1.000 | Pass=True | The score is 1.00 because there are no contradictions—great job staying true to the retrieval contex
[Hallucinated] Score=0.000 | Pass=False | The score is 0.00 because the actual output claims that ChromaDB was created by Google in 2022 and u

--- Demo 3: G-Eval Custom Metric (Conciseness) ---
Score : 1.000
Pass : True
Reason : The response directly answers the question by defining RAG as Retrieval-Augmented Generation, briefly explaining its two main components (retrieval and generation), and mentioning its purpose (reducing hallucinations). The explanation is concise, focused, and avoids unnecessary details, fully aligning with the evaluation steps.

✅ DeepEval environment confirmed working.
