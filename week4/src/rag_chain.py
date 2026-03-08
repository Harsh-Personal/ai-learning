# src/rag_chain.py
"""
rag_chain.py — Week 4, Wednesday
Shared RAG chain module.
LCEL syntax exclusively (pipe operator |). No deprecated LangChain classes.
LLM: Groq | Vector Store: ChromaDB (in-memory) | Embeddings: HuggingFace
"""
import os
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

# ─── Knowledge base: 8 documents on RAG, LLMs, and evaluation concepts ───────
KNOWLEDGE_BASE = [
    Document(
        page_content=(
            "LangChain Expression Language (LCEL) is a declarative syntax for composing "
            "LangChain components using the pipe operator (|). LCEL supports streaming, "
            "async, and batch processing. It replaces deprecated classes such as "
            "RetrievalQA.from_chain_type and LLMChain. "
            "Example: chain = prompt | llm | StrOutputParser()"
        ),
        metadata={"source": "langchain_docs", "topic": "lcel"},
    ),
    Document(
        page_content=(
            "ChromaDB is an open-source vector database. In a RAG system, documents are "
            "chunked, converted to embeddings, and stored in ChromaDB. At query time the "
            "user question is embedded and the k most similar chunks are retrieved using "
            "cosine similarity. The langchain-chroma package (version 0.2.5) provides the "
            "Chroma class for LangChain integration."
        ),
        metadata={"source": "chromadb_docs", "topic": "vector_store"},
    ),
    Document(
        page_content=(
            "RAG evaluation measures both retrieval quality and generation quality. "
            "Five key metrics are: "
            "(1) Faithfulness — is the answer grounded in the retrieved context with no hallucinations? "
            "(2) Answer Relevancy — is the answer relevant to the user's question? "
            "(3) Contextual Relevancy — are the retrieved chunks relevant to the question? "
            "(4) Contextual Precision — are the most relevant chunks ranked first? "
            "(5) Contextual Recall — does the context contain all info needed to answer?"
        ),
        metadata={"source": "deepeval_docs", "topic": "rag_evaluation"},
    ),
    Document(
        page_content=(
            "HuggingFace embeddings use sentence-transformer models to convert text into "
            "dense vector representations. The model all-MiniLM-L6-v2 is a popular choice "
            "for its balance of speed and quality (384 dimensions). It is available via the "
            "langchain-huggingface package through the HuggingFaceEmbeddings class."
        ),
        metadata={"source": "huggingface_docs", "topic": "embeddings"},
    ),
    Document(
        page_content=(
            "Document chunking splits large texts into smaller pieces before embedding. "
            "Common strategies: fixed-size chunking (e.g. 500 characters), semantic chunking "
            "(split on meaning boundaries), and recursive character splitting. Chunk overlap "
            "(e.g. 50 characters) preserves context at chunk boundaries. Chunk size is a "
            "critical hyperparameter: too large produces noisy context; too small loses context."
        ),
        metadata={"source": "langchain_docs", "topic": "chunking"},
    ),
    Document(
        page_content=(
            "Groq is an AI inference company offering fast LLM API access via Language "
            "Processing Units (LPUs). Its API is OpenAI-compatible and supports models "
            "including LLaMA 3, Mistral, and Gemma. Groq is useful for rapid experimentation "
            "and evaluation pipelines due to low latency. The langchain-groq package provides "
            "the ChatGroq class."
        ),
        metadata={"source": "groq_docs", "topic": "inference"},
    ),
    Document(
        page_content=(
            "Failure modes in RAG systems include: "
            "(1) Retrieval failure — the relevant chunk is not retrieved due to low embedding similarity. "
            "(2) Faithfulness failure — the LLM ignores the context and generates from parametric memory. "
            "(3) Context overflow — too much retrieved context confuses the LLM. "
            "(4) Chunk boundary issues — the answer spans two chunks that are not both retrieved. "
            "(5) Semantic gap — the query uses different vocabulary than the indexed documents."
        ),
        metadata={"source": "rag_research", "topic": "failure_modes"},
    ),
    Document(
        page_content=(
            "G-Eval is a custom LLM-as-a-Judge metric in DeepEval. It uses chain-of-thought "
            "reasoning to evaluate LLM outputs based on custom criteria written in natural "
            "language. G-Eval can measure any quality criterion: correctness, coherence, "
            "technical accuracy. It is available via: from deepeval.metrics import GEval. "
            "It requires LLMTestCaseParams to specify which test case fields are evaluated."
        ),
        metadata={"source": "deepeval_docs", "topic": "geval"},
    ),
]


def build_vectorstore(collection_name: str = "week4_eval") -> Chroma:
    """Build in-memory ChromaDB vectorstore from the knowledge base."""
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    vectorstore = Chroma.from_documents(
        documents=KNOWLEDGE_BASE,
        embedding=embeddings,
        collection_name=collection_name,
    )
    print(f"✅ Vectorstore: {len(KNOWLEDGE_BASE)} docs indexed")
    return vectorstore


def build_rag_chain():
    """
    Build LCEL RAG chain using Groq.
    Returns a chain that expects inputs: {context: str, question: str}
    Call via: chain.invoke({"context": "...", "question": "..."})
    """
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        api_key=os.environ["GROQ_API_KEY"],
    )
    prompt = ChatPromptTemplate.from_template(
        """You are a precise technical assistant.
Answer the question using ONLY the context provided below.
If the context does not contain enough information to answer,
respond with exactly: "I don't know based on the provided context."

Context:
{context}

Question: {question}

Answer:"""
    )
    # Pure LCEL chain — no deprecated wrappers
    chain = prompt | llm | StrOutputParser()
    return chain


def run_rag(chain, retriever, question: str) -> tuple[str, list[str]]:
    """
    Run the RAG chain for one question.
    Returns (answer, retrieval_context_list).
    retrieval_context is a list[str] — exactly what DeepEval expects.
    """
    docs = retriever.invoke(question)
    context_list: list[str] = [doc.page_content for doc in docs]
    context_str = "\n\n".join(context_list)
    answer = chain.invoke({"context": context_str, "question": question})
    return answer, context_list
