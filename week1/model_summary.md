# Groq Models Analysis

## 📋 Field Explanations

| Field | Meaning |
|-------|---------|
| **id** | Model identifier - use this when making API calls (e.g., `model="llama-3.3-70b-versatile"`) |
| **owned_by** | Company/organization that created the model |
| **context_window** | Maximum **input** tokens the model can process (your prompt + conversation history) |
| **max_completion_tokens** | Maximum tokens the model can **generate** in its response |
| **active** | Whether the model is currently available for use (all are `True` in your list) |
| **created** | Unix timestamp of when the model was added to Groq |

## 💰 Pricing - FREE vs PAID

**Good News: ALL models are available on Groq's FREE tier!**

### Free Tier Limits:
- ✅ 30 requests per minute
- ✅ 14,400 tokens per minute  
- ✅ 7,000 requests per day

### When You Need Paid:
- ❌ If you exceed the above rate limits
- ❌ For production applications with high traffic
- ❌ For commercial use at scale

**All 20 models in your list work on the free tier** - you just hit rate limits if you use them too much.

## 🔢 Models by Context Window Size

### Smallest Context Window (512 tokens):
1. **meta-llama/llama-prompt-guard-2-22m** - 512 tokens
2. **meta-llama/llama-prompt-guard-2-86m** - 512 tokens
   - 💡 Use case: These are specialized "guard" models for detecting prompt injections/jailbreaks, not for general chat

### Small Context (4,000-4,096 tokens):
3. **canopylabs/orpheus-arabic-saudi** - 4,000 tokens
4. **canopylabs/orpheus-v1-english** - 4,000 tokens  
5. **allam-2-7b** - 4,096 tokens
   - 💡 Use case: Short conversations, quick tasks, when you want to save tokens

### Large Context (131,072 tokens = 128K):
Most models have this size:
- **llama-3.3-70b-versatile** ⭐ (RECOMMENDED)
- **llama-3.1-8b-instant** ⭐ (FASTEST)
- **meta-llama/llama-4-scout-17b-16e-instruct**
- **meta-llama/llama-4-maverick-17b-128e-instruct**
- **meta-llama/llama-guard-4-12b**
- **qwen/qwen3-32b**
- **moonshotai/kimi-k2-instruct**
- **groq/compound-mini**
- **groq/compound**
- **openai/gpt-oss-120b**
- **openai/gpt-oss-20b**
- **openai/gpt-oss-safeguard-20b**
  - 💡 Use case: Large documents, long conversations, complex multi-turn tasks

### Largest Context (262,144 tokens = 256K):
- **moonshotai/kimi-k2-instruct-0905** - 262,144 tokens
  - 💡 Use case: Analyzing entire codebases, very long documents, extensive context

### Special Models (Whisper - Audio):
- **whisper-large-v3** - 448 tokens
- **whisper-large-v3-turbo** - 448 tokens
  - 💡 Use case: Audio transcription (not text chat)

## 🎯 Recommendations

### 1. **Best for General Use** (Balance of speed, quality, context):
```python
model = "llama-3.3-70b-versatile"
```
- Context: 131,072 tokens (128K)
- Max output: 32,768 tokens (32K)
- Great quality, good speed

### 2. **Fastest Model** (When speed matters most):
```python
model = "llama-3.1-8b-instant"
```
- Context: 131,072 tokens (128K)
- Max output: 131,072 tokens (128K)
- Smaller model = faster responses

### 3. **Largest Context** (For huge documents):
```python
model = "moonshotai/kimi-k2-instruct-0905"
```
- Context: 262,144 tokens (256K)
- Max output: 16,384 tokens (16K)
- Can handle massive inputs

### 4. **Most Token-Efficient** (Minimize costs if on paid tier):
```python
model = "allam-2-7b"
```
- Context: 4,096 tokens (4K)
- Max output: 4,096 tokens (4K)
- Use for simple, short tasks

## 🧮 Understanding Token Limits

**Example: llama-3.3-70b-versatile**
- `context_window: 131,072` = You can send up to 128K tokens as input
- `max_completion_tokens: 32,768` = The model can respond with up to 32K tokens

**Total tokens per request** = input tokens + output tokens

**Rough conversion:** 1 token ≈ 0.75 words (so 1,000 tokens ≈ 750 words)

## 📊 Quick Comparison Table

| Model | Context | Max Output | Speed | Quality | Best For |
|-------|---------|------------|-------|---------|----------|
| llama-3.1-8b-instant | 128K | 128K | ⚡⚡⚡ | ⭐⭐⭐ | Fast responses |
| llama-3.3-70b-versatile | 128K | 32K | ⚡⚡ | ⭐⭐⭐⭐ | General use |
| openai/gpt-oss-120b | 128K | 65K | ⚡ | ⭐⭐⭐⭐⭐ | High quality |
| kimi-k2-instruct-0905 | 256K | 16K | ⚡ | ⭐⭐⭐⭐ | Huge context |
| allam-2-7b | 4K | 4K | ⚡⚡⚡ | ⭐⭐ | Token efficiency |

## 🚀 How to Use in Your Code

```python
from groq import Groq
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Choose your model based on needs
chat_completion = client.chat.completions.create(
    messages=[
        {"role": "user", "content": "Your question here"}
    ],
    model="llama-3.3-70b-versatile",  # Change this to any model ID
)

print(chat_completion.choices[0].message.content)
```

## 💡 Pro Tips

1. **Start with free tier** - It's generous for learning and small projects
2. **Use llama-3.3-70b-versatile** for most tasks - great balance
3. **Use llama-3.1-8b-instant** when you need speed over quality
4. **Monitor your token usage** to stay within free tier limits
5. **Whisper models** are for audio transcription, not text chat
6. **Guard models** are for safety checks, not conversations
