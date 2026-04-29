"""
Example: Using tokeneyes.auto_track() for automatic SDK tracking

This example shows how to enable automatic tracking without changing
every import statement. Just call tokeneyes.auto_track() once at startup!
"""

import os

# ✨ STEP 1: Enable automatic tracking (do this FIRST!)
import tokeneyes
tokeneyes.auto_track()

# ✨ STEP 2: Now import SDKs normally - they're automatically wrapped!
from openai import OpenAI
from anthropic import Anthropic


def test_openai():
    """Test OpenAI - automatically tracked"""
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  OPENAI_API_KEY not set, skipping OpenAI")
        return

    print("🤖 Testing OpenAI (auto-tracked)...")

    # Use OpenAI normally - tracking happens automatically!
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say hello in 5 words"}],
        max_tokens=20
    )

    print(f"✅ Response: {response.choices[0].message.content}")
    print(f"✅ Tokens used: {response.usage.total_tokens}")
    print("✅ Usage automatically tracked to ~/.aitracker/sdk_events.jsonl")
    print()


def test_anthropic():
    """Test Anthropic - automatically tracked"""
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  ANTHROPIC_API_KEY not set, skipping Anthropic")
        return

    print("🤖 Testing Anthropic (auto-tracked)...")

    # Use Anthropic normally - tracking happens automatically!
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=20,
        messages=[{"role": "user", "content": "Say hello in 5 words"}]
    )

    print(f"✅ Response: {response.content[0].text}")
    print(f"✅ Tokens used: {response.usage.input_tokens + response.usage.output_tokens}")
    print("✅ Usage automatically tracked to ~/.aitracker/sdk_events.jsonl")
    print()


if __name__ == '__main__':
    print("=" * 60)
    print("Tokeneyes Auto-Track Example")
    print("=" * 60)
    print()
    print("✨ Called tokeneyes.auto_track() at startup")
    print("✨ All SDK imports are now automatically wrapped!")
    print()

    test_openai()
    test_anthropic()

    print("=" * 60)
    print("✅ All API calls tracked automatically!")
    print()
    print("View tracked usage with: tokeneyes stats")
    print("=" * 60)
