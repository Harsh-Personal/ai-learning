# Embeddings Experiment Results

We are using model `all-MiniLM-L6-v2` which has 384 dimensions

## Experiment 1 Findings:

- "I love pizza" ↔ "Pizza is my favorite" = 0.885
- Were pizza sentences more similar than unrelated ones? Yes
- Surprising observation:
  0.433 | 'I love pizza' ↔ 'I hate vegetables'
  0.383 | 'Pizza is my favorite food' ↔ 'I hate vegetables'
  0.214 | 'Javascript' ↔ 'Playwright'

Expected more for 'Pizza is my favorite food' ↔ 'I hate vegetables' and 'Javascript' ↔ 'Playwright'

## Experiment 2 (Synonyms):

- Synonym similarity: [0.684]
- Antonym similarity: [0.373]
- This proves: High likelable words have more similarity and hence better score but also to note antonyms score is not in negative because some how they are also related

## Experiment 3 (Domain):

- Medical terms similarity: [0.611]
- ML terms similarity: [0.651]
- Cross-domain similarity: [0.081]
- This shows embeddings understand: We are able to identify idential domains

## My Domain Test:

[Paste your results from SDET terms]
Testing:
0.460 | 'python' ↔ 'pytest'
0.311 | 'python' ↔ 'Javascript'
0.211 | 'python' ↔ 'Playwright'

Javascript:
0.214 | 'Javascript' ↔ 'Playwright'

Playwright:
0.231 | 'Playwright' ↔ 'pytest'

## Key Learning:

Embeddings don’t just encode exact word matching; they capture semantic structure. Paraphrases like “I love pizza” and “Pizza is my favorite food” get very high similarity (~0.88), while food-related but sentiment‑different sentences (“I love pizza” vs “I hate vegetables”) land in the mid range (~0.38–0.43). Synonyms are clearly closer than antonyms, but antonyms still show moderate similarity because they share context (both are emotions). In my SDET domain test, python is closest to pytest, confirming that embeddings understand framework–language relationships, while tools like Playwright sit in between languages and testing frameworks, reflecting their multi‑language nature.
