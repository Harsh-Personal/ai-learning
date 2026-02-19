# System Message Design Guide 🎯

## What is a System Message?

A **system message** is a special instruction that defines:
- **WHO** the AI is (identity/role)
- **WHAT** it should do (purpose/tasks)
- **HOW** it should behave (personality/style)
- **WHAT IT KNOWS** (context/data)

Think of it as the AI's "job description" and "training manual" combined.

---

## Anatomy of the OrderBot System Message

Let's break down the OrderBot system message piece by piece:

### 1. Identity & Role 🎭

```
"You are OrderBot, an automated service to collect orders for a pizza restaurant."
```

**Purpose:**
- Gives the AI a clear identity
- Sets expectations for its capabilities
- Defines the scope of interaction

**Why it matters:**
- Without this, the AI might answer general questions
- With this, it stays focused on pizza ordering

**Example alternatives:**
- ❌ "You are a helpful assistant" (too vague)
- ✅ "You are OrderBot, a pizza ordering specialist"
- ✅ "You are a virtual cashier at Mario's Pizza"

---

### 2. Workflow Definition 📋

```
"You first greet the customer, then collects the order, 
and then asks if it's a pickup or delivery. 
You wait to collect the entire order, then summarize it and check for a final 
time if the customer wants to add anything else. 
If it's a delivery, you ask for an address. 
Finally you collect the payment."
```

**Purpose:**
- Defines the conversation flow
- Ensures consistent experience
- Prevents skipping important steps

**The Flow:**
1. **Greet** → Build rapport
2. **Collect order** → Get items
3. **Pickup or delivery?** → Logistics
4. **Summarize & confirm** → Accuracy check
5. **Get address** (if delivery) → Fulfillment info
6. **Collect payment** → Transaction

**Why this order matters:**
- Logical progression (greeting before ordering)
- Prevents errors (confirm before payment)
- Better UX (address only if needed)

**Testing the workflow:**
```python
# Good: Follows the flow
User: "Hi"
Bot: "Hello! Welcome to our pizza place. What can I get for you?"

# Bad: Skips steps
User: "Hi"
Bot: "Cash or card?" ❌ (Too fast!)
```

---

### 3. Behavioral Guidelines 🎨

```
"Make sure to clarify all options, extras and sizes to uniquely 
identify the item from the menu."
```

**Purpose:**
- Prevents ambiguity
- Reduces order errors
- Improves customer satisfaction

**Example interaction:**
```
User: "I want a pizza"
Bot: "Great! Which pizza would you like? We have pepperoni, cheese, 
     or eggplant. And what size - small, medium, or large?"
```

**Without this instruction:**
```
User: "I want a pizza"
Bot: "OK, added pizza to your order" ❌ (What kind? What size?)
```

---

### 4. Personality & Tone 💬

```
"You respond in a short, very conversational friendly style."
```

**Purpose:**
- Makes interaction feel natural
- Keeps responses concise
- Creates positive experience

**Impact on responses:**

**With "short, conversational, friendly":**
```
"Hey! 👋 What can I get you today?"
```

**Without this (default formal):**
```
"Good day. I am here to assist you with placing an order. 
Please provide me with your selection from our menu."
```

**Style guidelines breakdown:**
- **Short**: No long paragraphs, get to the point
- **Conversational**: Use contractions, casual language
- **Friendly**: Warm tone, emojis (if appropriate)

---

### 5. Knowledge Base (The Menu) 📖

```
"The menu includes 
pepperoni pizza  12.95, 10.00, 7.00 
cheese pizza   10.95, 9.25, 6.50 
eggplant pizza   11.95, 9.75, 6.75 
fries 4.50, 3.50 
greek salad 7.25 
Toppings: 
extra cheese 2.00, 
mushrooms 1.50 
sausage 3.00 
canadian bacon 3.50 
AI sauce 1.50 
peppers 1.00 
Drinks: 
coke 3.00, 2.00, 1.00 
sprite 3.00, 2.00, 1.00 
bottled water 5.00"
```

**Purpose:**
- Provides factual data
- Enables accurate pricing
- Limits scope to available items

**Structure:**
- **Items with 3 prices** = Small, Medium, Large
- **Items with 2 prices** = Small, Large
- **Items with 1 price** = One size only

**Why include prices:**
- Bot can calculate totals
- Customer knows cost upfront
- Transparency builds trust

**What happens without the menu:**
```
User: "How much is a large pepperoni?"
Bot: "I don't have access to pricing information" ❌
```

**With the menu:**
```
User: "How much is a large pepperoni?"
Bot: "A large pepperoni pizza is $12.95!" ✅
```

---

## System Message Design Principles 🏗️

### 1. **Be Specific, Not Generic**

❌ Bad:
```
"You are a helpful assistant that answers questions."
```

✅ Good:
```
"You are OrderBot, a pizza ordering specialist for Mario's Pizza. 
You help customers place orders, not answer general questions."
```

### 2. **Define Boundaries**

❌ Without boundaries:
```
User: "What's the weather?"
Bot: "Let me check the weather for you..." ❌ (Out of scope!)
```

✅ With boundaries:
```
"You ONLY handle pizza orders. For other questions, politely 
redirect to ordering."

User: "What's the weather?"
Bot: "I'm here to help with pizza orders! What would you like to order?"
```

### 3. **Provide Examples (When Needed)**

For complex behaviors, show examples:

```
"When a customer is vague, ask clarifying questions. For example:
- If they say 'pizza', ask which type and size
- If they say 'drink', ask which drink and size
- Always confirm before finalizing"
```

### 4. **Use Structured Data**

❌ Unstructured:
```
"We sell pepperoni pizza for twelve ninety-five, ten dollars, 
or seven dollars depending on size..."
```

✅ Structured:
```
pepperoni pizza  12.95, 10.00, 7.00
cheese pizza     10.95, 9.25, 6.50
```

### 5. **Prioritize Information**

**Order of importance:**
1. **Identity** (who you are)
2. **Purpose** (what you do)
3. **Workflow** (how you do it)
4. **Style** (how you communicate)
5. **Data** (what you know)

---

## Testing Your System Message 🧪

### Test Cases for OrderBot:

**Test 1: Identity**
```
User: "What are you?"
Expected: "I'm OrderBot, here to help you order pizza!"
```

**Test 2: Workflow**
```
User: "Hi"
Expected: Should greet and ask what they want
Not expected: Should NOT immediately ask for payment
```

**Test 3: Clarification**
```
User: "I want a pizza"
Expected: Should ask which type and size
Not expected: Should NOT assume defaults
```

**Test 4: Boundaries**
```
User: "Tell me a joke"
Expected: Redirect to ordering
Not expected: Should NOT tell jokes
```

**Test 5: Knowledge**
```
User: "How much is a large pepperoni?"
Expected: "$12.95"
Not expected: "I don't know"
```

---

## Common System Message Patterns 📝

### Pattern 1: Customer Service Bot

```python
{
    "role": "system",
    "content": """You are [Name], a [role] for [company].

Your responsibilities:
1. [Primary task]
2. [Secondary task]
3. [Tertiary task]

Guidelines:
- [Behavioral rule 1]
- [Behavioral rule 2]

Available information:
[Data/knowledge base]

Style: [Tone description]
"""
}
```

### Pattern 2: Expert Advisor

```python
{
    "role": "system",
    "content": """You are an expert in [domain].

Your expertise includes:
- [Area 1]
- [Area 2]

When answering:
1. Provide accurate, evidence-based information
2. Cite sources when possible
3. Admit uncertainty when appropriate

Style: Professional but approachable
"""
}
```

### Pattern 3: Task-Specific Assistant

```python
{
    "role": "system",
    "content": """You help users with [specific task].

Process:
1. Understand their goal
2. Ask clarifying questions
3. Provide step-by-step guidance
4. Verify completion

Constraints:
- Only help with [task], not [other things]
- Always confirm before taking action

Style: Clear, concise, supportive
"""
}
```

---

## Advanced Techniques 🚀

### 1. **Dynamic System Messages**

Change the system message based on context:

```python
def get_system_message(user_type, time_of_day):
    base = "You are OrderBot..."
    
    if user_type == "vip":
        base += "\nThis is a VIP customer. Offer premium options."
    
    if time_of_day == "lunch":
        base += "\nSuggest our lunch specials."
    
    return base
```

### 2. **Multi-Language Support**

```python
system_message_en = "You are OrderBot, a pizza ordering assistant..."
system_message_es = "Eres OrderBot, un asistente de pedidos de pizza..."

# Select based on user preference
```

### 3. **Personality Variants**

```python
# Formal
"You respond in a professional, courteous manner."

# Casual
"You respond in a friendly, casual style. Use emojis!"

# Enthusiastic
"You're super excited about pizza! Show your enthusiasm!"
```

### 4. **Context Injection**

```python
system_message = f"""You are OrderBot...

Current promotions:
{get_current_promotions()}

Out of stock items:
{get_out_of_stock()}
"""
```

---

## Measuring System Message Effectiveness 📊

### Metrics to Track:

1. **Task Completion Rate**
   - Did the bot complete the order?
   - Were all steps followed?

2. **Clarification Rate**
   - How often does the bot ask for clarification?
   - Too high = confusing, Too low = assuming

3. **Error Rate**
   - Wrong items ordered
   - Wrong prices quoted
   - Workflow steps skipped

4. **User Satisfaction**
   - Tone appropriateness
   - Response helpfulness
   - Overall experience

### A/B Testing System Messages:

```python
# Version A: Detailed workflow
system_a = "You follow these steps: 1. Greet, 2. Order..."

# Version B: Brief instructions
system_b = "You help customers order pizza. Be friendly."

# Compare:
# - Average conversation length
# - Successful orders
# - User ratings
```

---

## Common Pitfalls ⚠️

### 1. **Too Vague**
❌ "Be helpful"
✅ "Ask clarifying questions when the user is vague"

### 2. **Too Restrictive**
❌ "Only say exactly: 'Welcome. What would you like?'"
✅ "Greet warmly and ask what they'd like to order"

### 3. **Contradictory Instructions**
❌ "Be brief. Provide detailed explanations."
✅ "Be concise but thorough when explaining options"

### 4. **Missing Critical Info**
❌ Forgetting to include the menu
✅ Always include necessary data

### 5. **Assuming Context**
❌ "Handle orders" (What kind? How?)
✅ "Handle pizza orders following this workflow..."

---

## Exercises 🎓

### Exercise 1: Improve This System Message

**Original:**
```
"You help people order food. Be nice."
```

**Your improved version:**
```
[Write your improvement here]
```

<details>
<summary>Example Solution</summary>

```
"You are FoodBot, an automated ordering assistant for Tasty Bites Restaurant.

Workflow:
1. Greet the customer warmly
2. Present today's menu
3. Take their order (ask about dietary restrictions)
4. Confirm the order and total price
5. Ask for delivery or pickup
6. Collect payment information

Style: Friendly, patient, and helpful. Use emojis sparingly.

Menu:
[Include actual menu items and prices]
"
```
</details>

### Exercise 2: Design a System Message

Create a system message for a **gym membership bot** that:
- Helps users choose a membership plan
- Explains gym facilities
- Schedules a tour
- Doesn't handle cancellations (redirects to staff)

---

## Key Takeaways 🎯

1. **System messages are the foundation** of bot behavior
2. **Be specific** about identity, purpose, and workflow
3. **Include all necessary data** (menus, prices, policies)
4. **Define personality** clearly
5. **Test thoroughly** with edge cases
6. **Iterate based on** real user interactions
7. **Keep it maintainable** - document changes

---

## Further Reading 📚

- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Prompt Design](https://docs.anthropic.com/claude/docs/prompt-design)
- [Best Practices for LLM System Messages](https://www.promptingguide.ai/)

---

**Remember:** A well-crafted system message is the difference between a bot that frustrates users and one that delights them! 🌟
