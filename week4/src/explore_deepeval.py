# src/explore_deepeval.py
"""
explore_deepeval.py — Week 4, Tuesday
Sanity check: run DeepEval metrics on hardcoded strings (no RAG chain).
Goal: understand what LLM-as-a-judge output looks like before connecting to RAG.
Requires: OPENAI_API_KEY set in environment (DeepEval judge)
"""

from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, GEval


def demo_answer_relevancy():
    """Test: Is the answer relevant to the question?"""
    print("\n--- Demo 1: AnswerRelevancyMetric ---")
    test_case = LLMTestCase(
        input="What is LangChain LCEL?",
        actual_output=(
            "LangChain Expression Language (LCEL) is a declarative syntax for composing "
            "chains using the pipe operator. It supports streaming and async by default."
        ),
    )
    metric = AnswerRelevancyMetric(threshold=0.5, verbose_mode=True)
    metric.measure(test_case)
    print(f"Score  : {metric.score:.3f}")
    print(f"Pass   : {metric.is_successful()}")
    print(f"Reason : {metric.reason}")


def demo_faithfulness():
    """Test: Is the answer grounded in the context (no hallucinations)?"""
    print("\n--- Demo 2: FaithfulnessMetric ---")

    # Case A: Faithful answer (all claims traceable to context)
    test_case_faithful = LLMTestCase(
        input="What does ChromaDB do?",
        actual_output="ChromaDB is a vector database that stores document embeddings.",
        retrieval_context=[
            "ChromaDB is an open-source vector database. It stores document embeddings "
            "and enables semantic similarity search using cosine distance."
        ],
    )
    metric_a = FaithfulnessMetric(threshold=0.5, verbose_mode=False)
    metric_a.measure(test_case_faithful)
    print(
        f"[Faithful Case]   Score={metric_a.score:.3f} | Pass={metric_a.is_successful()} | {metric_a.reason[:100]}"
    )

    # Case B: Hallucinated answer (claim NOT in the context)
    test_case_hallucinated = LLMTestCase(
        input="What does ChromaDB do?",
        actual_output=(
            "ChromaDB is a vector database created by Google in 2022 "
            "that uses GPU acceleration for embeddings."
        ),
        retrieval_context=[
            "ChromaDB is an open-source vector database. It stores document embeddings "
            "and enables semantic similarity search using cosine distance."
        ],
    )
    metric_b = FaithfulnessMetric(threshold=0.5, verbose_mode=False)
    metric_b.measure(test_case_hallucinated)
    print(
        f"[Hallucinated]    Score={metric_b.score:.3f} | Pass={metric_b.is_successful()} | {metric_b.reason[:100]}"
    )


def demo_geval():
    """Test: G-Eval with a custom criterion."""
    print("\n--- Demo 3: G-Eval Custom Metric (Conciseness) ---")
    test_case = LLMTestCase(
        input="What is RAG?",
        actual_output=(
            "RAG stands for Retrieval-Augmented Generation. It combines a retrieval step "
            "(finding relevant documents) with generation (using an LLM to produce an answer "
            "grounded in those documents). This reduces hallucinations."
        ),
    )
    conciseness = GEval(
        name="Conciseness",
        criteria=(
            "Evaluate whether the actual output directly answers the input without "
            "unnecessary verbosity or padding. A concise answer gets to the point."
        ),
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        threshold=0.5,
    )
    conciseness.measure(test_case)
    print(f"Score  : {conciseness.score:.3f}")
    print(f"Pass   : {conciseness.is_successful()}")
    print(f"Reason : {conciseness.reason}")


if __name__ == "__main__":
    demo_answer_relevancy()
    demo_faithfulness()
    demo_geval()
    print("\n✅ DeepEval environment confirmed working.")
