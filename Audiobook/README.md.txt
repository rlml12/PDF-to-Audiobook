# PDF to Audiobook Converter

A simple Python script that extracts text from PDF files, cleans up common formatting/OCR errors, and converts them into MP3 audiobooks using Edge TTS.

## Installation

Make sure you have Python installed, then install the required libraries:

```bash
pip install edge-tts pymupdf

Usage
Simply run the script from your terminal:

python main.py

A window will pop up asking you to select a PDF file. Once you select it, the script will clean the text and generate an MP3 audiobook in the same folder.

Customization
You can easily open the Python file and edit the voice, rate, and pitch variables to change the narrator's voice or reading speed.