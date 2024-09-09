import io
from flask import Flask, request, render_template
import PyPDF2
import fitz
from pdfminer.high_level import extract_text_to_fp
from anonymization import anonymize
from detection import analyze

app = Flask(__name__)

# def extract_text_from_pdf(file):
#     reader = PyPDF2.PdfReader(file)
#     text = ""
#     for page_num in range(len(reader.pages)):
#         text += reader.pages[page_num].extract_text()
#     return text

# def extract_text_from_pdf(file):
#     output_string = io.StringIO()
#     extract_text_to_fp(file.stream, output_string)
#     text = output_string.getvalue()
#     output_string.close()
#     return text

def extract_text_from_pdf(file):
    # Read the PDF file into a PyMuPDF document
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    # Extract text from each page
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        entities = request.form.getlist('entities')
        
        if file and entities:
            text = extract_text_from_pdf(file)
            analyzer_results = analyze(text, entities)
            anonymized_text = anonymize(text, analyzer_results)
            
            detected_details = []
            for result in analyzer_results:
                original_text = text[result.start:result.end]
                detected_details.append({
                    'entity_type': result.entity_type,
                    'start': result.start,
                    'end': result.end,
                    'score': result.score,
                    'original_text': original_text
                })
            
            return render_template('result.html', original_text=text, anonymized_text=anonymized_text, detected_details=detected_details)

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
