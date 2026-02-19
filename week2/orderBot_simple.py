"""
OrderBot - Simple Pizza Ordering Chatbot
"""

import os
from groq import Groq
import panel as pn

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
pn.extension()

context = [{
    "role": "system",
    "content": """You are OrderBot, an automated service to collect orders for a pizza restaurant. \
You first greet the customer, then collects the order, \
and then asks if it's a pickup or delivery. \
You wait to collect the entire order, then summarize it and check for a final \
time if the customer wants to add anything else. \
If it's a delivery, you ask for an address. \
Finally you collect the payment.\
Make sure to clarify all options, extras and sizes to uniquely \
identify the item from the menu.\
You respond in a short, very conversational friendly style. \
IMPORTANT: Be very careful with price calculations. Double-check all math before stating prices.

The menu includes \
pepperoni pizza: large $12.95, medium $10.00, small $7.00 \
cheese pizza: large $10.95, medium $9.25, small $6.50 \
eggplant pizza: large $11.95, medium $9.75, small $6.75 \
fries: large $4.50, small $3.50 \
greek salad: $7.25 \
Toppings: \
extra cheese $2.00, \
mushrooms $1.50, \
sausage $3.00, \
canadian bacon $3.50, \
AI sauce $1.50, \
peppers $1.00 \
Drinks: \
coke: large $3.00, medium $2.00, small $1.00 \
sprite: large $3.00, medium $2.00, small $1.00 \
bottled water: $5.00

For cheese pizza specifically:
- Medium is $2.75 more than small ($9.25 - $6.50)
- Large is $1.70 more than medium ($10.95 - $9.25)
- Large is $4.45 more than small ($10.95 - $6.50)"""
}]

# Chat display area
chat_log = pn.Column()
chat_log.append(pn.pane.Markdown("**🤖 OrderBot:** Hi! Welcome to our pizza place. What can I get for you today?"))

# Use TextAreaInput which has better Enter key support
text_input = pn.widgets.TextAreaInput(
    placeholder="Type and press Ctrl+Enter to send...", 
    rows=3,
    width=400,
    auto_grow=False
)
send_btn = pn.widgets.Button(name="Send", button_type="primary", width=100)

def send_message(event=None):
    """Handle message sending"""
    user_msg = text_input.value.strip()
    if not user_msg:
        return
    
    text_input.value = ""
    chat_log.append(pn.pane.Markdown(f"**👤 You:** {user_msg}"))
    
    context.append({"role": "user", "content": user_msg})
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=context,
            temperature=0
        )
        bot_msg = response.choices[0].message.content
        context.append({"role": "assistant", "content": bot_msg})
        chat_log.append(pn.pane.Markdown(f"**🤖 OrderBot:** {bot_msg}"))
    except Exception as e:
        chat_log.append(pn.pane.Markdown(f"**❌ Error:** {str(e)}"))

send_btn.on_click(send_message)

pn.template.FastListTemplate(
    title="🍕 OrderBot",
    main=[
        pn.Card(chat_log, title="Chat", height=600, scroll=True),
        pn.Row(text_input, send_btn)
    ]
).servable()
