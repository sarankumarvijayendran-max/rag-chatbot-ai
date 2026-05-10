import pandas as pd
from PyPDF2 import PdfReader


# --------------------------------------------------
# PDF TEXT EXTRACTION
# --------------------------------------------------

def extract_text_from_pdf(path):

    reader = PdfReader(path)

    text = ""

    for page in reader.pages:

        text += page.extract_text() or ""

    return text


# --------------------------------------------------
# EXCEL TEXT EXTRACTION
# --------------------------------------------------

def extract_text_from_excel(path):

    excel_data = pd.read_excel(
        path,
        sheet_name=None
    )

    combined_text = ""

    for sheet_name, df in excel_data.items():

        combined_text += (
            f"\n\nSheet Name: {sheet_name}\n"
        )

        combined_text += df.to_string(
            index=False
        )

    return combined_text