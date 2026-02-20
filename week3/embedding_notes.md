# My Embeddings Notes (Final)

## What is an embedding?

An embedding is a numerical representation of text, audio, or image
as a vector of numbers. Machines understand numbers, not words, so
embeddings convert the MEANING of text into math that machines can
process. Each embedding is typically 384-1536 numbers.

## Why vectors?

1. Machines need numbers to do computation
2. Vectors have MULTIPLE dimensions (e.g., 384 numbers)
3. Each dimension captures different aspects of meaning
4. This allows efficient similarity calculation (cosine similarity)
5. Makes semantic search possible

## Semantic similarity:

Two words or phrases that express similar meaning should have similar
embeddings (close vector values). For example, "happy" and "joyful"
will have similarity score of 0.85+, allowing machines to understand
they're related even though the words are different.

## When to use embeddings:

✅ Semantic search (find similar meaning)
✅ Document similarity
✅ RAG systems (retrieve relevant context)
✅ Classification/categorization
✅ Large datasets (1000s+ items)

## When NOT to use:

❌ Exact matching needed (email, IDs)
❌ Structured data queries (SQL better)
❌ Small datasets (<100 items)
❌ Simple keyword search

## My aha moment:

This is HOW we teach machines to understand language meaning!
Embeddings are the bridge between human language and machine math.

## Real-world application:

My company could use embeddings for semantic search across trial
documents, finding similar protocols, and auto-categorizing QC issues.

Typical cosine similarity ranges for these models:

0.8+ → Very similar (often paraphrases).

0.6–0.8 → Related in topic.

0.3–0.6 → Loosely related, same domain/theme.

<0.3 → Mostly unrelated.
