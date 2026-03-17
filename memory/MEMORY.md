# Project Memory

## User Background

- **Role:** SDET, 11 years experience → transitioning to AI Quality / AI Safety Engineer
- **Location:** Hapur, India | **Employer:** US-based startup (full-time)
- **Education:** B.tech ECE, 2014
- **Programming:** Python (intermediate), JS (intermediate)
- **Tools:** Groq API, OpenAI API, VS Code, GitHub, Jupyter

## Target Roles

1. AI Safety Engineer (Anthropic, OpenAI, Google DeepMind, Meta)
2. Model Quality Software Engineer
3. LLM Evaluation Engineer
4. AI Trust & Safety Engineer

## Coaching Style

- User is new to AI eval — explain the "why" not just the "what"
- Point out what concepts matter for their target roles
- When reviewing eval results, help interpret what scores mean and what to fix
- Be direct but thorough when it matters for learning

## Project Structure

- `week4/src/` — main eval code
  - `eval_runner.py` — runs evals, writes CSV results
  - `metrics.py` — deepeval metrics, category→metric mapping
  - `rag_loader.py` — loads week3 Chroma DB, builds RAG chain (Groq llama-3.1-8b-instant)
  - `test_cases.py` — 19 test cases across 6 categories (vague, buried_content, trick, prompt_injection, out_of_scope, exact_facts, multi_part)

## Key Fixes Made

- Added `metric.measure(test_case)` in eval_runner.py — metrics were never being evaluated
- Added `.flake8` with `max-line-length = 88, extend-ignore = E501` to match Black formatter
- VSCode settings: Black formatter on save for Python
