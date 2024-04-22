from PyPDF2 import PdfReader

import tabula
from handler.handler_dataframe import handler_composicao, handler_termo

reader = PdfReader("contrato.pdf")
for i, page in enumerate(reader.pages):
    if (
        "7\n.\nAnexo II\nTermo Complementar \nRelação de Terminais da Negociação"
        in page.extract_text()
    ):
        termo_complementar = page.extract_text()

    if ("\nUnit.\nServiço Vlr. Unit.\n") in page.extract_text():
        composicao_page = i + 1


composicao = tabula.read_pdf("contrato.pdf", pages=composicao_page, lattice=True)[0]


handler_composicao(composicao)
handler_termo(termo_complementar)
