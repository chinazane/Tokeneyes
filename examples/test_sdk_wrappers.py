"""
Test script for SDK wrappers

Tests that SDK wrappers work as drop-in replacements and track tokens correctly.

NOTE: These are example tests. To run them, you need:
1. Valid API keys in environment variables
2. The respective SDKs installed (openai, anthropic)

Run with:
    python examples/test_sdk_wrappers.py
"""

import os
from pathlib import Path


def test_openai_wrapper():
    """Test OpenAI SDK wrapper"""
    print("=" * 60)
    print("Testing OpenAI SDK Wrapper")
    print("=" * 60)

    try:
        from tokeneyes.sdk import OpenAI

        # Initialize client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("⚠️  OPENAI_API_KEY not set, skipping OpenAI test")
            return

        client = OpenAI(api_key=api_key)

        # Make a simple API call
        print("\n🔄 Making API call to GPT-3.5 Turbo...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Say 'Hello from Tokeneyes!' in exactly 5 words."}
            ],
            max_tokens=20
        )

        # Display response
        message = response.choices[0].message.content
        print(f"✅ Response: {message}")

        # Display usage
        if response.usage:
            print(f"\n📊 Token Usage:")
            print(f"   Prompt tokens: {response.usage.prompt_tokens}")
            print(f"   Completion tokens: {response.usage.completion_tokens}")
            print(f"   Total tokens: {response.usage.total_tokens}")

        # Check if event was tracked
        event_file = Path.home() / '.aitracker' / 'sdk_events.jsonl'
        if event_file.exists():
            with open(event_file) as f:
                lines = f.readlines()
            print(f"\n✅ Token usage tracked! ({len(lines)} total events in file)")
            print(f"   Event file: {event_file}")
        else:
            print(f"\n⚠️  Event file not found at {event_file}")

    except ImportError as e:
        print(f"⚠️  OpenAI SDK not installed: {e}")
        print("   Install with: pip install openai")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_anthropic_wrapper():
    """Test Anthropic SDK wrapper"""
    print("\n\n" + "=" * 60)
    print("Testing Anthropic SDK Wrapper")
    print("=" * 60)

    try:
        from tokeneyes.sdk import Anthropic

        # Initialize client
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            print("⚠️  ANTHROPIC_API_KEY not set, skipping Anthropic test")
            return

        client = Anthropic(api_key=api_key)

        # Make a simple API call
        print("\n🔄 Making API call to Claude 3 Haiku...")
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=20,
            messages=[
                {"role": "user", "content": "Say 'Hello from Tokeneyes!' in exactly 5 words."}
            ]
        )

        # Display response
        message = response.content[0].text
        print(f"✅ Response: {message}")

        # Display usage
        if response.usage:
            print(f"\n📊 Token Usage:")
            print(f"   Input tokens: {response.usage.input_tokens}")
            print(f"   Output tokens: {response.usage.output_tokens}")
            if hasattr(response.usage, 'cache_read_input_tokens'):
                print(f"   Cache read tokens: {response.usage.cache_read_input_tokens}")

        # Check if event was tracked
        event_file = Path.home() / '.aitracker' / 'sdk_events.jsonl'
        if event_file.exists():
            with open(event_file) as f:
                lines = f.readlines()
            print(f"\n✅ Token usage tracked! ({len(lines)} total events in file)")
            print(f"   Event file: {event_file}")
        else:
            print(f"\n⚠️  Event file not found at {event_file}")

    except ImportError as e:
        print(f"⚠️  Anthropic SDK not installed: {e}")
        print("   Install with: pip install anthropic")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_tracking_disabled():
    """Test that tracking can be disabled"""
    print("\n\n" + "=" * 60)
    print("Testing Tracking Disabled")
    print("=" * 60)

    try:
        from tokeneyes.sdk import OpenAI

        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("⚠️  OPENAI_API_KEY not set, skipping test")
            return

        # Create client with tracking disabled
        client = OpenAI(api_key=api_key, track_tokens=False)

        print("\n🔄 Making API call with tracking disabled...")

        # Get event count before
        event_file = Path.home() / '.aitracker' / 'sdk_events.jsonl'
        before_count = 0
        if event_file.exists():
            with open(event_file) as f:
                before_count = len(f.readlines())

        # Make API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=5
        )

        # Check event count after
        after_count = 0
        if event_file.exists():
            with open(event_file) as f:
                after_count = len(f.readlines())

        if after_count == before_count:
            print(f"✅ Tracking disabled successfully (event count unchanged: {after_count})")
        else:
            print(f"⚠️  Event count changed: {before_count} → {after_count}")

    except ImportError:
        print("⚠️  OpenAI SDK not installed")
    except Exception as e:
        print(f"❌ Error: {e}")


def display_tracked_events():
    """Display all tracked events"""
    print("\n\n" + "=" * 60)
    print("Tracked Events Summary")
    print("=" * 60)

    event_file = Path.home() / '.aitracker' / 'sdk_events.jsonl'

    if not event_file.exists():
        print("No events tracked yet")
        return

    import json

    events_by_service = {}

    with open(event_file) as f:
        for line in f:
            if not line.strip():
                continue

            try:
                event = json.loads(line)
                service = event.get('service', 'unknown')

                if service not in events_by_service:
                    events_by_service[service] = {
                        'count': 0,
                        'total_tokens': 0
                    }

                events_by_service[service]['count'] += 1
                events_by_service[service]['total_tokens'] += event.get('total_tokens', 0)

            except json.JSONDecodeError:
                continue

    print(f"\n📊 Events tracked: {sum(s['count'] for s in events_by_service.values())}")
    print(f"📁 Event file: {event_file}\n")

    for service, stats in events_by_service.items():
        print(f"{service}:")
        print(f"  Requests: {stats['count']}")
        print(f"  Total tokens: {stats['total_tokens']:,}")


if __name__ == '__main__':
    print("\n🔍 Tokeneyes SDK Wrapper Tests\n")

    # Run tests
    test_openai_wrapper()
    test_anthropic_wrapper()
    test_tracking_disabled()

    # Show summary
    display_tracked_events()

    print("\n\n" + "=" * 60)
    print("✅ Tests Complete")
    print("=" * 60)
    print("\nNote: These tests require:")
    print("  - OPENAI_API_KEY environment variable")
    print("  - ANTHROPIC_API_KEY environment variable")
    print("  - pip install openai anthropic")
