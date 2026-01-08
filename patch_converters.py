"""
Monkey patch for Django 6.0 / DRF format suffix converter issue
This must be imported before Django URLs are loaded
"""
try:
    import django.urls.converters as converters_module

    # Store original if not already patched
    if not hasattr(converters_module, '_original_register_converter'):
        converters_module._original_register_converter = converters_module.register_converter

        def patched_register_converter(converter, type_name=""):
            """Register converter but don't raise error if already registered"""
            try:
                converters_module._original_register_converter(converter, type_name)
            except ValueError as e:
                if "already registered" in str(e):
                    # Silently ignore duplicate registration
                    pass
                else:
                    raise

        # Apply the patch
        converters_module.register_converter = patched_register_converter
except Exception:
    pass
