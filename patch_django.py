#!/usr/bin/env python
"""
Properly patch Django's Context class for Python 3.14 compatibility.
"""
import os
import sys

try:
    import django.template.context
    import inspect
    
    source_file = inspect.getfile(django.template.context)
    print(f'Patching global Django: {source_file}')
    
    with open(source_file, 'r') as f:
        content = f.read()
    
    # Try the current broken pattern first
    old_code = '''    def __copy__(self):
        duplicate = object.__new__(self.__class__)
        duplicate.dicts = self.dicts[:]
        return duplicate'''
    
    new_code = '''    def __copy__(self):
        duplicate = object.__new__(self.__class__)
        duplicate.dicts = self.dicts[:]
        # Copy all instance attributes from self to duplicate
        duplicate.__dict__.update(self.__dict__)
        return duplicate'''
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        with open(source_file, 'w') as f:
            f.write(content)
        print('✓ Global Django patched successfully (fixed)!')
    else:
        print('✗ Current pattern not found - trying original pattern...')
        # Try the original broken pattern
        old_code2 = '''    def __copy__(self):
        duplicate = copy(super())
        duplicate.dicts = self.dicts[:]
        return duplicate'''
        
        if old_code2 in content:
            content = content.replace(old_code2, new_code)
            with open(source_file, 'w') as f:
                f.write(content)
            print('✓ Global Django patched successfully (from original)!')
        else:
            print('✗ Neither pattern found')
except Exception as e:
    print(f'Error patching global Django: {e}')

print("\nNow restart the server with: python manage.py runserver 8001")
