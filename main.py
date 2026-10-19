import os
from dotenv import load_dotenv
from groq import Groq
from tools import TOOL_MAP , TOOLS_SCHEMA

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print("API key found:", GROQ_API_KEY is not None)
# Groq client banao
client = Groq(api_key=GROQ_API_KEY)
messages = [
    {"role": "user", "content": "Tell me my server CPU capacity?"}
]

try:
    response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=messages,
    tools=TOOLS_SCHEMA,       # <-- Tools array yahan pass hota hai
    tool_choice="auto"
)
    message = response.choices[0].message
    while True:

        if message.tool_calls:

            tool_call = message.tool_calls[0]

            function_name = tool_call.function.name
  
            print("Function requested:", function_name)
            function_to_call = TOOL_MAP[function_name]

            result = function_to_call()

            print("Function result:", result)
            messages.append(response.choices[0].message)

        else:
            print("Grok:", message.content)

        messages.append({
           "role": "tool",
           "tool_call_id": tool_call.id,
           "content": result
       })


        final_response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        tools=TOOLS_SCHEMA
        )

        print("Final Response:")
        print(final_response.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")






