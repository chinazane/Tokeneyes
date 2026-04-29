"""
Auto-patch module for SDK wrappers

Installs import hooks that automatically replace OpenAI/Anthropic imports
with Tokeneyes wrappers for automatic token tracking.

This enables automatic tracking without code changes!
"""

import sys
import importlib
import importlib.util
from typing import Optional, Any


class TokeneyesImportFinder:
    """
    Import finder that intercepts AI SDK imports and redirects them
    to Tokeneyes wrappers.

    When users do:
        from openai import OpenAI

    They actually get:
        from tokeneyes.sdk.openai_wrapper import OpenAI

    This is completely transparent - their code works unchanged!
    """

    def __init__(self):
        self.redirects = {
            'openai': 'tokeneyes.sdk.openai_wrapper',
            'anthropic': 'tokeneyes.sdk.anthropic_wrapper',
        }

    def find_spec(self, fullname: str, path: Optional[Any] = None, target: Optional[Any] = None):
        """
        Called when Python tries to import a module.
        Return a ModuleSpec if we want to handle this import.
        """
        # Only intercept top-level modules
        if fullname not in self.redirects:
            return None

        # Check if our wrapper module exists
        wrapper_name = self.redirects[fullname]

        try:
            # Get the spec for our wrapper module
            spec = importlib.util.find_spec(wrapper_name)
            if spec is None:
                # Wrapper not found, let Python try the original
                return None

            # Return a spec that redirects to our wrapper
            # Create a new spec with the original name but wrapper location
            wrapper_spec = importlib.util.spec_from_loader(
                fullname,  # Name in sys.modules
                loader=_TokeneyesLoader(wrapper_name),
                origin=spec.origin
            )
            return wrapper_spec

        except (ImportError, AttributeError):
            # Wrapper import failed, let Python handle normally
            return None


class _TokeneyesLoader:
    """Loader that loads our wrapper module"""

    def __init__(self, wrapper_module_name: str):
        self.wrapper_module_name = wrapper_module_name

    def create_module(self, spec):
        """Let Python create the module normally"""
        return None  # Use default module creation

    def exec_module(self, module):
        """
        Execute the wrapper module and copy its contents to the
        module being loaded (which has the original SDK name)
        """
        # Import the wrapper module
        wrapper = importlib.import_module(self.wrapper_module_name)

        # Copy all attributes from wrapper to the target module
        for attr in dir(wrapper):
            if not attr.startswith('_'):
                setattr(module, attr, getattr(wrapper, attr))

        # Also copy important dunder attributes
        if hasattr(wrapper, '__file__'):
            module.__file__ = wrapper.__file__
        if hasattr(wrapper, '__path__'):
            module.__path__ = wrapper.__path__


def install_import_hooks():
    """
    Install import hooks to automatically track SDK usage.

    Call this when the application starts to enable automatic tracking
    of all OpenAI/Anthropic API calls.
    """
    # Check if already installed
    for finder in sys.meta_path:
        if isinstance(finder, TokeneyesImportFinder):
            # Already installed, don't add again
            return

    # Install our import finder at the beginning of the meta_path
    # This ensures it gets first chance to handle imports
    finder = TokeneyesImportFinder()
    sys.meta_path.insert(0, finder)

    print("[Tokeneyes] Import hooks installed - SDK calls will be tracked automatically")


def uninstall_import_hooks():
    """
    Remove import hooks.

    Call this to stop intercepting SDK imports.
    """
    # Remove our finder from meta_path
    sys.meta_path[:] = [
        finder for finder in sys.meta_path
        if not isinstance(finder, TokeneyesImportFinder)
    ]

    print("[Tokeneyes] Import hooks uninstalled")


def is_hook_installed() -> bool:
    """Check if import hooks are currently installed"""
    return any(isinstance(finder, TokeneyesImportFinder) for finder in sys.meta_path)
