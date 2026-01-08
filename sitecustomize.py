"""
Site-wide customizations that run before any imports.
This patches Django URLconverter registration to handle duplicate registrations.
"""
import sys

def patch_django_converters():
    """Patch Django converter registration before it's used"""
    try:
        import django.urls.converters as converters_module
        
        # Only patch once
        if hasattr(converters_module.register_converter, '_is_patched'):
            return
            
        original_register = converters_module.register_converter
        
        def patched_register_converter(converter, type_name=""):
            """Silently ignore duplicate converter registrations"""
            try:
                original_register(converter, type_name)
            except ValueError as e:
                if "already registered" in str(e):
                    # Ignore duplicate registration
                    pass
                else:
                    raise
        
        patched_register_converter._is_patched = True
        converters_module.register_converter = patched_register_converter
    except Exception:
        pass

# Apply the patch immediately when this module is imported
patch_django_converters()
