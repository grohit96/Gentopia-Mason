import PyPDF2
import requests
from io import BytesIO
from gentopia.tools.basetool import BaseTool

class PDFReader(BaseTool):
    name = "pdf_reader"
    description = "Tool to read a PDF from a URL or local file and extract text."

    def _run(self, **kwargs) -> str:
        return self._process_pdf(kwargs.get('__arg1', ''))

    async def _arun(self, **kwargs) -> str:
        return self._process_pdf(kwargs.get('__arg1', ''))

    def _process_pdf(self, pdf_source: str) -> str:
        if not pdf_source:
            return "Error: No file path or URL provided."
        
        try:
            pdf_file = self._get_pdf_file(pdf_source)
            reader = PyPDF2.PdfReader(pdf_file)
            return ''.join(page.extract_text() or '' for page in reader.pages).strip() or "No text found in the PDF."
        except Exception as e:
            return str(e)

    def _get_pdf_file(self, pdf_source: str):
        if pdf_source.startswith('http'):
            response = requests.get(pdf_source)
            response.raise_for_status()
            return BytesIO(response.content)
        return open(pdf_source, 'rb')
