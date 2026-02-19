# OrderBot - Pizza Ordering Chatbot 🍕

A collection of chatbot implementations for automated pizza ordering, demonstrating different approaches and best practices.

## 📁 Files Overview

### 1. `orderBot.py` (Original)
The original implementation with some issues:
- Uses OpenAI API
- Has unused imports and code
- Missing API key setup
- Basic functionality

**Use this to:** Learn from the original code and understand what needs improvement.

### 2. `orderBot_cleaned.py` ✨ (Recommended for OpenAI)
Clean, production-ready version using OpenAI:
- Removed unused code
- Added proper error handling
- Added documentation
- Fixed API key setup
- Better variable naming

**Use this to:** Deploy with OpenAI's GPT models.

### 3. `orderBot_groq.py` 🚀 (Recommended for Groq)
Optimized for Groq's fast inference:
- Uses LLaMA 3.3 70B model
- Fast response times
- Token usage tracking
- Enhanced UI with emojis

**Use this to:** Get faster responses with Groq's infrastructure.

### 4. `orderBot_enhanced.py` 💎 (Most Feature-Rich)
Production-ready with advanced features:
- Retry logic for API failures
- Conversation history export
- Session statistics tracking
- Reset functionality
- Loading indicators
- Better error messages

**Use this to:** Production deployments requiring reliability.

### 5. `SYSTEM_MESSAGE_GUIDE.md` 📖
Comprehensive guide on designing effective system messages:
- Principles and patterns
- Testing strategies
- Common pitfalls
- Real-world examples

**Use this to:** Learn how to craft effective AI instructions.

---

## 🚀 Quick Start

### Prerequisites

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install panel groq openai
```

### Setup API Keys

**For Groq versions:**
```bash
export GROQ_API_KEY="your-groq-api-key-here"
```

**For OpenAI versions:**
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

### Run the App

**Option 1: Groq (Fast & Free)**
```bash
panel serve orderBot_groq.py --show
```

**Option 2: OpenAI (GPT-4)**
```bash
panel serve orderBot_cleaned.py --show
```

**Option 3: Enhanced Version**
```bash
panel serve orderBot_enhanced.py --show
```

The app will open in your browser at `http://localhost:5006`

---

## 🎯 Feature Comparison

| Feature | Original | Cleaned | Groq | Enhanced |
|---------|----------|---------|------|----------|
| **Working out of the box** | ❌ | ✅ | ✅ | ✅ |
| **Error handling** | ❌ | ✅ | ✅ | ✅✅ |
| **API provider** | OpenAI | OpenAI | Groq | Groq |
| **Documentation** | ❌ | ✅ | ✅ | ✅✅ |
| **Retry logic** | ❌ | ❌ | ❌ | ✅ |
| **Save conversation** | ❌ | ❌ | ❌ | ✅ |
| **Statistics tracking** | ❌ | ❌ | ⚠️ | ✅ |
| **Reset function** | ❌ | ❌ | ❌ | ✅ |
| **Loading indicator** | ❌ | ❌ | ❌ | ✅ |
| **Empty message handling** | ❌ | ❌ | ✅ | ✅ |

---

## 🏗️ Architecture

### How It Works

```
┌─────────────┐
│   User UI   │  (Panel web interface)
└──────┬──────┘
       │
       ↓
┌─────────────────┐
│ collect_messages│  (Handle user input)
└──────┬──────────┘
       │
       ↓
┌──────────────────────┐
│ Conversation Context │  (Store all messages)
└──────┬───────────────┘
       │
       ↓
┌────────────────────────┐
│ get_completion_from... │  (Call AI API)
└──────┬─────────────────┘
       │
       ↓
┌─────────────┐
│  AI Model   │  (Groq/OpenAI)
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  Response   │  (Display in UI)
└─────────────┘
```

### Key Components

**1. System Message (Lines 68-100)**
- Defines the bot's personality
- Provides the menu
- Sets the conversation workflow

**2. Context Array**
- Stores entire conversation history
- Sent to AI with each request
- Enables memory and continuity

**3. Panels Array**
- UI display of messages
- Separate from context
- Visual representation only

**4. collect_messages Function**
- Main interaction handler
- Updates context and UI
- Calls AI API

---

## 🎨 Customization Guide

### Change the Menu

Edit the system message in any file:

```python
context = [
    {
        "role": "system",
        "content": """You are OrderBot...
        
The menu includes:
YOUR_ITEM_1  price1, price2, price3
YOUR_ITEM_2  price1, price2
...
"""
    }
]
```

### Change the Personality

Modify the style instruction:

```python
# Formal
"You respond in a professional, courteous manner."

# Casual
"You respond in a friendly, casual style with emojis!"

# Enthusiastic
"You're super excited about pizza! Show your enthusiasm!"
```

### Change the Model

**For Groq:**
```python
model="llama-3.3-70b-versatile"  # Fast, high quality
model="mixtral-8x7b-32768"       # Alternative
model="llama-3.1-8b-instant"     # Fastest
```

**For OpenAI:**
```python
model="gpt-4o-mini"     # Cheap, fast
model="gpt-4o"          # Best quality
model="gpt-3.5-turbo"   # Cheapest
```

### Change the Temperature

```python
temperature=0    # Deterministic, consistent
temperature=0.5  # Balanced
temperature=1    # Creative, varied
```

---

## 🧪 Testing

### Manual Testing Checklist

1. **Basic Flow**
   - [ ] Bot greets when you say "Hi"
   - [ ] Bot asks for order details
   - [ ] Bot asks pickup or delivery
   - [ ] Bot asks for address (if delivery)
   - [ ] Bot summarizes order
   - [ ] Bot asks for payment

2. **Edge Cases**
   - [ ] Empty message (should be ignored)
   - [ ] Vague request "I want pizza" (should clarify)
   - [ ] Off-topic question (should redirect)
   - [ ] Invalid item (should suggest from menu)

3. **Error Handling**
   - [ ] Network error (should show error message)
   - [ ] Invalid API key (should fail gracefully)
   - [ ] Long conversation (should maintain context)

### Automated Testing

```python
# test_orderbot.py
def test_greeting():
    context = [system_message]
    context.append({"role": "user", "content": "Hi"})
    response = get_completion_from_messages(context)
    assert "welcome" in response.lower() or "hello" in response.lower()

def test_menu_knowledge():
    context = [system_message]
    context.append({"role": "user", "content": "How much is a large pepperoni?"})
    response = get_completion_from_messages(context)
    assert "12.95" in response
```

---

## 📊 Performance Comparison

### Groq vs OpenAI

| Metric | Groq (LLaMA 3.3) | OpenAI (GPT-4o-mini) |
|--------|------------------|----------------------|
| **Response Time** | ~1-2 seconds | ~2-4 seconds |
| **Cost per 1M tokens** | Free tier available | $0.15 input, $0.60 output |
| **Quality** | Excellent | Excellent |
| **Rate Limits** | Generous | Depends on tier |
| **Best For** | Development, testing | Production, critical apps |

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'panel'"
```bash
pip install panel
```

### "Connection error" or "API key not found"
```bash
# Check your API key is set
echo $GROQ_API_KEY  # Should show your key

# If empty, set it:
export GROQ_API_KEY="your-key-here"
```

### "Address already in use" (Port 5006 busy)
```bash
# Use a different port
panel serve orderBot_groq.py --port 5007 --show
```

### Bot responses are slow
- Use Groq instead of OpenAI (faster inference)
- Use a smaller model (llama-3.1-8b-instant)
- Check your internet connection

### Bot doesn't remember previous messages
- Check that `context.append()` is being called
- Verify the context array includes all messages
- Print the context to debug: `print(context)`

---

## 🎓 Learning Path

1. **Start with:** `orderBot.py` - Understand the original code
2. **Read:** `SYSTEM_MESSAGE_GUIDE.md` - Learn system message design
3. **Run:** `orderBot_cleaned.py` - See clean code in action
4. **Experiment:** `orderBot_groq.py` - Try Groq's fast inference
5. **Deploy:** `orderBot_enhanced.py` - Use production features

---

## 🔗 Resources

### Documentation
- [Panel Documentation](https://panel.holoviz.org/)
- [Groq API Docs](https://console.groq.com/docs)
- [OpenAI API Docs](https://platform.openai.com/docs)

### Tutorials
- [Building Chatbots with LLMs](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/)
- [Panel Dashboard Tutorial](https://panel.holoviz.org/getting_started/index.html)

### Community
- [Groq Discord](https://discord.gg/groq)
- [Panel Discourse](https://discourse.holoviz.org/)

---

## 📝 Next Steps

### Enhancements to Try

1. **Add Authentication**
   - User login
   - Order history per user
   - Saved addresses

2. **Database Integration**
   - Store orders in database
   - Track inventory
   - Analytics dashboard

3. **Payment Integration**
   - Stripe/PayPal integration
   - Order confirmation emails
   - Receipt generation

4. **Multi-Language Support**
   - Detect user language
   - Translate menu
   - Localized responses

5. **Voice Interface**
   - Speech-to-text input
   - Text-to-speech output
   - Phone ordering

---

## 🤝 Contributing

Found a bug or have an improvement? Feel free to:
1. Document the issue
2. Create a test case
3. Implement the fix
4. Test thoroughly

---

## 📄 License

This is educational code for learning purposes.

---

## 🙏 Acknowledgments

- Based on DeepLearning.AI's ChatGPT course
- Uses Groq's fast inference infrastructure
- Built with Panel by HoloViz

---

**Happy Ordering! 🍕**
