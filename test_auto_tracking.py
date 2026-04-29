#!/usr/bin/env python3
"""
Test that automatic SDK tracking works after tokeneyes init
"""

print("Testing automatic SDK tracking...")
print()

# This should be automatically wrapped because sitecustomize.py is installed!
try:
    from openai import OpenAI
    print("✅ Imported OpenAI")
    print(f"   OpenAI class: {OpenAI}")
    print(f"   Module: {OpenAI.__module__}")

    # Check if it's our wrapper
    if 'tokeneyes' in OpenAI.__module__:
        print("   ✅ This is the Tokeneyes wrapper! (automatic tracking enabled)")
    else:
        print("   ⚠️  This is the original OpenAI SDK (tracking NOT enabled)")

except ImportError as e:
    print(f"⚠️  OpenAI not installed: {e}")

print()

try:
    from anthropic import Anthropic
    print("✅ Imported Anthropic")
    print(f"   Anthropic class: {Anthropic}")
    print(f"   Module: {Anthropic.__module__}")

    # Check if it's our wrapper
    if 'tokeneyes' in Anthropic.__module__:
        print("   ✅ This is the Tokeneyes wrapper! (automatic tracking enabled)")
    else:
        print("   ⚠️  This is the original Anthropic SDK (tracking NOT enabled)")

except ImportError as e:
    print(f"⚠️  Anthropic not installed: {e}")

print()
print("=" * 60)

# Check if auto_track marker exists
from pathlib import Path
marker = Path.home() / '.aitracker' / 'auto_track'
if marker.exists():
    print("✅ Auto-track marker exists:", marker)
    print("   Automatic SDK tracking is ENABLED")
else:
    print("⚠️  Auto-track marker not found")
    print("   Run: tokeneyes init --setup-sdk-wrappers")
