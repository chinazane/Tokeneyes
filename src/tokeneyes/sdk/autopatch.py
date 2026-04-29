"""
Auto-patch module for SDK wrappers

When the daemon starts, it installs import hooks that automatically
replace OpenAI/Anthropic imports with Tokeneyes wrappers.

This enables automatic tracking without code changes!
"""

import sys
import importlib
from typing import Optional, Any


class TokeneyesImportHook:
    """
    Import hook that intercepts AI SDK imports and replaces them
    with Tokeneyes wrappers for automatic token tracking.

    When users do:
        from openai import OpenAI

    They actually get:
        from tokeneyes.sdk import OpenAI

    This is completely transparent - their code works unchanged!
    """

    def __init__(self):
        self.redirects = {
            'openai': 'tokeneyes.sdk.openai_wrapper',
            'anthropic': 'tokeneyes.sdk.anthropic_wrapper',
        }

    def find_module(self, fullname: str, path: Optional[Any] = None):
        """
        Called when Python tries to import a module.
        Return self if we want to handle this import.
        """
        # Check if this is a module we want to intercept
        if fullname in self.redirects:
            return self

        # Not our concern - let Python handle it normally
        return None

    def load_module(self, fullname: str):
        """
        Called to actually load the module.
        We return our wrapper instead of the original SDK.
        """
        if fullname not in self.redirects:
            # Shouldn't happen, but just in case
            return importlib.import_module(fullname)

        # Return our wrapper module
        wrapper_module = self.redirects[fullname]

        try:
            # Import our wrapper
            module = importlib.import_module(wrapper_module)

            # Register it in sys.modules so future imports use our wrapper
            sys.modules[fullname] = module

            return module

        except ImportError as e:
            # If our wrapper can't be imported (SDK not installed),
            # fall back to trying the original
            try:
                return importlib.import_module(fullname)
            except ImportError:
                # Neither wrapper nor original available
                raise ImportError(
                    f"Neither {fullname} nor tokeneyes wrapper available. "
                    f"Install with: pip install {fullname}"
                )


def install_import_hooks():
    """
    Install import hooks to automatically track SDK usage.

    Call this when the daemon starts to enable automatic tracking
    of all OpenAI/Anthropic API calls system-wide.
    """
    # Check if already installed
    for hook in sys.meta_path:
        if isinstance(hook, TokeneyesImportHook):
            # Already installed, don't add again
            return

    # Install our import hook at the beginning of the meta_path
    # This ensures it gets first chance to handle imports
    hook = TokeneyesImportHook()
    sys.meta_path.insert(0, hook)

    print("[Tokeneyes] Import hooks installed - SDK calls will be tracked automatically")


def uninstall_import_hooks():
    """
    Remove import hooks.

    Call this when the daemon stops to clean up.
    """
    # Remove our hook from meta_path
    sys.meta_path[:] = [
        hook for hook in sys.meta_path
        if not isinstance(hook, TokeneyesImportHook)
    ]

    print("[Tokeneyes] Import hooks uninstalled")


def is_hook_installed() -> bool:
    """Check if import hooks are currently installed"""
    return any(isinstance(hook, TokeneyesImportHook) for hook in sys.meta_path)
