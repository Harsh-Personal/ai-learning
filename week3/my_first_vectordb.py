# my_first_vectordb.py
import chromadb
from chromadb.utils import embedding_functions

print("Initializing ChromaDB...")

# Create ChromaDB client (creates local database)
client = chromadb.PersistentClient(path="./chroma_db")

# Create collection (like a "table" in SQL)
collection = client.get_or_create_collection(
    name="test_collection", metadata={"description": "My first vector database"}
)

print("✅ Collection created!")

# Add documents (ChromaDB auto-generates embeddings)
documents = [
    "The capital of France is Paris",
    "Python is a programming language",
    "Machine learning uses data to train models",
    "Paris is known for the Eiffel Tower",
    "JavaScript is used for web development",
    "The Eiffel Tower is 330 meters tall",
    "TypeScript is a superset of JavaScript",
    "Deep learning is a subset of machine learning",
]

ids = [f"doc{i}" for i in range(len(documents))]

metadatas = [
    {"category": "geography", "topic": "France"},
    {"category": "programming", "topic": "Python"},
    {"category": "AI", "topic": "ML"},
    {"category": "geography", "topic": "Paris"},
    {"category": "programming", "topic": "JavaScript"},
    {"category": "geography", "topic": "Paris"},
    {"category": "programming", "topic": "TypeScript"},
    {"category": "AI", "topic": "deep learning"},
]

print("\nAdding documents to database...")
collection.add(documents=documents, ids=ids, metadatas=metadatas)
print(f"✅ Added {len(documents)} documents")

# QUERY 1: Semantic search
print("\n" + "=" * 60)
print("QUERY 1: 'Tell me about France'")
print("=" * 60)

results = collection.query(query_texts=["Tell me about France"], n_results=3)

print("\nTop 3 Results:")
for i, doc in enumerate(results["documents"][0]):
    distance = results["distances"][0][i]
    print(f"\n{i+1}. {doc}")
    print(f"   Distance: {distance:.4f} (lower = more similar)")

# QUERY 2: Programming question
print("\n" + "=" * 60)
print("QUERY 2: 'Which languages are for coding?'")
print("=" * 60)

results2 = collection.query(
    query_texts=["Which languages are for coding?"], n_results=3
)

print("\nTop 3 Results:")
for i, doc in enumerate(results2["documents"][0]):
    distance = results2["distances"][0][i]
    print(f"{i+1}. {doc} (Distance: {distance:.4f})")

# QUERY 3: Metadata filtering
print("\n" + "=" * 60)
print("QUERY 3: 'France' but ONLY geography category")
print("=" * 60)

results3 = collection.query(
    query_texts=["France"],
    n_results=3,
    where={"category": "geography"},  # Filter by metadata
)

print("\nResults (geography only):")
for doc in results3["documents"][0]:
    distance = results3["distances"][0][i]
    print(f"{i+1}. {doc} (Distance: {distance:.4f})")

# QUERY 4: "Trick question" - not in database
print("\n" + "=" * 60)
print("QUERY 4: 'What is the weather in Tokyo?'")
print("=" * 60)

results4 = collection.query(query_texts=["What is the weather in Tokyo?"], n_results=2)

print("\nTop 2 Results:")
for i, doc in enumerate(results4["documents"][0]):
    print(f"{i+1}. {doc}")
    print(f"   Distance: {results4['distances'][0][i]:.4f}")

print("\n⚠️ NOTICE: It returned SOMETHING, even though we have")
print("no weather data. This is a key limitation of RAG!")

print("\n✅ Database auto-saved to ./chroma_db")

# QUERY 1: Semantic search
print("\n" + "=" * 60)
print("QUERY 4: 'Explain deep learning'")
print("=" * 60)

results = collection.query(query_texts=["Explain deep learning"], n_results=3)

print("\nTop 3 Results:")
for i, doc in enumerate(results["documents"][0]):
    distance = results["distances"][0][i]
    print(f"\n{i+1}. {doc}")
    print(f"   Distance: {distance:.4f} (lower = more similar)")
