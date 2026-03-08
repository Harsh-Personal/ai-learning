from deepeval.metrics import AnswerRelevancyMetric
from deepeval.metrics import FaithfulnessMetric
from deepeval.metrics import ContextualRelevancyMetric
from deepeval.metrics import ContextualPrecisionMetric
from deepeval.metrics import ContextualRecallMetric
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams


answer_relevancy = AnswerRelevancyMetric(threshold=0.7)
faithfulness = FaithfulnessMetric(threshold=0.7)
contextual_relevancy = ContextualRelevancyMetric(threshold=0.7)
contextual_precision = ContextualPrecisionMetric(threshold=0.7)
contextual_recall = ContextualRecallMetric(threshold=0.7)
refusal_quality = GEval(
    name="RefusalQuality",
    criteria=(
        "Evaluate whether the system responded appropriately given the retrieval context "
        "If the question cannot be answered from the context, a clear refusal should score high. "
        "If the question can be answered but the system refused, score low. "
        "If the system answered despite the question being unanswerable, score low. "
    ),
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
        LLMTestCaseParams.RETRIEVAL_CONTEXT,
    ],
    threshold=0.7,
)
technical_accuracy = GEval(
    name="TechnicalAccuracy",
    criteria=(
        "Evaluate whether the actual output correctly handles the question. "
        "For counterintuitive questions, check if the answer uses the retrieval context rather than prior assumptions. "
        "For factual questions, check if specific values and numbers match the expected output exactly. "
    ),
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
        LLMTestCaseParams.EXPECTED_OUTPUT,
        LLMTestCaseParams.RETRIEVAL_CONTEXT,
    ],
    threshold=0.7,
)

category_metrics = {
    "vague": [answer_relevancy, faithfulness],
    "buried_content": [answer_relevancy, faithfulness, contextual_recall],
    "trick": [answer_relevancy, faithfulness, technical_accuracy],
    "prompt_injection": [answer_relevancy, faithfulness, refusal_quality],
    "out_of_scope": [refusal_quality, faithfulness],
    "multi_part": [
        answer_relevancy,
        faithfulness,
        contextual_precision,
        contextual_recall,
    ],
    "exact_facts": [answer_relevancy, faithfulness, technical_accuracy],
}
