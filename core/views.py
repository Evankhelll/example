import json
import webcolors
from PIL import Image
import numpy as np
from django.http import JsonResponse
from django.conf import settings
import os
import math
from .models import gambar
from PIL import Image
from sklearn.cluster import KMeans
import colorsys
from scipy.spatial import KDTree
from webcolors import hex_to_rgb


# Predefined set of web color names with their RGB values
KNOWN_COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "gray": (128, 128, 128),
}

# Map color names to their approximate visible light wavelengths (in nm)
COLOR_WAVELENGTHS = {
    "violet": (380, 450),
    "blue": (450, 495),
    "cyan": (495, 520),
    "green": (520, 560),
    "yellow": (560, 590),
    "orange": (590, 620),
    "red": (620, 750),
}

def rgb_to_hex(rgb):
    """Convert an RGB tuple to a hex color code."""
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

def classify_color_tone(rgb):
    """Classify the color tone as 'warm' or 'cool' based on the RGB values."""
    r, g, b = rgb
    if r > 100 and g > 100 and b < 100:
        return 'warm'  # Predominantly red or yellow
    elif b > 100 and r < 100 and g < 100:
        return 'cool'  # Predominantly blue
    else:
        return 'neutral'  # Other cases (e.g., greenish or neutral)

def closest_color(rgb):
    """Return the closest web color name for the given RGB using Euclidean distance."""
    min_dist = float('inf')
    closest_color_name = None
    for name, color_rgb in KNOWN_COLORS.items():
        # Calculate the Euclidean distance between the two colors
        dist = math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(rgb, color_rgb)))
        if dist < min_dist:
            min_dist = dist
            closest_color_name = name
    return closest_color_name

def get_wavelength(color_name):
    """Get the wavelength range for a color name."""
    return COLOR_WAVELENGTHS.get(color_name, None)

def get_all_colors(image_path):
    """Get all unique colors in the image."""
    # Open the image
    img = Image.open(image_path)

    # Convert image to RGB (just in case it's not already)
    img = img.convert('RGB')

    # Resize the image to speed up the process (optional, remove this line if not needed)
    img = img.resize((img.width // 5, img.height // 5))

    # Convert image to numpy array
    img_data = np.array(img)

    # Reshape the image data to a list of RGB values (flatten the image)
    img_data = img_data.reshape((-1, 3))

    # Get unique colors (this removes duplicate colors)
    unique_colors = np.unique(img_data, axis=0)

    # Convert unique RGB colors to hex
    hex_colors = [rgb_to_hex(tuple(color)) for color in unique_colors]

    # Convert numpy int64 to Python native int for JSON serialization
    unique_colors = unique_colors.astype(int).tolist()  # Ensure it's in a list of Python ints

    return unique_colors, hex_colors

def get_colors_as_json(request, id):

    gambar_instance = gambar.objects.get(id=id)

    # Image path and name
    image_name = gambar_instance.gambar.name
    image_path = os.path.join(settings.MEDIA_ROOT, image_name)  # Correct path
    
    # Get unique colors and hex values
    unique_colors, hex_colors = get_all_colors(image_path)

    # Classify colors into categories (warm, cool, neutral) and get their names
    color_data = []
    seen_colors = set()  # Set to keep track of unique colors

    for color, hex_code in zip(unique_colors, hex_colors):
        # Convert RGB color to a tuple and check if it's already in the set
        color_tuple = tuple(color)
        
        if color_tuple not in seen_colors:
            color_name = closest_color(color)  # Use the closest color name instead of direct matching
            if color_name:  # Only include colors that have a name
                color_tone = classify_color_tone(color)
                wavelength = get_wavelength(color_name)
                if wavelength:  # Only include colors with known wavelengths
                    color_data.append({
                        "color": color,
                        "hex": hex_code,
                        "tone": color_tone,
                        "name": color_name,
                        "wavelength_nm": wavelength
                    })
                    seen_colors.add(color_tuple)  # Add the color to the set of seen colors

    # Return the result as a JSON response, including the image name
    return JsonResponse({
        "name": gambar_instance.nama_gambar,
        "keterangan": gambar_instance.keterangan,
        "image_path": gambar_instance.gambar.url,
        "unique_colors": color_data
    })

CSS3_NAMES_TO_HEX = {
    'black': '#000000',
    'silver': '#c0c0c0',
    'gray': '#808080',
    'white': '#ffffff',
    'maroon': '#800000',
    'red': '#ff0000',
    'purple': '#800080',
    'fuchsia': '#ff00ff',
    'green': '#008000',
    'lime': '#00ff00',
    'olive': '#808000',
    'yellow': '#ffff00',
    'navy': '#000080',
    'blue': '#0000ff',
    'teal': '#008080',
    'aqua': '#00ffff',
    # Add other colors as needed
}

# bagian claude.ai
def get_color_name(rgb_tuple):
    # Use the manually defined mappings
    rgb_values = []
    names = []

    for color_name, hex_value in CSS3_NAMES_TO_HEX.items():
        rgb_value = hex_to_rgb(hex_value)
        rgb_values.append(rgb_value)
        names.append(color_name)

    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(rgb_tuple)
    return names[index]

def rgb_to_wavelength(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    wavelength = 380 + (h * 320)
    return round(wavelength, 2)

def get_colors_as_json2(request, id):
    gambar_instance = gambar.objects.get(id=id)
    
    # Image path and name
    image_name = gambar_instance.gambar.name
    image_path = os.path.join(settings.MEDIA_ROOT, image_name)
    
    # Open the image and convert to RGB
    img = Image.open(image_path).convert('RGB')
    
    # Convert the image to a numpy array and reshape
    img_array = np.array(img)
    pixels = img_array.reshape(-1, 3)
    
    # Use KMeans to detect dominant colors
    kmeans = KMeans(n_clusters=50, random_state=42)  # Detect 10 dominant colors
    kmeans.fit(pixels)
    
    # Get dominant colors and their percentages
    colors = kmeans.cluster_centers_
    labels = kmeans.labels_
    total_pixels = len(labels)
    
    # Track seen hex codes
    seen_hex_codes = set()
    colors_data = []
    
    for i, color in enumerate(colors):
        percentage = (np.sum(labels == i) / total_pixels) * 100
        
        # Convert color to integer RGB values
        rgb = tuple(int(x) for x in color)
        hex_code = '#{:02x}{:02x}{:02x}'.format(*rgb)
        
        # Skip if the hex code is already seen
        if hex_code in seen_hex_codes:
            continue
        
        # Add the hex code to the seen set
        seen_hex_codes.add(hex_code)
        
        # Build the color data
        color_info = {
            "hex_code": hex_code,
            "wavelength": {
                "value": rgb_to_wavelength(*rgb),
                "unit": "nm"
            },
            "percentage": round(percentage, 2)
        }
        colors_data.append(color_info)
    
    # Sort by highest percentage
    colors_data.sort(key=lambda x: x['percentage'], reverse=True)
    
    return JsonResponse({
        "name": gambar_instance.nama_gambar,
        "keterangan": gambar_instance.keterangan,
        "image_path": gambar_instance.gambar.url,
        "unique_colors": colors_data
    })
