from deepeval.test_case import LLMTestCase


def build_test_case(
    question: str, actual_output: str, retrieval_context: list[str]
) -> LLMTestCase:
    return LLMTestCase(
        input=question,
        actual_output=actual_output,
        expected_output=expected_output,
        retrieval_context=retrieval_context,
    )
