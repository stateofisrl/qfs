#!/usr/bin/env python3
import os
import re

# Color mapping from dark to light theme
dark_to_light = {
    'bg-black': 'bg-white',
    'bg-gray-900': 'bg-white',
    'bg-gray-800': 'bg-white',
    'bg-gray-700': 'bg-gray-100',
    'text-white': 'text-gray-900',
    'text-gray-300': 'text-gray-700',
    'text-gray-400': 'text-gray-600',
    'text-gray-500': 'text-gray-700',
    'border-gray-800': 'border-gray-300',
    'border-gray-700': 'border-gray-300',
    'focus:ring-white': 'focus:ring-blue-600',
    'hover:bg-gray-800': 'hover:bg-gray-100',
    'hover:bg-gray-700': 'hover:bg-gray-100',
    'hover:bg-gray-200': 'hover:bg-blue-700',
    'hover:text-white': 'hover:text-gray-900',
    'hover:text-gray-300': 'hover:text-gray-900',
    'divide-gray-700': 'divide-gray-300',
    'divide-gray-800': 'divide-gray-300',
    'bg-green-900': 'bg-green-100',
    'text-green-400': 'text-green-800',
    'text-green-200': 'text-green-800',
    'bg-red-900': 'bg-red-100',
    'text-red-400': 'text-red-800',
    'text-red-200': 'text-red-800',
    'border-green-800': 'border-green-400',
    'border-red-800': 'border-red-400',
    'bg-yellow-900': 'bg-yellow-100',
    'text-yellow-400': 'text-yellow-800',
    'text-yellow-200': 'text-yellow-800',
    'border-yellow-800': 'border-yellow-400',
    'bg-blue-900': 'bg-blue-100',
    'text-blue-400': 'text-blue-800',
    'bg-white text-black': 'bg-blue-600 text-white',
    'bg-white hover:bg-gray-200 text-black': 'bg-blue-600 hover:bg-blue-700 text-white',
}

templates_dir = 'templates'

for filename in os.listdir(templates_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(templates_dir, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply replacements
        for dark, light in dark_to_light.items():
            content = content.replace(dark, light)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {filename}")

print("Theme conversion complete!")
