# 🎓 Complete Learning Guide: OrderBot with Calculator

## 📚 Table of Contents

1. [Overview - The Big Picture](#overview)
2. [Setup & Imports](#section-1-setup)
3. [The Calculator Tool](#section-2-calculator-tool)
4. [The Brain: System Message](#section-3-system-message)
5. [Getting Bot Responses](#section-4-bot-response)
6. [Handling User Input](#section-5-user-input)
7. [The UI](#section-6-ui)
8. [How It All Works Together](#how-it-works)

---

## Overview - The Big Picture 🗺️

**Think of this app like a restaurant:**

- **You** = Customer placing order
- **OrderBot** = Waiter taking your order
- **Calculator Tool** = Cash register for accurate prices
- **UI (Panel)** = The menu board and order screen

**The Flow:**

```
You type message → Send to Groq API → Bot decides if it needs calculator
                                      ↓
                            Bot uses calculator for math
                                      ↓
                            Bot responds with answer → Display in UI
```

---

## Section 1: Setup & Imports (Lines 1-12)

### The Code:

```python
import os
from groq import Groq
import panel as pn
import json

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
pn.extension()
```

### What Each Line Does:

**`import os`**

- Access operating system functions
- Used to read environment variables (like API keys)
- **Why?** Keeps secrets safe (not hardcoded in code)

**`from groq import Groq`**

- Import the Groq library
- **Analogy:** Like importing a phone to call someone
- Groq = The phone company that connects us to the AI

**`import panel as pn`**

- Import Panel for building the web interface
- `as pn` = nickname (shorter to type)
- **Analogy:** Panel is like HTML/CSS but easier

**`import json`**

- Handle JSON data (JavaScript Object Notation)
- **Why?** Bot sends calculator requests as JSON

**`client = Groq(api_key=...)`**

- Create a connection to Groq's servers
- API key = Your password to use Groq
- `os.environ.get("GROQ_API_KEY")` = Read key from environment variable

**`pn.extension()`**

- Initialize Panel
- **Must run** before using any Panel features

---

## Section 2: The Calculator Tool (Lines 14-47)

### The Tool Definition (Lines 15-34):

```python
calculator_tool = {
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "Perform basic arithmetic calculations",
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "The operation to perform"
                },
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number"}
            },
            "required": ["operation", "a", "b"]
        }
    }
}
```

### What This Means:

**Think of it as an instruction manual for the bot:**

```
Tool Name: "calculate"
Purpose: Do math

How to Use:
1. Choose operation: add, subtract, multiply, or divide
2. Provide first number (a)
3. Provide second number (b)

Example: calculate(operation="subtract", a=10.95, b=9.25)
```

**Why JSON format?**

- Standard way computers describe functions
- Like a contract: "If you call me with these inputs, I'll give you this output"

### The Calculator Function (Lines 37-47):

```python
def calculate(operation, a, b):
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b if b != 0 else "Error: Division by zero"
    return "Error: Unknown operation"
```

**This is the actual calculator:**

- Takes 3 inputs: operation, a, b
- Does the math
- Returns the result

**Example:**

```python
calculate("subtract", 10.95, 9.25)  # Returns: 1.70
```

---

## Section 3: The Brain - System Message (Lines 50-84)

```python
context = [{
    "role": "system",
    "content": """You are OrderBot, an automated service...

    IMPORTANT: When you need to calculate prices, USE THE CALCULATE TOOL.

    The menu includes...
    """
}]
```

### What is This?

**The system message = Bot's job description + training manual**

**Analogy:** Imagine training a new employee:

- "You are a waiter at a pizza restaurant"
- "Here's how you take orders: step 1, step 2..."
- "Here's our menu with prices"
- "If customer asks about price differences, use the calculator"

### Key Parts:

1. **Identity:** "You are OrderBot"
2. **Process:** Greet → Order → Pickup/Delivery → Address → Payment
3. **Tools:** "USE THE CALCULATE TOOL for math"
4. **Knowledge:** The complete menu
5. **Style:** "conversational friendly style"

### Why "context"?

**Context = Conversation memory**

```python
context = [
    {system message},
    {user: "Hi"},
    {assistant: "Welcome!"},
    {user: "I want pizza"},
    {assistant: "Which size?"}
]
```

Every message gets added to context → Bot remembers the conversation

---

## Section 4: Getting Bot Responses (Lines 94-162)

This is the **most complex** part. Let's break it down:

### The Function:

```python
def get_bot_response(messages):
```

**Purpose:** Send messages to AI, handle calculator if needed, return response

### Step-by-Step Flow:

#### **Step 1: Call the AI (Lines 96-101)**

```python
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,
    tools=[calculator_tool],  # ← Give bot access to calculator
    temperature=0
)
```

**What happens:**

- Send conversation to Groq
- "Here's a calculator tool you can use"
- Get response back

**Temperature=0:** Be consistent, not creative

#### **Step 2: Print Token Usage (Lines 103-110)**

```python
if hasattr(response, "usage"):
    print(f"TOKEN USAGE:")
    print(f"  Prompt tokens: {response.usage.prompt_tokens}")
    print(f"  Completion tokens: {response.usage.completion_tokens}")
    print(f"  Total tokens: {response.usage.total_tokens}")
```

**What are tokens?**

- Words (roughly): "Hello" = 1 token, "pizza" = 1 token
- **Prompt tokens:** Your messages + system message
- **Completion tokens:** Bot's response
- **Why track?** Groq charges per token (or has limits)

#### **Step 3: Check if Bot Wants Calculator (Lines 115-143)**

```python
if message.tool_calls:
```

**This means:** Bot decided "I need to do math!"

**Example scenario:**

- User: "What's the difference between large and medium?"
- Bot thinks: "Let me calculate 10.95 - 9.25"
- Bot: _calls calculator tool_

**What we do:**

```python
# Extract the calculator request
function_name = tool_call.function.name  # "calculate"
function_args = json.loads(tool_call.function.arguments)
# {"operation": "subtract", "a": 10.95, "b": 9.25}

# Actually do the calculation
result = calculate(
    function_args["operation"],
    float(function_args["a"]),
    float(function_args["b"])
)
# result = 1.70

# Tell bot the answer
messages.append({"role": "tool", "content": "1.70"})
```

**Analogy:**

- Bot: "Hey, can you calculate 10.95 - 9.25?"
- Calculator: "Sure! The answer is 1.70"
- Bot: "Thanks! Now I can tell the user"

#### **Step 4: Get Final Response (Lines 145-159)**

```python
final_response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,  # ← Now includes calculator result!
    temperature=0
)
return final_response.choices[0].message.content
```

**Now bot knows:** "The calculator told me 1.70"

**Bot responds:** "The difference is $1.70"

**This is what user sees!**

---

## Section 5: Handling User Input (Lines 165-194)

```python
def send_message(event):
```

**This function runs when user clicks "Send"**

### Step-by-Step:

#### **Step 1: Get User's Message (Lines 166-168)**

```python
user_msg = text_input.value.strip()
if not user_msg:
    return  # Don't send empty messages
```

**`strip()`:** Remove extra spaces

- " hello " → "hello"

#### **Step 2: Clear Input & Display Message (Lines 170-173)**

```python
text_input.value = ""  # Clear the text box
chat_log.append(pn.pane.Markdown(f"**👤 You:** {user_msg}"))
```

**User sees:** "👤 You: I want pizza"

#### **Step 3: Add to Context (Line 176)**

```python
context.append({"role": "user", "content": user_msg})
```

**Now context includes:**

```python
[
    {system message},
    {previous messages...},
    {"role": "user", "content": "I want pizza"}  ← New!
]
```

#### **Step 4: Get Bot Response (Lines 178-186)**

```python
bot_msg = get_bot_response(context)  # ← Handles calculator internally

if bot_msg and bot_msg.strip():
    chat_log.append(pn.pane.Markdown(f"**🤖 OrderBot:** {bot_msg}"))
    context.append({"role": "assistant", "content": bot_msg})
```

**Flow:**

1. Send context to bot
2. Bot might use calculator (hidden from user)
3. Bot returns final answer
4. Display answer
5. Add to context for next message

#### **Step 5: Error Handling (Lines 187-194)**

```python
except Exception as e:
    chat_log.append(
        pn.pane.Markdown("Sorry, I had trouble...")
    )
```

**If something breaks:** Show friendly message, not scary error

---

## Section 6: The UI (Lines 197-207)

```python
text_input = pn.widgets.TextInput(
    placeholder="Type here and click Send...",
    width=400
)
send_btn = pn.widgets.Button(name="Send", button_type="primary", width=100)
send_btn.on_click(send_message)
```

### Creating UI Components:

**`TextInput`:** Text box where user types

- `placeholder`: Hint text
- `width=400`: Size in pixels

**`Button`:** Click to send

- `button_type="primary"`: Make it blue (important button)

**`on_click(send_message)`:** When clicked → run `send_message` function

### The Layout:

```python
pn.template.FastListTemplate(
    title="🍕 OrderBot (with Calculator)",
    main=[
        pn.Card(chat_log, title="Chat", height=600, scroll=True),
        pn.Row(text_input, send_btn)
    ]
).servable()
```

**Template:** Pre-made page layout

**Structure:**

```
┌─────────────────────────┐
│  🍕 OrderBot            │ ← Title
├─────────────────────────┤
│  Chat Card (scrollable) │ ← Chat history
│  600px high             │
├─────────────────────────┤
│ [Text Input] [Send]     │ ← Input row
└─────────────────────────┘
```

**`.servable()`:** Make it available as web page

---

## How It All Works Together 🎯

### Complete Flow Example:

**User types:** "What's the price difference between large and medium cheese?"

```
1. send_message() runs
   ├─ Get user message: "What's the price difference..."
   ├─ Clear input box
   ├─ Show in chat: "👤 You: What's the price..."
   └─ Add to context

2. get_bot_response(context) called
   ├─ Send to Groq API with calculator tool
   └─ Bot receives message

3. Bot thinks...
   ├─ "User wants price difference"
   ├─ "I need to calculate: 10.95 - 9.25"
   └─ Bot calls calculator tool

4. Calculator tool call detected
   ├─ Extract: operation="subtract", a=10.95, b=9.25
   ├─ Run: calculate("subtract", 10.95, 9.25)
   ├─ Result: 1.70
   └─ Add to context: "Tool result: 1.70"

5. Bot called again with calculator result
   ├─ Bot now knows: "The result is 1.70"
   └─ Bot formulates response: "The difference is $1.70"

6. Display response
   ├─ Show: "🤖 OrderBot: The difference is $1.70"
   └─ Add to context for memory

7. Wait for next user message...
```

---

## Key Concepts to Remember 🔑

### 1. **Context is Memory**

```python
context = [system, user1, bot1, user2, bot2, ...]
```

- Bot remembers entire conversation
- Gets longer with each message
- More context = more tokens = higher cost

### 2. **Tool Calls are Hidden**

- User types: "What's the difference?"
- User sees: "The difference is $1.70"
- User **doesn't see:** `calculate(subtract, 10.95, 9.25)`

### 3. **Two API Calls for Calculator**

- First call: Bot decides to use calculator
- Second call: Bot uses calculator result to respond
- That's why we see 2 token usage prints!

### 4. **Separation of Concerns**

- **UI (Panel):** What user sees
- **Logic (functions):** How it works
- **Data (context):** What it remembers
- **API (Groq):** The AI brain

---

## Common Questions ❓

### Q: Why use a calculator tool? Can't the bot do math?

**A:** LLMs are text predictors, not calculators!

- They "guess" numbers based on patterns
- Often make mistakes (like 10.95 - 9.25 = 1.70 ❌ might be 1.65)
- Calculator tool = 100% accurate

### Q: What's the difference between `context` and `chat_log`?

**A:**

- **`context`:** Data sent to API (conversation history)
- **`chat_log`:** UI display (what user sees)
- Context includes hidden stuff (tool calls), chat_log doesn't

### Q: Why `temperature=0`?

**A:**

- Temperature controls randomness
- 0 = Deterministic, consistent answers
- 1 = Creative, varied answers
- For a restaurant bot, we want consistency!

### Q: What if calculator isn't enough?

**A:** You can add more tools!

- Database lookup (check inventory)
- Payment processor (charge customer)
- Email sender (send confirmation)
- Same pattern: define tool → bot calls it → return result

---

## Try It Yourself! 🧪

### Experiment 1: Change the Calculator

Add a new operation:

```python
elif operation == "percentage":
    return (a / b) * 100
```

Then update the tool definition:

```python
"enum": ["add", "subtract", "multiply", "divide", "percentage"]
```

### Experiment 2: Track Stats

Add to `send_message()`:

```python
message_count = len([m for m in context if m.get("role") == "user"])
print(f"Total messages: {message_count}")
```

### Experiment 3: Add Menu Item

Edit system message:

```python
"garlic bread 4.50 \"
```

Bot will now know about garlic bread!

---

## Next Steps 📈

**Now that you understand this, try:**

1. **Add a new tool** (e.g., check_inventory)
2. **Modify the UI** (add a reset button)
3. **Change the bot personality** (make it funny/formal)
4. **Add conversation export** (save to JSON file)

---

**You now understand:**

- ✅ How LLM APIs work
- ✅ How to give bots tools
- ✅ How to build chat interfaces
- ✅ How context/memory works
- ✅ How to handle tool calls

**Keep learning! 🚀**
