"""
OrderBot - With Calculator Tool
Fixes math errors by giving the bot a calculator
"""

import os
from groq import Groq
import panel as pn
import json

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
pn.extension()

# Calculator tool definition
calculator_tool = {
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "Perform basic arithmetic calculations (add, subtract, multiply, divide)",
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "The operation to perform",
                },
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number"},
            },
            "required": ["operation", "a", "b"],
        },
    },
}


def calculate(operation, a, b):
    """Perform calculation"""
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b if b != 0 else "Error: Division by zero"
    return "Error: Unknown operation"


context = [
    {
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

IMPORTANT: When you need to calculate prices or differences, USE THE CALCULATE TOOL. Do not do mental math.

The menu includes \
pepperoni pizza  12.95, 10.00, 7.00 \
cheese pizza   10.95, 9.25, 6.50 \
eggplant pizza   11.95, 9.75, 6.75 \
fries 4.50, 3.50 \
greek salad 7.25 \
Toppings: \
extra cheese 2.00, \
mushrooms 1.50 \
sausage 3.00 \
canadian bacon 3.50 \
AI sauce 1.50 \
peppers 1.00 \
Drinks: \
coke 3.00, 2.00, 1.00 \
sprite 3.00, 2.00, 1.00 \
bottled water 5.00""",
    }
]

chat_log = pn.Column()
chat_log.append(
    pn.pane.Markdown(
        "**🤖 OrderBot:** Hi! Welcome to our pizza place. What can I get for you today?"
    )
)


def get_bot_response(messages):
    """Get response from bot, handling tool calls - returns only final text response"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=[calculator_tool],
        temperature=0,
    )

    # Print token usage to terminal
    if hasattr(response, "usage"):
        print(f"\n{'='*50}")
        print(f"TOKEN USAGE:")
        print(f"  Prompt tokens: {response.usage.prompt_tokens}")
        print(f"  Completion tokens: {response.usage.completion_tokens}")
        print(f"  Total tokens: {response.usage.total_tokens}")
        print(f"{'='*50}\n")

    message = response.choices[0].message

    # Check if bot wants to use the calculator
    if message.tool_calls:
        # Process each tool call
        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            if function_name == "calculate":
                # Convert to float in case they come as strings
                result = calculate(
                    function_args["operation"],
                    float(function_args["a"]),
                    float(function_args["b"]),
                )

                # Add tool call and result to context (but not to chat display)
                messages.append(
                    {
                        "role": "assistant",
                        "content": "",
                        "tool_calls": [tool_call.dict()],
                    }
                )
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result),
                    }
                )

        # Get final response with calculation result - this is what user sees
        final_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", messages=messages, temperature=0
        )

        # Print token usage for final response
        if hasattr(final_response, "usage"):
            print(f"\n{'='*50}")
            print(f"TOKEN USAGE (After Tool Call):")
            print(f"  Prompt tokens: {final_response.usage.prompt_tokens}")
            print(f"  Completion tokens: {final_response.usage.completion_tokens}")
            print(f"  Total tokens: {final_response.usage.total_tokens}")
            print(f"{'='*50}\n")

        return final_response.choices[0].message.content

    # No tool calls, return direct response
    return message.content if message.content else ""


def send_message(event):
    user_msg = text_input.value.strip()
    if not user_msg:
        return

    text_input.value = ""

    # Show user message (always visible)
    chat_log.append(pn.pane.Markdown(f"**👤 You:** {user_msg}"))

    # Add to context
    context.append({"role": "user", "content": user_msg})

    try:
        # Get bot response (this handles tool calls internally)
        bot_msg = get_bot_response(context)

        # Only show the final text response to user (no function calls)
        if bot_msg and bot_msg.strip():
            chat_log.append(pn.pane.Markdown(f"**🤖 OrderBot:** {bot_msg}"))
            # Add final response to context
            context.append({"role": "assistant", "content": bot_msg})
    except Exception as e:
        error_msg = str(e)
        # Show user-friendly error, not technical details
        chat_log.append(
            pn.pane.Markdown(
                f"**❌ OrderBot:** Sorry, I had trouble with that. Can you try rephrasing?"
            )
        )


text_input = pn.widgets.TextInput(placeholder="Type here and click Send...", width=400)
send_btn = pn.widgets.Button(name="Send", button_type="primary", width=100)
send_btn.on_click(send_message)

pn.template.FastListTemplate(
    title="🍕 OrderBot (with Calculator)",
    main=[
        pn.Card(chat_log, title="Chat", height=600, scroll=True),
        pn.Row(text_input, send_btn),
    ],
).servable()
