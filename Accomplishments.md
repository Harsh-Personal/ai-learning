Week 3:

After learning embeddings realized we are using old model of open-ai embeddings ada-002
instead of text-embedding-3-small which allows for dynamic dimensions based on our use case and save cost, faster search

smaller dimensions = faster search + lower storage but slightly less accuracy we will see from evaluations

Adding relevant evaluations and update model to check what best dimensions will work is great implementation

Weaviate is interesting because it supports both vector search (pure semantic similarity) and hybrid search (vector + keyword BM25).

Our codebase is using vector search today. Understanding when hybrid search would give better results is a great addition to my learning.
