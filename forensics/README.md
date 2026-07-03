# Digital Forensics Tools

This project contains tools to assist with Digital Forensics and Incident Response (DFIR) tasks. When analyzing a compromised machine or a suspicious file, building timelines and extracting hidden metadata are essential first steps.

## Included Tools

1. **`metadata_extractor.py`**: Extracts the MAC (Modified, Accessed, Created) times of any file. If the file is an image, it also extracts hidden EXIF metadata (which can contain GPS coordinates, camera models, and software used).
2. **`timeline_builder.py`**: Recursively scans a target directory and generates a chronological CSV timeline of every file's creation, modification, and access events.

## Prerequisites

For extracting EXIF data from images, you need the `Pillow` library:

```bash
pip install Pillow
```

## Usage

### 1. Extract File Metadata

Run the extractor against any file. If it's a JPEG or PNG, EXIF data will also be processed.

```bash
python metadata_extractor.py C:\Users\Public\Downloads\suspicious_image.jpg
```

### 2. Build a Forensic Timeline

To figure out exactly what happened on a system and when, you can build a timeline of file activity in a specific folder (like an infected web server directory or a user's Downloads folder).

```bash
python timeline_builder.py C:\Path\To\Scan -o timeline_output.csv
```

This will output a `timeline_output.csv` file. You can open this in Excel or a specialized tool like Eric Zimmerman's Timeline Explorer to trace the exact order in which files were dropped, modified, and executed.
