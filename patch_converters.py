"""
Monkey patch for Django 6.0 / DRF format suffix converter issue
This must be imported before Django URLs are loaded
"""
import django.urls.converters as converters_module

original_register = converters_module.register_converter

def patched_register_converter(converter, type_name=""):
    """Register converter but don't raise error if already registered"""
    try:
        original_register(converter, type_name)
    except ValueError as e:
        if "already registered" in str(e):
            # Silently ignore duplicate registration
            pass
        else:
            raise

# Apply the patch
converters_module.register_converter = patched_register_converter
