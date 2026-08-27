import os
from PIL import Image

# Load source image
source_image = "icons/ispeaklogo.png"

# Icon sizes required for Web, PWA, and Mobile
SIZES = {
    "favicon-16x16.png": (16, 16),
    "favicon-32x32.png": (32, 32),
    "apple-touch-icon.png": (180, 180),
    "icon-192x192.png": (192, 192),
    "icon-512x512.png": (512, 512),
}

output_dir = "icons"
os.makedirs(output_dir, exist_ok=True)

try:
    with Image.open(source_image) as img:
        # Convert to RGBA to preserve transparency
        img = img.convert("RGBA")
        
        # Generate PNG icons
        for name, size in SIZES.items():
            resized = img.resize(size, Image.Resampling.LANCZOS)
            resized.save(os.path.join(output_dir, name))
            print(f"Generated: {name} ({size[0]}x{size[1]})")

        # Generate root favicon.ico
        img.save("favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
        print("Generated: favicon.ico")

except FileNotFoundError:
    print(f"Error: Could not find '{source_image}'. Make sure it exists in this directory.")