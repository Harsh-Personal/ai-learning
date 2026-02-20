# Vector DB Experiment Results

## Query Results

### Query 1: "Tell me about France"

| Rank | Document                            | Distance |
| ---- | ----------------------------------- | -------- |
| 1    | The capital of France is Paris      | 0.7379   |
| 2    | Paris is known for the Eiffel Tower | 1.1394   |
| 3    | The Eiffel Tower is 330 meters tall | 1.5921   |

### Query 2: "Which languages are for coding?"

| Rank | Document                               | Distance |
| ---- | -------------------------------------- | -------- |
| 1    | Python is a programming language       | 0.9281   |
| 2    | JavaScript is used for web development | 1.1256   |
| 3    | TypeScript is a superset of JavaScript | 1.5770   |

### Query 3: "France" — geography category only (metadata filter)

| Rank | Document                            | Distance |
| ---- | ----------------------------------- | -------- |
| 1    | The capital of France is Paris      | 1.7554   |
| 2    | Paris is known for the Eiffel Tower | 1.7554   |
| 3    | The Eiffel Tower is 330 meters tall | 1.7554   |

### Query 4: "What is the weather in Tokyo?" (not in database)

| Rank | Document                               | Distance |
| ---- | -------------------------------------- | -------- |
| 1    | TypeScript is a superset of JavaScript | 1.7355   |
| 2    | The Eiffel Tower is 330 meters tall    | 1.7578   |

### Query 5: "Explain deep learning"

| Rank | Document                                      | Distance |
| ---- | --------------------------------------------- | -------- |
| 1    | Deep learning is a subset of machine learning | 0.6801   |
| 2    | Machine learning uses data to train models    | 1.0654   |
| 3    | Python is a programming language              | 1.6769   |

---

## What Worked Well

It is almost 99% correct when the data exists in the database. For queries that match, the ranking makes intuitive sense — more relevant sentences have lower distances.

- **"Tell me about France"** → returned capital, Paris, Eiffel Tower
- **"Which languages are for coding?"** → returned Python, JavaScript, TypeScript

This shows the vector DB performs true **semantic search** — it understands that "languages for coding" maps to Python/JavaScript/TypeScript, and that "France" relates to Paris and the Eiffel Tower, even without keyword overlap.

---

## The Limitation I Discovered

When relevant data is not in the database, the DB still returns _something_ (always returns the closest vectors). The only signal that nothing matches well is the **high distance value**.

> I noticed Query 3 results had a much higher distance than Queries 1 and 2, even though the same documents were returned. The `where={"category": "geography"}` filter restricts the search space, so the model ranks within that subset — that's why the distances are higher (less freedom to find the best semantic match).

**The core RAG limitation:** if these irrelevant chunks are passed to an LLM without checks, it may generate a confident but wrong answer (hallucination).

Production systems must add:

- Distance/similarity **thresholds** to reject low-confidence results
- **Metadata filters** to restrict the search space
- **LLM instructions** like "say I don't know if context is missing"

---

## Why Metadata Filtering Matters

**My observation:** LLMs predict the next best word and queries are rarely exact — similarity is what matters. But with metadata, retrieval becomes even more targeted. For example, a query about deep learning could filter by `category="AI"` even if the word "deep learning" isn't in the document explicitly. For fast, large-scale search this is very powerful.

**Why it matters:**

- Embeddings are great for **semantic similarity** (France → Paris, Eiffel Tower)
- But sometimes we need **hard constraints**:
  - Only a certain domain (geography, AI, medicine)
  - Only certain customers, projects, or document types
  - Only current version, not archived data

Metadata lets you **combine** two strategies:

1. **Metadata filter** — hard constraint that narrows the search space
2. **Embeddings** — semantic ranking within that narrowed subset

**Example:** Query "deep learning" with `where={"category": "AI"}` — even if the text doesn't literally say "deep learning", docs tagged `category="AI"` become the candidates. This makes retrieval both **faster** (smaller search space) and **more accurate** (no irrelevant categories).
