from PyPDF2 import PdfReader

import tabula
from handler.handler_dataframe import handler_composicao, handler_termo, handler_visao
from utils.functions import found_page

reader = PdfReader("input/contrato.pdf")
termo, found_page = found_page(reader)


composicao = tabula.read_pdf("input/contrato.pdf", pages=found_page, lattice=True)[0]
visao = tabula.read_pdf("input/visão.pdf", pages="2")[0]

handler_composicao(composicao)
handler_termo(termo)
handler_visao(visao)
