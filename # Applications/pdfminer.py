import sys
from pdfminer.pdfparser import PDFParser, PDFDocument, PDFPage
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed, PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams

fp = open('ICCV.pdf','rb')
parser = PDFParser(fp)
document = PDFDocument(parser)
def parse_pdf(path):
    fp = open('ICCV.pdf', 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)

    doc.initialize()

    if not doc.is_extractable():
        raise PDFTextExtractionNotAllowed
    else:
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageInterpreter(rsrcmgr, laparams = laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        for page in doc.get_pages():
            interpreter.process_page(page)
            layout = device.get_result()
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    with open(r'test.txt','a') as f:
                        results = x.get_text()
                        print(results)
                        f.write(results + '\n')
parse_pdf('ICCV.pdf')



