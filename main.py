import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_function import available_functions, call_function

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("GEMINI_API_KEY not found in .env file. Please set it.")

parser = argparse.ArgumentParser(description="AI Agent CLI powered by Gemini")
parser.add_argument("user_prompt", type=str, help="The task or prompt to send to the agent")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

client = genai.Client(api_key=api_key)

messages = [
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
]

MAX_ITERATIONS = 20

for iteration in range(MAX_ITERATIONS):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions],
            temperature=0
        )
    )

    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    if response.usage_metadata is None:
        raise RuntimeError("Failed to get usage metadata from the API response.")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.function_calls:
        function_responses = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose=args.verbose)
            if not function_call_result.parts:
                raise RuntimeError("Function call result has no parts")
            if function_call_result.parts[0].function_response is None:
                raise RuntimeError("Function response is None")
            if function_call_result.parts[0].function_response.response is None:
                raise RuntimeError("Function response response is None")
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            function_responses.append(function_call_result.parts[0])
        if function_responses:
            messages.append(types.Content(role="user", parts=function_responses))
    else:
        print(response.text)
        sys.exit(0)

print("Maximum iterations reached without a final response.")
sys.exit(1)
