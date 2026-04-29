#!/usr/bin/env python3
import sys

# Check modules before any imports
print("Modules in sys.modules that contain 'openai' or 'anthropic':")
for key in sys.modules:
    if 'openai' in key.lower() or 'anthropic' in key.lower():
        print(f"  {key}: {sys.modules[key]}")

print("\nNow testing imports...")

# Import tokeneyes first
import tokeneyes
tokeneyes.auto_track()

# Now try imports
print("\nAfter auto_track(), trying imports...")

from openai import OpenAI
print(f"OpenAI: {OpenAI}, module: {OpenAI.__module__}")

from anthropic import Anthropic
print(f"Anthropic: {Anthropic}, module: {Anthropic.__module__}")
