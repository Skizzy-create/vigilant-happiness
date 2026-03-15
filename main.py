import os
from dotenv import load_dotenv
from google import genai
import argparse
from call_function import avaliable_functions, call_function
from google.genai import types
from prompts import system_prompt
from config import AGNET_LOOP_LIMIT
import sys


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not configured")

    parser = argparse.ArgumentParser(description="Gemini-3.1-flash-lite Bot")

    parser.add_argument(
        "user_prompt",
        type=str,
        nargs="?",
        help="User prompt, the question you want to ask",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output. \nSend's the usage_metadata as well",
    )

    args = parser.parse_args()

    client = genai.Client(api_key=api_key)

    call_Gemini(client, user_prompt=args.user_prompt, isVerbose=args.verbose)


def call_Gemini(client, user_prompt, isVerbose=False):
    if user_prompt == None:
        user_prompt = """Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."""

    messages = [
        genai.types.Content(role="user", parts=[genai.types.Part(text=user_prompt)])
    ]

    for _ in range(AGNET_LOOP_LIMIT):
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0,
                tools=[avaliable_functions],
                thinking_config=types.ThinkingConfig(thinking_budget=0),
            ),
        )

        if not response.usage_metadata:
            raise RuntimeError("Gemini Response Error")

        for candidate in response.candidates:
            messages.append(candidate.content)

        function_results = call_tools(response, user_prompt, isVerbose)

        if function_results is None:
            return

        messages.append(types.Content(role="user", parts=function_results))

    print("Error: max iterations reached without a final response:", AGNET_LOOP_LIMIT)
    sys.exit(1)


def call_tools(response, user_prompt, isVerbose):

    if not response.usage_metadata:
        raise RuntimeError("Gemini Response Error")

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if isVerbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    if not response.function_calls:
        print(f"Response:\n{response.text}")
        return None  # signals the loop to stop

    function_result = []

    if response.function_calls:
        for fc in response.function_calls:
            function_call_result = call_function(fc, verbose=isVerbose)

            if not function_call_result.parts:
                raise RuntimeError("Function call returned empty parts")

            fr = function_call_result.parts[0].function_response

            if fr is None:
                raise RuntimeError(f"Function response is None for {fc.name}")

            if fr.response is None:
                raise RuntimeError(f"No response in function response for {fc.name}")

            function_result.append(function_call_result.parts[0])

            if isVerbose:
                # fix 2: use a different variable name, not `response`
                tool_resp = function_call_result.parts[0].function_response.response
                result_str = tool_resp.get("result") or tool_resp.get("error", "")
                print(f"-> {result_str}")
    return function_result


if __name__ == "__main__":
    main()
