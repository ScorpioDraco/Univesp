#////////////////////////////////////////////////#
# Desenvolvido por Carlos Eduardo Sakamoto       #
# cesakamoto@gmail.com                           #
# Download de PDFs da Biblioteca Virtual Univesp #
# Para uso pessoal apenas!                       #
#////////////////////////////////////////////////#

import urllib.request
import img2pdf
import PyPDF2
import sys
import os
import shutil
import time
from PIL import Image

if len(sys.argv) < 3 or len(sys.argv) > 4:
    print('Devem ser informados três argumentos: código do livro, página inicial e página final.')
    exit()

TMP_DIR = r'C:\tmp'
OUTPUT_DIR = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
URL_BASE = 'https://staticbv.am4.com.br/publicacoes'
BOOK = sys.argv[1]
F_PAGE = sys.argv[2]
# For two args, L_PAGE = F_PAGE
if len(sys.argv) == 4:
    L_PAGE = sys.argv[3]
else:
    L_PAGE = sys.argv[2]

def downloadPages(urlBase, book, fPage, lPage):
    print('Solicitando o download...')

    for page in range(int(fPage), int(lPage) + 1):
        # Exemplo de URL: https://staticbv.am4.com.br/publicacoes/2223/p_524.jpg
        url = urlBase + '/' + book + '/p_' + str(page) + '.jpg'
        imageFileName = book + '-p_' + str(page).zfill(3) + '.jpg'

        # File download
        urllib.request.urlretrieve(url, imageFileName)

        # PDF convertion
        pdfFileName = book + '-p_' + str(page).zfill(3) + '.pdf'
        image = Image.open(imageFileName)
        # Convert into chunks
        pdfBytes = img2pdf.convert(image.filename)
        # Open or creat pdf file
        file = open(pdfFileName, "wb")
        # Write pdf files with chunks
        file.write(pdfBytes)
        image.close()
        file.close()
        # Remove image file
        os.remove(imageFileName)

        print(f'Página {page} concluída.')

def mergePDF(book, fPage, lPage):
    # Get all the PDF filenames
    pdf2merge = []
    for fileName in os.listdir():
        if fileName.startswith(book) and fileName.endswith('.pdf'):
            pdf2merge.append(fileName)

    pdfWriter = PyPDF2.PdfFileWriter()

    # Loop through all PDFs
    for fileName in pdf2merge:
        # rb for read binary
        pdfFileObj = open(fileName, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        # Opening each page of the PDF
        for pageNum in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(pageNum)
            pdfWriter.addPage(pageObj)
    
    # Save PDF to file (wb for write binary)
    pdfOutput = open(OUTPUT_DIR + '\\' + BOOK + '-' + fPage + '_' + lPage + '.pdf', 'wb')
    pdfWriter.write(pdfOutput)
    pdfOutput.close()
    return True

def main():
    if not os.path.exists(TMP_DIR):
        os.mkdir(TMP_DIR)
    else:
        shutil.rmtree(TMP_DIR)
        os.mkdir(TMP_DIR)

    os.chdir(TMP_DIR)
    downloadPages(URL_BASE, BOOK, F_PAGE, L_PAGE)
    mergePDF(BOOK, F_PAGE, L_PAGE)
    print('\n\nProcesso concluído.\nArquivo salvo na Área de Trabalho.')
    time.sleep(5)

main()
