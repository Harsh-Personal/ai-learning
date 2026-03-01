# Document Chunking - Feb 28

## My PDF:

- Title: sample_document.pdf
- Pages: 21 Pages
- Total characters: 109,934

## Results:

| Strategy    | Chunks | Avg Size   |
| ----------- | ------ | ---------- |
| Small 500   | 244    | 455 chars  |
| Medium 1000 | 129    | 908 chars  |
| Large 2000  | 70     | 1691 chars |

## Why overlap matters:

To not loose important context in case the chunks at a point which could confuse the llm of the context because of how the word will appear now. Overlapping adds part of tail of the chunk to head of next chunk making sure words are not cut/ommitted in a way leading to confusion

[Your understanding in 1-2 sentences]

## My prediction for tomorrow's RAG test:

- Best for specific questions ("What is X?"): [small]
- Best for summary questions ("Explain the main idea"): [medium]
- I'll start with: [medium - safe choice]

## Questions I have:

I didn't understand the code we used and implication from it. Like preview and retrieval although I observed retrieval is same irrespictive of chunk size
