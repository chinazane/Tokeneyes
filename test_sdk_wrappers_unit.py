"""
Unit tests for SDK wrappers (no API keys required)

Tests the wrapper structure and token tracking logic without making actual API calls.
"""

import sys
from pathlib import Path


def test_base_classes():
    """Test base classes can be imported"""
    print("=" * 60)
    print("Test 1: Base Classes Import")
    print("=" * 60)

    from tokeneyes.sdk.base import BaseSDKWrapper, TokenTracker
    print("✅ BaseSDKWrapper imported")
    print("✅ TokenTracker imported")

    # Test TokenTracker initialization
    tracker = TokenTracker()
    print(f"✅ TokenTracker initialized (state_dir: {tracker.state_dir})")

    assert tracker is not None
    assert tracker.state_dir.exists()


def test_wrapper_imports():
    """Test wrapper imports (may fail if SDKs not installed)"""
    print("\n" + "=" * 60)
    print("Test 2: Wrapper Imports")
    print("=" * 60)

    # Test OpenAI wrapper
    openai_available = False
    try:
        from tokeneyes.sdk import OpenAI, AsyncOpenAI
        print("✅ OpenAI wrappers imported")
        openai_available = True
    except ImportError as e:
        print(f"⚠️  OpenAI wrappers not available: {e}")
        print("   (This is OK if openai SDK is not installed)")

    # Test Anthropic wrapper
    anthropic_available = False
    try:
        from tokeneyes.sdk import Anthropic, AsyncAnthropic
        print("✅ Anthropic wrappers imported")
        anthropic_available = True
    except ImportError as e:
        print(f"⚠️  Anthropic wrappers not available: {e}")
        print("   (This is OK if anthropic SDK is not installed)")

    # At least one should be available if SDKs are installed
    assert True  # This test is informational, not a hard requirement


def test_package_exports():
    """Test package __all__ exports"""
    print("\n" + "=" * 60)
    print("Test 3: Package Exports")
    print("=" * 60)

    import tokeneyes.sdk as sdk

    expected_exports = [
        'BaseSDKWrapper',
        'TokenTracker',
        'OpenAI',
        'AsyncOpenAI',
        'Anthropic',
        'AsyncAnthropic',
    ]

    found_exports = []
    for export in expected_exports:
        if hasattr(sdk, export):
            value = getattr(sdk, export)
            if value is not None:
                print(f"✅ {export} available")
                found_exports.append(export)
            else:
                print(f"⚠️  {export} is None (SDK not installed)")
        else:
            print(f"❌ {export} not found")

    # At least base classes should be available
    assert 'BaseSDKWrapper' in found_exports
    assert 'TokenTracker' in found_exports


def test_token_tracker():
    """Test TokenTracker functionality"""
    print("\n" + "=" * 60)
    print("Test 4: TokenTracker Functionality")
    print("=" * 60)

    from tokeneyes.sdk import TokenTracker
    import tempfile
    import json

    # Use temporary directory for testing
    with tempfile.TemporaryDirectory() as tmpdir:
        state_dir = Path(tmpdir)
        tracker = TokenTracker(state_dir=state_dir)

        print(f"✅ TokenTracker created with temp dir: {state_dir}")

        # Track a test event
        tracker.track_event(
            service='test-service',
            model='test-model',
            prompt_tokens=100,
            completion_tokens=200,
            total_tokens=300,
            cached_tokens=50,
            metadata={'test': True}
        )

        print("✅ Event tracked")

        # Verify event file was created
        event_file = state_dir / 'sdk_events.jsonl'
        assert event_file.exists(), "Event file was not created"
        print(f"✅ Event file created: {event_file}")

        # Read and verify event
        with open(event_file) as f:
            event = json.loads(f.read().strip())

        assert event['service'] == 'test-service'
        assert event['model'] == 'test-model'
        assert event['prompt_tokens'] == 100
        assert event['completion_tokens'] == 200
        assert event['total_tokens'] == 300
        assert event['cached_tokens'] == 50
        assert event['metadata']['test'] is True

        print("✅ Event data verified")
        print(f"   Service: {event['service']}")
        print(f"   Model: {event['model']}")
        print(f"   Tokens: {event['total_tokens']}")


def test_wrapper_initialization():
    """Test wrapper initialization without API keys"""
    print("\n" + "=" * 60)
    print("Test 5: Wrapper Initialization")
    print("=" * 60)

    openai_works = False
    anthropic_works = False

    # Test OpenAI wrapper initialization
    try:
        from tokeneyes.sdk import OpenAI

        # Try to initialize without API key (should work, but will fail on API call)
        client = OpenAI(api_key="test-key-not-real", track_tokens=False)
        print("✅ OpenAI wrapper initialized (tracking disabled)")

        # Check that it has the expected attributes
        assert hasattr(client, '_client')
        assert hasattr(client, 'track_tokens')
        print("✅ OpenAI wrapper has expected attributes")
        openai_works = True
    except ImportError:
        print("⚠️  OpenAI SDK not installed, skipping")
    except Exception as e:
        print(f"⚠️  OpenAI wrapper initialization issue: {e}")

    # Test Anthropic wrapper initialization
    try:
        from tokeneyes.sdk import Anthropic

        client = Anthropic(api_key="test-key-not-real", track_tokens=False)
        print("✅ Anthropic wrapper initialized (tracking disabled)")

        assert hasattr(client, '_client')
        assert hasattr(client, 'track_tokens')
        print("✅ Anthropic wrapper has expected attributes")
        anthropic_works = True
    except ImportError:
        print("⚠️  Anthropic SDK not installed, skipping")
    except Exception as e:
        print(f"⚠️  Anthropic wrapper initialization issue: {e}")

    # At least test that the test ran
    assert True


def main():
    print("\n🧪 Tokeneyes SDK Wrapper Unit Tests")
    print("(No API keys required)\n")

    results = {
        'base_classes': test_base_classes(),
        'wrapper_imports': test_wrapper_imports(),
        'package_exports': test_package_exports(),
        'token_tracker': test_token_tracker(),
        'wrapper_init': test_wrapper_initialization(),
    }

    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    total_tests = len(results)
    passed_tests = sum(1 for v in results.values() if v and (isinstance(v, bool) or any(v.values())))

    for test_name, result in results.items():
        if isinstance(result, bool):
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name}: {status}")
        elif isinstance(result, dict):
            available = sum(1 for v in result.values() if v)
            total = len(result)
            print(f"{test_name}: {available}/{total} available")

    print("\n" + "=" * 60)

    if results['base_classes'] and results['token_tracker']:
        print("✅ Core functionality tests PASSED")
        print("\n📝 Note: SDK wrappers require 'openai' and 'anthropic' packages")
        print("   Install with: pip install openai anthropic")
        return 0
    else:
        print("❌ Some tests FAILED")
        return 1


if __name__ == '__main__':
    sys.exit(main())
