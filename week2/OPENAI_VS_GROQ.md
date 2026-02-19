# OpenAI vs Groq: Code Differences 🔄

## Quick Summary

| Aspect | OpenAI | Groq |
|--------|--------|------|
| **Import** | `import openai` | `from groq import Groq` |
| **Setup** | `openai.api_key = "..."` | `client = Groq(api_key="...")` |
| **API Call** | `openai.ChatCompletion.create()` | `client.chat.completions.create()` |
| **Models** | GPT-4, GPT-3.5, etc. | LLaMA, Mixtral, etc. |
| **Speed** | 2-4 seconds | 1-2 seconds (faster!) |
| **Cost** | Paid (per token) | Free tier available |

---

## 1️⃣ Import Statements

### OpenAI
```python
import os
import openai
import panel as pn
```

### Groq
```python
import os
from groq import Groq  # Different import!
import panel as pn
```

**Key Difference:**
- OpenAI: Import the whole `openai` module
- Groq: Import the `Groq` class specifically

---

## 2️⃣ API Client Setup

### OpenAI
```python
# Set up OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# No client object needed - use openai directly
```

**How it works:**
- Set API key as a module-level variable
- All subsequent calls use this key automatically

### Groq
```python
# Initialize Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Use the client object for all API calls
```

**How it works:**
- Create a `client` object with the API key
- All API calls go through this client object
- More object-oriented approach

---

## 3️⃣ API Call Method

### OpenAI
```python
def get_completion_from_messages(messages, model="gpt-4o-mini", temperature=0):
    response = openai.ChatCompletion.create(
        model=model, 
        messages=messages, 
        temperature=temperature
    )
    return response.choices[0].message.content
```

**Structure:**
```
openai.ChatCompletion.create(...)
  └── Module.Class.Method
```

### Groq
```python
def get_completion_from_messages(messages, model="llama-3.3-70b-versatile", temperature=0):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content
```

**Structure:**
```
client.chat.completions.create(...)
  └── Object.Property.Property.Method
```

**Key Difference:**
- OpenAI: `openai.ChatCompletion.create()`
- Groq: `client.chat.completions.create()`

---

## 4️⃣ Model Names

### OpenAI Models
```python
model="gpt-4o-mini"        # Fast, cheap
model="gpt-4o"             # Best quality
model="gpt-3.5-turbo"      # Cheapest
model="gpt-4-turbo"        # Previous generation
```

**Naming pattern:** `gpt-[version]-[variant]`

### Groq Models
```python
model="llama-3.3-70b-versatile"    # LLaMA 3.3, 70B params
model="llama-3.1-8b-instant"       # Fastest
model="mixtral-8x7b-32768"         # Mixtral model
model="gemma2-9b-it"               # Google's Gemma
```

**Naming pattern:** `[model-name]-[size]-[variant]`

---

## 5️⃣ Response Structure

Both return the same structure, but access slightly differently:

### OpenAI
```python
response = openai.ChatCompletion.create(...)

# Access response
content = response.choices[0].message.content
tokens = response.usage.total_tokens  # Token usage
```

### Groq
```python
response = client.chat.completions.create(...)

# Access response (same!)
content = response.choices[0].message.content
tokens = response.usage.total_tokens  # Token usage
```

**Key Point:** Response structure is identical! Both follow OpenAI's format.

---

## 6️⃣ Error Handling

### OpenAI
```python
try:
    response = openai.ChatCompletion.create(...)
except openai.error.RateLimitError:
    print("Rate limit exceeded")
except openai.error.APIError:
    print("API error")
except Exception as e:
    print(f"Error: {e}")
```

### Groq
```python
try:
    response = client.chat.completions.create(...)
except Exception as e:
    # Groq uses standard exceptions
    print(f"Error: {e}")
```

**Key Difference:**
- OpenAI: Has specific exception types
- Groq: Uses generic exceptions (simpler)

---

## 7️⃣ Complete Side-by-Side Comparison

### OpenAI Version
```python
import openai

# Setup
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Function
def get_completion(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content

# Usage
messages = [{"role": "user", "content": "Hello"}]
result = get_completion(messages)
```

### Groq Version
```python
from groq import Groq

# Setup
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Function
def get_completion(messages):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content

# Usage
messages = [{"role": "user", "content": "Hello"}]
result = get_completion(messages)
```

---

## 8️⃣ Environment Variables

### OpenAI
```bash
export OPENAI_API_KEY="sk-proj-..."
```

### Groq
```bash
export GROQ_API_KEY="gsk_..."
```

**Key Difference:** Different environment variable names!

---

## 9️⃣ Performance Comparison

### Speed Test Results

**Prompt:** "Explain testing in AI" (generates ~700 tokens)

| Provider | Average Response Time | Tokens/Second |
|----------|----------------------|---------------|
| OpenAI (GPT-4o-mini) | 2-4 seconds | ~200-350 |
| Groq (LLaMA 3.3) | 1-2 seconds | ~350-700 |

**Winner:** Groq is **2x faster** 🚀

### Cost Comparison

**For 1 Million Tokens:**

| Provider | Input Cost | Output Cost | Total (avg) |
|----------|-----------|-------------|-------------|
| OpenAI (GPT-4o-mini) | $0.15 | $0.60 | ~$0.38 |
| Groq (LLaMA 3.3) | Free tier | Free tier | $0.00* |

*Free tier has limits; paid tier available

---

## 🔟 Converting Between OpenAI and Groq

### Step-by-Step Conversion

**1. Change the import:**
```python
# FROM:
import openai

# TO:
from groq import Groq
```

**2. Change the setup:**
```python
# FROM:
openai.api_key = os.environ.get("OPENAI_API_KEY")

# TO:
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
```

**3. Change the API call:**
```python
# FROM:
response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=messages,
    temperature=0
)

# TO:
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,
    temperature=0
)
```

**4. Everything else stays the same!**
- Message format: Same
- Response access: Same
- Context handling: Same
- UI code: Same

---

## 1️⃣1️⃣ Compatibility

### What's the Same? ✅

Both APIs support:
- ✅ Chat completions
- ✅ System/user/assistant messages
- ✅ Temperature control
- ✅ Streaming (real-time responses)
- ✅ Token usage tracking
- ✅ Max tokens limit

### What's Different? ⚠️

| Feature | OpenAI | Groq |
|---------|--------|------|
| **Function calling** | ✅ Yes | ⚠️ Limited |
| **Vision (images)** | ✅ Yes | ❌ No |
| **Fine-tuning** | ✅ Yes | ❌ No |
| **Embeddings** | ✅ Yes | ❌ No |
| **Moderation** | ✅ Yes | ❌ No |

---

## 1️⃣2️⃣ When to Use Which?

### Use OpenAI When:
- ✅ You need vision/image understanding
- ✅ You need function calling
- ✅ You need embeddings
- ✅ You want the absolute best quality
- ✅ Cost isn't a major concern

### Use Groq When:
- ✅ You need **fast** responses
- ✅ You're building/testing/learning
- ✅ You want to save money
- ✅ You only need text chat
- ✅ You want open-source models

---

## 1️⃣3️⃣ Real-World Example: OrderBot

### Why OrderBot Works Great with Both:

**Requirements:**
- ✅ Text-only chat (no images needed)
- ✅ Simple conversation flow
- ✅ No function calling needed
- ✅ Standard chat format

**With OpenAI:**
- Reliable, well-tested
- Slightly slower
- Costs money

**With Groq:**
- Much faster responses
- Free tier available
- Same quality for this use case

**Verdict:** Groq is better for OrderBot! 🎯

---

## 1️⃣4️⃣ Migration Checklist

Converting from OpenAI to Groq? Follow this checklist:

- [ ] Install Groq: `pip install groq`
- [ ] Get Groq API key from [console.groq.com](https://console.groq.com)
- [ ] Set environment variable: `export GROQ_API_KEY="..."`
- [ ] Change import statement
- [ ] Create client object
- [ ] Update API call method
- [ ] Change model name
- [ ] Test thoroughly
- [ ] Update error handling (if using specific OpenAI exceptions)
- [ ] Update documentation

---

## 1️⃣5️⃣ Code Template for Both

### Universal Template (Works with Both!)

```python
# config.py
PROVIDER = "groq"  # or "openai"

if PROVIDER == "openai":
    import openai
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    
    def get_completion(messages):
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0
        )
        return response.choices[0].message.content

elif PROVIDER == "groq":
    from groq import Groq
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    def get_completion(messages):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0
        )
        return response.choices[0].message.content
```

---

## 🎯 Key Takeaways

1. **API Structure:** OpenAI uses module-level, Groq uses object-oriented
2. **Speed:** Groq is ~2x faster
3. **Cost:** Groq has free tier, OpenAI is paid
4. **Quality:** Both excellent for chat
5. **Conversion:** Easy - just 3 main changes!
6. **Use Case:** Choose based on your needs (speed vs features)

---

## 📚 Quick Reference

### OpenAI Cheat Sheet
```python
import openai
openai.api_key = "sk-..."
response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hi"}]
)
print(response.choices[0].message.content)
```

### Groq Cheat Sheet
```python
from groq import Groq
client = Groq(api_key="gsk_...")
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Hi"}]
)
print(response.choices[0].message.content)
```

---

**Bottom Line:** The APIs are very similar! Main differences are setup and the API call method. Everything else (messages, responses, context) works the same way. 🎉
