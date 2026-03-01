"""
Week 3 - Document Chunking Experiment
Goal: Understand how chunk size affects RAG retrieval
"""

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pickle
import json

# 1. Load your PDF
print("Loading PDF...")
loader = PyPDFLoader("sample_document.pdf")  # ← your PDF filename
pages = loader.load()

total_chars = sum(len(p.page_content) for p in pages)
print(f"✅ {len(pages)} pages | {total_chars:,} total characters")

# 2. Three chunking strategies
strategies = {
    "small": RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50),
    "medium": RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100),
    "large": RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200),
}

results = {}

for name, splitter in strategies.items():
    chunks = splitter.split_documents(pages)
    avg_len = sum(len(c.page_content) for c in chunks) / len(chunks)

    results[name] = {"count": len(chunks), "avg_length": round(avg_len)}

    # Save for RAG building tomorrow
    with open(f"chunks_{name}.pkl", "wb") as f:
        pickle.dump(chunks, f)

    print(f"\n{name.upper()} chunks:")
    print(f"  Total: {len(chunks)} chunks")
    print(f"  Avg length: {avg_len:.0f} chars")
    print(f"  Preview: {chunks[0].page_content[:150]}...")

    print("\n--- PROOF chunks ARE different ---")
    print(f"\n{name.upper()} chunk[0] last 100 chars:")
    print(repr(chunks[0].page_content[-100:]))

# 3. Save stats
with open("chunking_stats.json", "w") as f:
    json.dump(results, f, indent=2)

print("\n✅ All chunks saved! Ready for RAG tomorrow.")
