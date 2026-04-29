"""
Example: Using Tokeneyes SDK Wrapper with OpenAI

This example shows how to use Tokeneyes as a drop-in replacement for the OpenAI SDK.
Just change the import statement - everything else stays the same!
"""

import os

# ✨ BEFORE: from openai import OpenAI
# ✨ AFTER:  from tokeneyes.sdk import OpenAI

from tokeneyes.sdk import OpenAI


def main():
    # Initialize client (same as official SDK)
    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY')
    )

    print("🤖 Making API call to OpenAI...")
    print()

    # Make API call (exactly the same as official SDK)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that explains things concisely."
            },
            {
                "role": "user",
                "content": "What is Tokeneyes in one sentence?"
            }
        ],
        max_tokens=100
    )

    # Access response (exactly the same)
    message = response.choices[0].message.content
    print(f"Response: {message}")
    print()

    # Token usage is available as normal
    if response.usage:
        print(f"Token Usage:")
        print(f"  Prompt: {response.usage.prompt_tokens}")
        print(f"  Completion: {response.usage.completion_tokens}")
        print(f"  Total: {response.usage.total_tokens}")
        print()

    # ✅ Bonus: Token usage is automatically tracked!
    print("✅ Token usage automatically tracked to ~/.aitracker/sdk_events.jsonl")
    print()
    print("View tracked usage with: tokeneyes stats")


if __name__ == '__main__':
    # Check if API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Please set OPENAI_API_KEY environment variable")
        print("   export OPENAI_API_KEY=sk-...")
        exit(1)

    main()
