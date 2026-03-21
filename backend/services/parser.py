import PyPDF2
import io

def parse_resume(file):
    return extract_text_from_pdf(file)

def parse_jd(file):
    filename = file.filename.lower()
    if filename.endswith('.pdf'):
        return extract_text_from_pdf(file)
    else:
        return file.read().decode('utf-8')
def extract_text_from_pdf(file):
    text = ""
    file.seek(0)
    reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted
        print("EXTRACTED TEXT:",text[:500])
        return text