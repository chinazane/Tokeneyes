"""
Tokeneyes SDK Tracking - Automatic Setup Guide

The daemon can't automatically intercept SDK calls in other processes.
This guide explains the options for automatic tracking.
"""

# OPTION 1: User Changes Import (Current - Simplest)
# ====================================================
# User changes one line in their code:

from tokeneyes.sdk import OpenAI  # Instead of: from openai import OpenAI

client = OpenAI(api_key="...")
# ✅ Automatic tracking!


# OPTION 2: Environment + sitecustomize.py (Fully Automatic)
# ===========================================================
# One-time setup (per environment):

# 1. Create ~/.python/sitecustomize.py:
cat > ~/.python/sitecustomize.py << 'EOF'
import os
if os.getenv('TOKENEYES_TRACK'):
    try:
        from tokeneyes.sdk.autopatch import install_import_hooks
        install_import_hooks()
    except ImportError:
        pass
EOF

# 2. Set environment variable:
export TOKENEYES_TRACK=1

# 3. Run app normally:
python myapp.py  # ✅ Automatic tracking!


# OPTION 3: CLI Wrapper (No Code Changes)
# ========================================
# Run app with tokeneyes wrapper:

tokeneyes exec python myapp.py  # ✅ Automatic tracking!


# OPTION 4: Library Initialization (Programmatic)
# ================================================
# Add to your app's __init__.py or main.py:

import tokeneyes
tokeneyes.auto_track()  # Installs import hooks

# Then all subsequent imports are tracked:
from openai import OpenAI  # ✅ Automatically wrapped!
