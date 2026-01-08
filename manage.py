#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# Patch Django converter registration BEFORE Django is imported
def _patch_converters():
    try:
        import django.urls.converters as conv
        if hasattr(conv, '_patched'):
            return
        _orig = conv.register_converter
        def _new_reg(converter, type_name=""):
            try:
                _orig(converter, type_name)
            except ValueError as e:
                if "already registered" not in str(e):
                    raise
        conv.register_converter = _new_reg
        conv._patched = True
    except:
        pass

_patch_converters()


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
