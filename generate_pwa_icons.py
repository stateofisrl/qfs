"""
Generate PWA icons from teslogo.png for iOS and Android
"""
from PIL import Image
import os

# Ensure images directory exists
os.makedirs('static/images', exist_ok=True)

# Load the original logo
logo = Image.open('static/teslogo.png')

# Icon sizes needed for iOS and Android
sizes = [72, 96, 128, 144, 152, 180, 192, 384, 512]

for size in sizes:
    # Resize the logo maintaining aspect ratio
    resized = logo.resize((size, size), Image.Resampling.LANCZOS)
    
    # Save the icon
    filename = f'static/images/icon-{size}x{size}.png'
    resized.save(filename, 'PNG')
    print(f'✅ Created {filename}')

print('\n✅ All PWA icons generated from teslogo.png successfully!')
