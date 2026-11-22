
import fitz


def extract_text_from_pdf(uploaded_file):
    """
    Extract text from an uploaded PDF file.
    """

    try:
        pdf_document = fitz.open(
            stream=uploaded_file.getvalue(),
            filetype="pdf"
        )

        extracted_text = ""

        for page_number, page in enumerate(pdf_document):
            extracted_text += page.get_text()
            extracted_text += "\n"

        pdf_document.close()

        if not extracted_text.strip():
            return None

        return extracted_text

    except Exception as error:
        print("PDF extraction error:", error)
        return None
