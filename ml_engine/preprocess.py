import os
from utils.pdf_extractor import extract_text_from_pdf
from utils.text_cleaner import clean_text

def process_resume(pdf_path):
    print("📄 Reading PDF:", pdf_path)

    raw_text = extract_text_from_pdf(pdf_path)
    print("📝 Raw text length:", len(raw_text))

    if len(raw_text.strip()) == 0:
        print("❌ No text extracted from PDF")
        return ""

    clean_resume = clean_text(raw_text)
    print("✅ Cleaned text length:", len(clean_resume))

    return clean_resume


if __name__ == "__main__":
    sample_pdf = "datasets/resume_pdfs/sample_resume.pdf"

    if not os.path.exists(sample_pdf):
        print("❌ PDF file not found:", sample_pdf)
    else:
        processed_text = process_resume(sample_pdf)
        print("\n===== FINAL CLEANED OUTPUT =====\n")
        print(processed_text[:500])
