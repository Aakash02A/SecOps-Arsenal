import os
import argparse
from datetime import datetime

try:
    from PIL import Image
    from PIL.ExifTags import TAGS
    PILLOW_INSTALLED = True
except ImportError:
    PILLOW_INSTALLED = False

def extract_file_metadata(filepath):
    print(f"[*] Basic File Metadata for: {filepath}")
    try:
        stat_info = os.stat(filepath)
        print(f"  - Size: {stat_info.st_size} bytes")
        print(f"  - Created: {datetime.fromtimestamp(stat_info.st_ctime)}")
        print(f"  - Modified: {datetime.fromtimestamp(stat_info.st_mtime)}")
        print(f"  - Accessed: {datetime.fromtimestamp(stat_info.st_atime)}")
    except Exception as e:
        print(f"[-] Error retrieving basic metadata: {e}")

def extract_exif(filepath):
    if not PILLOW_INSTALLED:
        print("[-] Pillow library not installed. Cannot extract EXIF data from images.")
        print("    Run: pip install Pillow")
        return
        
    print(f"\n[*] EXIF Metadata for: {filepath}")
    try:
        image = Image.open(filepath)
        exif_data = image._getexif()
        
        if not exif_data:
            print("  - No EXIF data found.")
            return
            
        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            # Skip long binary tags like MakerNote or UserComment for cleaner output
            if tag_name in ('MakerNote', 'UserComment'):
                value = "<Binary Data Omitted>"
            print(f"  - {tag_name}: {value}")
            
    except Exception as e:
        print(f"[-] Error extracting EXIF (file might not be a supported image): {e}")

def main():
    parser = argparse.ArgumentParser(description="Forensic Metadata Extractor")
    parser.add_argument("file", help="File to extract metadata from")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"[-] File not found: {args.file}")
        return
        
    extract_file_metadata(args.file)
    
    # Try to extract EXIF if it looks like an image based on extension
    if args.file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        extract_exif(args.file)

if __name__ == "__main__":
    main()
