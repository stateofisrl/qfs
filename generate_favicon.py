"""
Generate favicon PNG files from existing icons for iOS compatibility
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Ensure directories exist
os.makedirs('static/images', exist_ok=True)

# Light blue Q on white background
background_color = (255, 255, 255)  # White background
logo_color = (135, 206, 250)  # Light blue Q

# Create favicon sizes with letter "Q"
def create_favicon(size, filename):
    img = Image.new('RGB', (size, size), background_color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a nice font, fallback to default
    try:
        # Use Arial Bold or fallback to default
        font_size = int(size * 0.7)
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # Use default font for small sizes
        font = ImageFont.load_default()
    
    # Draw letter "Q" centered
    text = "Q"
    
    # For better centering, calculate text bbox
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size - text_width) // 2 - bbox[0]
        y = (size - text_height) // 2 - bbox[1]
        draw.text((x, y), text, fill=logo_color, font=font)
    except:
        # Fallback for older PIL versions
        draw.text((size // 4, size // 8), text, fill=logo_color, font=font)
    
    img.save(filename, 'PNG')
    print(f'✅ Created {filename}')
    return img

# Generate standard favicon sizes
favicon_16 = create_favicon(16, 'static/favicon-16x16.png')
favicon_32 = create_favicon(32, 'static/favicon-32x32.png')
favicon_48 = create_favicon(48, 'static/favicon-48x48.png')

# Generate iOS/PWA icon sizes (reusing or creating)
create_favicon(180, 'static/images/icon-180x180.png')
create_favicon(192, 'static/images/icon-192x192.png')
create_favicon(512, 'static/images/icon-512x512.png')

# Create multi-resolution favicon.ico
print('\n✅ Creating favicon.ico with multiple resolutions...')
favicon_16.save(
    'static/favicon.ico',
    format='ICO',
    sizes=[(16, 16), (32, 32), (48, 48)]
)
print('✅ Created static/favicon.ico')

print('\n✅ All favicon files generated successfully!')
