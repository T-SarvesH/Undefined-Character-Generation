
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.conf import settings
import os
import json
import requests
import logging
from django.core.files import File
from .models import fontFiles

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Directories
GOOGLE_FONTS_JSON = "google_fonts.json"
DOWNLOAD_DIR = "Font Files"

# Ensure download directory exists
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# ======================== FONT DOWNLOAD FUNCTIONS ======================== #

def fetch_google_fonts(api_key, sort_by="popularity", subset=None, family=None, capability=None):
    base_url = "https://www.googleapis.com/webfonts/v1/webfonts"
    params = {"key": api_key, "sort": sort_by}

    if subset:
        params["subset"] = subset
    if family:
        params["family"] = family
    if capability:
        params["capability"] = capability

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json().get("items", [])
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching fonts: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
        return None

def save_fonts_to_json(font_data, filename=GOOGLE_FONTS_JSON):
    if font_data:
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(font_data, f, ensure_ascii=False, indent=4)
            logger.info(f"Font data saved to {filename}")
        except IOError as e:
            logger.error(f"Error saving font data: {e}")
    else:
        logger.warning("No font data to save.")

def load_fonts_from_json(filename=GOOGLE_FONTS_JSON):
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            logger.error(f"Error loading font data: {e}")
            return None
    else:
        logger.warning(f"File {filename} does not exist.")
        return None

def download_fonts(font_data):
    """Download Google and Ubuntu fonts, ensuring no duplicates"""
    new_fonts = []  # Collect font instances for bulk creation

    # Download Google Fonts
    if font_data:
        for font in font_data:
            family_name = font["family"].replace(" ", "_")

            if "files" in font:
                for weight, ttf_url in font["files"].items():
                    try:
                        filename = f"{family_name}-{weight}.ttf"
                        file_path = os.path.join(DOWNLOAD_DIR, filename)

                        if fontFiles.objects.filter(file=f"font_files/{filename}").exists():
                            logger.info(f"Skipping duplicate: {filename}")
                            continue

                        response = requests.get(ttf_url)
                        response.raise_for_status()

                        with open(file_path, "wb") as f:
                            f.write(response.content)
                        logger.info(f"Downloaded: {filename}")

                        with open(file_path, "rb") as f:
                            new_fonts.append(fontFiles(file=File(f, name=filename)))

                    except requests.exceptions.RequestException as e:
                        logger.error(f"Error downloading {family_name} {weight}: {e}")
                    except IOError as file_error:
                        logger.error(f"File writing error for {family_name} {weight}: {file_error}")

    # Download Ubuntu Fonts
    ubuntu_font_dir = "/usr/share/fonts"
    for dirpath, dirnames, filenames in os.walk(ubuntu_font_dir):
        for filename in filenames:
            if filename.lower().endswith((".ttf", ".otf", ".ttc")):
                full_path = os.path.join(dirpath, filename)
                dest_path = os.path.join(DOWNLOAD_DIR, filename)

                if fontFiles.objects.filter(file=f"font_files/{filename}").exists():
                    logger.info(f"Skipping duplicate: {filename}")
                    continue

                try:
                    with open(full_path, 'rb') as src, open(dest_path, 'wb') as dst:
                        dst.write(src.read())
                    logger.info(f"Copied: {filename}")

                    with open(dest_path, "rb") as f:
                        new_fonts.append(fontFiles(file=File(f, name=filename)))

                except IOError as e:
                    logger.error(f"Error copying {filename}: {e}")

    # Bulk insert for performance improvement
    if new_fonts:
        fontFiles.objects.bulk_create(new_fonts)
        logger.info(f"Added {len(new_fonts)} fonts to the database.")

# ======================== MAIN EXECUTION ======================== #

API_KEY = "YOUR_GOOGLE_FONTS_API_KEY"

# Load Google Fonts data from JSON or API
fonts = load_fonts_from_json()

if fonts is None:
    fonts = fetch_google_fonts(API_KEY, sort_by="popularity")
    save_fonts_to_json(fonts)

# Download fonts and add them to the database
if fonts:
    download_fonts(fonts)
    logger.info("All fonts successfully downloaded and added to the database.")
else:
    logger.warning("No Google Fonts data found or available.")

def ffupload(request):
    if request.method == "POST":
        API_KEY = settings.GOOGLE_FONTS_API_KEY
        fonts = fetch_google_fonts(API_KEY)

        if fonts:
            download_fonts(fonts)
            return JsonResponse({"status": "success", "message": "Fonts uploaded successfully!"})

        return JsonResponse({"status": "error", "message": "Failed to download fonts."})

    return JsonResponse({"status": "error", "message": "Invalid request method."})