import os
from utils.pdf_extractor import extract_text_from_pdf
from utils.text_cleaner import clean_text

def process_resume(pdf_path):
    raw_text = extract_text_from_pdf(pdf_path)
    clean_resume = clean_text(raw_text)
    return clean_resume


if __name__ == "__main__":
    sample_pdf = "datasets/resume_pdfs/sample_resume.pdf"
    if os.path.exists(sample_pdf):
        processed_text = process_resume(sample_pdf)
        print(processed_text[:500])
    else:
        print("Sample resume PDF not found")
