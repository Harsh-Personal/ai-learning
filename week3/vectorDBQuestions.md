# Vector Database Questions

## 1. Why can't we just use PostgreSQL or MongoDB for embeddings?

**My Answer:** They are not designed to handle vectors and query vectors — they were designed to query rows based on string, text, etc. but not vectors. Vectors are arrays of numbers and querying them is not the same as querying traditional databases. We needed efficient databases designed to deal with vectors, and querying them doesn't require more storage.

**Full Answer:**

Traditional databases (PostgreSQL, MongoDB) are optimized for exact matches and simple comparisons on structured data (numbers, strings, dates). They can store vectors as arrays, but they are not efficient at:

- Computing cosine similarity or vector distance over millions of rows
- Doing nearest-neighbor search in high-dimensional space (384, 768, 1536 dims)

A vector DB is built specifically for:

- Fast similarity search over large collections of embeddings
- Specialized indexes (HNSW, IVF, etc.) for high-dimensional vectors
- Scale: millions to billions of vectors with low latency

You can hack embeddings into Postgres (with extensions), but performance and features are usually worse than a dedicated vector database.

---

## 2. What is "Approximate Nearest Neighbors" (ANN)?

**My Answer:** ANN is an algorithm used in vector databases to search for vector embeddings. These algorithms are assembled into a pipeline that provides fast and accurate retrieval of the neighbors of a queried vector. The vector database compares the indexed query vector to the indexed vectors in the dataset to find the nearest neighbors (applying a similarity metric used by that index).

**Full Answer:**

ANN = Approximate Nearest Neighbors. It's a family of algorithms that finds vectors that are _close enough_ to the query vector without exhaustively comparing against every single vector.

**Why "approximate"?**

- Exact search = compare query with all N vectors → too slow for millions of vectors
- ANN builds special indexes and data structures so we only compare with a small subset

**Trade-off:**

- You sacrifice perfect accuracy (might miss the mathematically closest vector)
- In exchange for huge speed gains (ms instead of seconds)

Vector DBs (Chroma, Pinecone, Weaviate) use ANN under the hood to make semantic search fast on large datasets.

---

## 3. What is an "index" in vector databases?

**My Answer:** Not sure entirely, but a wild guess — like we have indexes in a vector embedding to match and can use to compare with other vectors. Similarly, entire sentences, words, etc. can be added to a database and can be indexed, then queried for easy identification.

**Full Answer:**

An index in a vector database is a data structure that organizes embeddings so that nearest-neighbor search becomes fast.

---

## 4. When would you choose ChromaDB vs Pinecone vs Weaviate?

**My Answer:** Not read about it in the material yet. Pinecone provides both local and cloud database — that I know.

**Full Answer:**

|                | ChromaDB                                                                                                          | Pinecone                                                                                                                                                    | Weaviate                                                                                                                |
| -------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **Best for**   | Local development, prototypes, small-medium projects                                                              | Managed, production-grade vector search in the cloud                                                                                                        | Hybrid search + more complex data models                                                                                |
| **Features**   | Pure Python, easy to run locally; no external service needed; great for notebooks, experiments, personal projects | Fully managed SaaS (scaling, replication, backups handled for you); very good performance and reliability at large scale; strong ecosystem and integrations | Can run self-hosted or managed; supports hybrid search (BM25 + vector) and rich schemas; strong community, GraphQL/REST |
| **Trade-offs** | Less ideal for large, multi-region production at huge scale                                                       | Ongoing cost, tied to their cloud service                                                                                                                   | More to learn (schema, modules, deployment)                                                                             |

**Simple rule of thumb:**

- Learning, local RAG, hobby/project → **ChromaDB**
- Startup / production SaaS, want "just works" cloud service → **Pinecone**
- More control, richer search features, maybe self-hosting → **Weaviate**
