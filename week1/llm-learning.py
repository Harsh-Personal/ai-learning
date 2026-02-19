import os
import time
from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "help me become an ai evaluation engineer as an SDET",
#         }
#     ],
#     model="llama-3.3-70b-versatile",
# )

# print(chat_completion.choices[0].message.content)


def ask_llm(prompt, temperature, times):
    all_messages = []
    for i in range(times):
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=temperature,
        )
        all_messages.append(response.choices[0].message.content)
        time.sleep(2)
    return all_messages


print(ask_llm("explain how testing is done in AI", 1, 10))
