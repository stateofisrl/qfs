"""
Fix for Django 6.0 + DRF converter issue
Run this before starting the server
"""
from django.urls import converters

# Check if converter is already registered and unregister it
if 'drf_format_suffix' in converters.get_converters():
    converters.unregister_converter('drf_format_suffix')
    print("✓ Unregistered drf_format_suffix converter")
