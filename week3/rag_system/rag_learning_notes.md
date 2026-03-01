# RAG System - Week 3 Notes

## Pipeline Summary:

PDF → PyPDFLoader → RecursiveCharacterTextSplitter →
HuggingFaceEmbeddings → ChromaDB → Retriever →
ChatPromptTemplate → ChatGroq → StrOutputParser

## Results:

============================================================
STEP 1: Loading PDF
============================================================
✅ Loaded 21 pages | 109,934 characters

============================================================
STEP 2: Chunking Documents
============================================================
✅ Created 129 chunks | avg 908 chars each

First chunk preview:
1
Retrieval-Augmented Generation for Large
Language Models: A Survey
Yunfan Gaoa, Yun Xiong b, Xinyu Gao b, Kangxiang Jia b, Jinliu Pan b, Yuxi Bi c, Yi Dai a, Jiawei Sun a, Meng
Wangc, and Haofen Wan

============================================================
STEP 3: Loading Embedding Model
============================================================
✅ Embedding model loaded (384 dimensions)
✅ Test embedding: 384 dimensions confirmed

============================================================
STEP 4: Building ChromaDB Vector Store
============================================================
(First run takes 2-3 min — embedding all chunks locally)
✅ Vector store created with 129 chunks
✅ Saved to ./chroma_db (persists between runs)

============================================================
STEP 5: Setting Up Retriever
============================================================
✅ Retriever test: 'What is Naive RAG?'
Retrieved 3 chunks:

Chunk 1 (page 1):
RAG, and Modular RAG, as showed in Figure 3. Despite
RAG method are cost-effective and surpass the performance
of the native LLM, they also exhibit se...

Chunk 2 (page 1):
on RAG’s downstream tasks and evaluation system. Sec-
tion VII mainly discusses the challenges that RAG currently
faces and its future development dir...

Chunk 3 (page 0):
leading to rapid development in RAG studies. As research
progressed, the enhancement of RAG was no longer limited
to the inference stage but began to ...

============================================================
STEP 6: Connecting to Groq LLM
============================================================
✅ Groq LLM connected (llama-3.1-8b-instant)

============================================================
STEP 7: Building RAG Chain (LCEL)
============================================================
✅ RAG chain built (LCEL pipeline)
Flow: Question → Retriever → Prompt → LLM → Answer

============================================================
STEP 8: Testing RAG System
============================================================

============================================================
❓ QUESTION: What is Naive RAG?
============================================================

✅ ANSWER:
The Naive RAG research paradigm represents the earliest methodology in the RAG development process, which gained prominence shortly after the initial introduction of RAG.

📚 SOURCES USED (3 chunks):

Source 1 (Page 1):
RAG, and Modular RAG, as showed in Figure 3. Despite
RAG method are cost-effective and surpass the performance
of the native LLM, they also exhibit several limitations.
The development of Advanced RAG...

Source 2 (Page 1):
on RAG’s downstream tasks and evaluation system. Sec-
tion VII mainly discusses the challenges that RAG currently
faces and its future development directions. At last, the paper
concludes in Section V...

Source 3 (Page 0):
leading to rapid development in RAG studies. As research
progressed, the enhancement of RAG was no longer limited
to the inference stage but began to incorporate more with LLM
fine-tuning techniques.
...

============================================================
❓ QUESTION: What are the main challenges in RAG systems?
============================================================

✅ ANSWER:
I don't have enough information in the provided context to answer this. The context mentions that "several challenges persist that warrant in-depth research" in the RAG technology, but it does not explicitly state what those challenges are. However, it does mention that the chapter will introduce the current challenges and future research directions faced by RAG in the section "VII. DISCUSSION AND FUTURE PROSPECTS."

📚 SOURCES USED (3 chunks):

Source 1 (Page 0):
leading to rapid development in RAG studies. As research
progressed, the enhancement of RAG was no longer limited
to the inference stage but began to incorporate more with LLM
fine-tuning techniques.
...

Source 2 (Page 1):
RAG, and Modular RAG, as showed in Figure 3. Despite
RAG method are cost-effective and surpass the performance
of the native LLM, they also exhibit several limitations.
The development of Advanced RAG...

Source 3 (Page 13):
quantitative metrics that not only gauge RAG model perfor-
mance but also enhance comprehension of the model’s capabil-
ities across various evaluation aspects. Prominent benchmarks
such as RGB, RECAL...

============================================================
❓ QUESTION: How does Advanced RAG differ from Naive RAG?
============================================================

✅ ANSWER:
According to the provided context, the development of Advanced RAG is a response to the specific shortcomings in Naive RAG. However, the exact differences between Advanced RAG and Naive RAG are not explicitly stated in the given text.

It is mentioned that Naive RAG exhibits several limitations, and Advanced RAG is a response to these shortcomings. But the specific limitations and how Advanced RAG addresses them are not detailed in the provided context.

Therefore, I don't have enough information in the provided context to answer this question in detail.

📚 SOURCES USED (3 chunks):

Source 1 (Page 1):
RAG, and Modular RAG, as showed in Figure 3. Despite
RAG method are cost-effective and surpass the performance
of the native LLM, they also exhibit several limitations.
The development of Advanced RAG...

Source 2 (Page 0):
leading to rapid development in RAG studies. As research
progressed, the enhancement of RAG was no longer limited
to the inference stage but began to incorporate more with LLM
fine-tuning techniques.
...

Source 3 (Page 0):
hensively reviews the downstream tasks, datasets, benchmarks,
and evaluation methods applicable to RAG. Overall, this
paper sets out to meticulously compile and categorize the
foundational technical c...

============================================================
❓ QUESTION: What evaluation metrics are used for RAG?
============================================================

✅ ANSWER:
According to the provided context, the evaluation metrics used for RAG are summarized in Table III. These metrics include:

1. Accuracy
2. EM (Exact Match)
3. Recall
4. Precision
5. R-Rate
6. Cosine Similarity
7. Hit Rate
8. MRR (Mean Reciprocal Rank)
9. NDCG (Normalized Discounted Cumulative Gain)
10. BLEU
11. ROUGE/ROUGE-L

📚 SOURCES USED (3 chunks):

Source 1 (Page 11):
The main downstream tasks of RAG and their corresponding
datasets are summarized in Table II.
B. Evaluation Target
Historically, RAG models assessments have centered on
their execution in specific dow...

Source 2 (Page 13):
14
TABLE III
SUMMARY OF METRICS APPLICABLE FOR EVALUATION ASPECTS OF RAG
Context
Relevance Faithfulness Answer
Relevance
Noise
Robustness
Negative
Rejection
Information
Integration
Counterfactual
Robu...

Source 3 (Page 13):
quantitative metrics that not only gauge RAG model perfor-
mance but also enhance comprehension of the model’s capabil-
ities across various evaluation aspects. Prominent benchmarks
such as RGB, RECAL...

============================================================
STEP 9: Testing Limitations
============================================================

--- Questions NOT in the document ---

❓ What is the weather in Tokyo?
✅ I don't have enough information in the provided context to answer this. The context appears to be about a document discussing a model optimization method called RAG (Rapid Ascent Generator) and its applications in question-answering tasks, but it does not contain any information about the weather in Tokyo.
← Did it admit it doesn't know, or hallucinate? Yes

❓ What is the price of Pinecone in 2026?
✅ I don't have enough information in the provided context to answer this.
← Did it admit it doesn't know, or hallucinate? Yes

❓ Who won IPL 2025?
✅ I don't have enough information in the provided context to answer this.
← Did it admit it doesn't know, or hallucinate? Yes

### Questions FROM document:

- "What is Naive RAG?" → mentioned in results
- "What are main challenges?" → mentioned in results
- "Naive vs Advanced RAG?" → mentioned in results

### Questions NOT in document:

- "Weather in Tokyo?" → [did it say I don't know?] - Yes
- "IPL 2025?" → [hallucinated or admitted?] - Admitted

## Key observations:

1. [What worked well?] Question 1 and 4 answer and not hallucinating for questions it didn't have any answer about
2. [What surprised you?] Not getting better answers for 2 and 3 inspite of being in the documents
3. [Any hallucinations?] No
4. [Which chunk source was most retrieved?] The once which are the top of string matching basically if it found something related in page 1-2 it won't go deeper it just retrieved the closest from first pages

## What LCEL chain means:

LCEL - is basically the process from asking questions to get answer from LLM
If we have a document first we create chunks, and store in vectordb along with embeddings
First the question is sent to retriever which will try to get top matching chunks we mentioned with top_k from the vectors we have stored in db. Then these retrieved chunks along with question will be sent to llm as context and question to provide an answer along with the prompt settings
Pipe operator basically runs 2 processes in parallel from the chunks received it tries to format them and create a single string to work as context
[Explain in your words what the | pipe operator does]
