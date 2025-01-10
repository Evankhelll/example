import json
import numpy as np
from django.http import JsonResponse
from django.conf import settings
import os
from .models import gambar
from sklearn.cluster import KMeans
import colorsys

# bagian claude.ai
def rgb_to_wavelength(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    wavelength = 380 + (h * 320)
    return round(wavelength, 6)

def wavelength_to_energy(wavelength_nm):
    """
    Menghitung energi foton dari panjang gelombang.
    Args:
        wavelength_nm: panjang gelombang dalam nanometer
    Returns:
        energy dalam elektronvolt (eV)
    """
    # Konstanta
    h = 6.626e-34  # Konstanta Planck dalam J⋅s
    c = 2.998e8    # Kecepatan cahaya dalam m/s
    e = 1.602e-19  # Muatan elektron dalam Coulomb (untuk konversi ke eV)
    
    # Konversi wavelength dari nm ke m
    wavelength_m = wavelength_nm * 1e-9
    
    # Hitung energi dalam Joule
    energy_j = (h * c) / wavelength_m
    
    # Konversi ke eV
    energy_ev = energy_j / e
    
    return round(energy_ev, 6)

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
    kmeans = KMeans(n_clusters=200, random_state=42)  # Detect 100 dominant colors
    kmeans.fit(pixels)
    
    # Get dominant colors and their percentages
    colors = kmeans.cluster_centers_
    labels = kmeans.labels_
    total_pixels = len(labels)
    
    # Track unique combinations
    seen_combinations = set()
    colors_data = []
    
    for i, color in enumerate(colors):
        percentage = (np.sum(labels == i) / total_pixels) * 100
        
        # Convert color to integer RGB values
        rgb = tuple(int(round(x)) for x in color)
        hex_code = '#{:02x}{:02x}{:02x}'.format(*rgb)
        
        # Calculate wavelength
        wavelength = round(rgb_to_wavelength(*rgb), 2)
        
        # Calculate energy
        energy = round(wavelength_to_energy(wavelength), 2)
        
        # Skip if the combination of hex_code, wavelength, and energy is already seen
        combination = (wavelength, energy)
        if combination in seen_combinations:
            continue
        
        # Add the combination to the seen set
        seen_combinations.add(combination)
        
        # Build the color data
        color_info = {
            "hex_code": hex_code,
            "wavelength": {
                "value": wavelength,
                "energy": energy,
                "energy_unit": "eV",
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