"""
Example: Using Tokeneyes SDK Wrapper with Anthropic Claude

This example shows how to use Tokeneyes as a drop-in replacement for the Anthropic SDK.
Just change the import statement - everything else stays the same!
"""

import os

# ✨ BEFORE: from anthropic import Anthropic
# ✨ AFTER:  from tokeneyes.sdk import Anthropic

from tokeneyes.sdk import Anthropic


def main():
    # Initialize client (same as official SDK)
    client = Anthropic(
        api_key=os.getenv('ANTHROPIC_API_KEY')
    )

    print("🤖 Making API call to Claude...")
    print()

    # Make API call (exactly the same as official SDK)
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=100,
        messages=[
            {
                "role": "user",
                "content": "What is Tokeneyes in one sentence?"
            }
        ]
    )

    # Access response (exactly the same)
    message = response.content[0].text
    print(f"Response: {message}")
    print()

    # Token usage is available as normal
    if response.usage:
        print(f"Token Usage:")
        print(f"  Input: {response.usage.input_tokens}")
        print(f"  Output: {response.usage.output_tokens}")

        # Anthropic-specific: prompt caching
        if hasattr(response.usage, 'cache_read_input_tokens'):
            cache_read = response.usage.cache_read_input_tokens or 0
            if cache_read > 0:
                print(f"  Cache read: {cache_read}")

        print()

    # ✅ Bonus: Token usage is automatically tracked!
    print("✅ Token usage automatically tracked to ~/.aitracker/sdk_events.jsonl")
    print()
    print("View tracked usage with: tokeneyes stats")


if __name__ == '__main__':
    # Check if API key is set
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("❌ Please set ANTHROPIC_API_KEY environment variable")
        print("   export ANTHROPIC_API_KEY=sk-ant-...")
        exit(1)

    main()
