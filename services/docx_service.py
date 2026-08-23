from docx import Document

def extract_docx_text(docx_path):

    doc = Document(docx_path)

    text = []

    for para in doc.paragraphs:
        text.append(para.text)

    return "\n".join(text)