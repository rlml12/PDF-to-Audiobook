import asyncio
import os
import re
from tkinter import Tk, filedialog
import edge_tts
import pymupdf

def clean_pdf_text(pdf_path):
    doc = pymupdf.open(pdf_path)
    full_text = ""
    
    for page in doc:
        full_text += page.get_text() + "\n"
        
    full_text = re.sub(r'([a-zA-ZçğıöşüÇĞİÖŞÜ]+)\s*[-‐­–]\s*\n*\s*([a-zA-ZçğıöşüÇĞİÖŞÜ]+)', r'\1\2', full_text)
    
    ocr_corrections = {
        "1l ": "",
        "]oe": "Joe",
        " '": "'"
    }
    for wrong, correct in ocr_corrections.items():
        full_text = full_text.replace(wrong, correct)
    
    full_text = re.sub(r'(?<![.!?:”"])\n(?!\n)', ' ', full_text)
    full_text = re.sub(r' +', ' ', full_text)
    
    return full_text.strip()

async def text_to_speech(text, output_file):
    # VOICE MODELS (Uncomment the one you want to use):
    # voice = "tr-TR-AhmetNeural"               # Turkish male voice
    voice = "en-US-AndrewMultilingualNeural"    # Multilingual male voice (warm/documentary tone)
    # voice = "en-US-AriaNeural"                # English female voice
    
    # SPEED AND PITCH SETTINGS:
    # rate="+15%" -> Reads 15% faster than default
    # pitch="-6Hz" -> Lowers the pitch slightly for a deeper tone
    communicate = edge_tts.Communicate(text, voice, rate="+15%", pitch="-6Hz")
    
    print(f"🎙️ Creating audiobook ({voice} | Rate: +15% | Pitch: -6Hz)...")
    print("⏳ Please wait (this may take 1-2 minutes)...")
    await communicate.save(output_file)
    print(f"✅ Done! Your audio file is ready:\n👉 {output_file}")

if __name__ == "__main__":
    folder_path = os.path.dirname(os.path.abspath(__file__))
    default_pdf = os.path.join(folder_path, "sample.pdf")
    
    if not os.path.exists(default_pdf):
        print("📂 Default PDF not found. Please select a PDF file from the dialog...")
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        pdf_file = filedialog.askopenfilename(
            title="Select PDF File to Read",
            filetypes=[("PDF Files", "*.pdf")]
        )
    else:
        pdf_file = default_pdf
        
    if not pdf_file:
        print("❌ No file selected. Operation cancelled.")
    else:
        base_name = os.path.splitext(os.path.basename(pdf_file))[0]
        mp3_file = os.path.join(folder_path, f"{base_name}_audiobook.mp3")
        
        print(f"📄 Reading and cleaning '{os.path.basename(pdf_file)}'...")
        cleaned_text = clean_pdf_text(pdf_file)
        
        print("\n--- PREVIEW ---\n" + cleaned_text[:300] + "...\n-----------------\n")
        
        asyncio.run(text_to_speech(cleaned_text, mp3_file))