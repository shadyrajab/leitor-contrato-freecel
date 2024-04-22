from PyPDF2 import PdfReader

import tabula
from handler.handler_dataframe import (
    handler_composicao,
    handler_faturamento,
    handler_termo,
    handler_visao,
)
from handler.merge_dataframes import merge_dataframes, read_dataframes
from utils.functions import found_page

reader = PdfReader("input/contrato.pdf")
termo, found_page = found_page(reader)


composicao = tabula.read_pdf("input/contrato.pdf", pages=found_page, lattice=True)[0]
visao = tabula.read_pdf("input/visão.pdf", pages="2")[0]
simulacao = tabula.read_pdf("input/simulação.pdf", pages="1", lattice=True)[0]


handler_composicao(composicao)
handler_termo(termo)
handler_visao(visao)
handler_faturamento(simulacao)


simulacao, composicao, termo, visao = read_dataframes()
merge_dataframes(simulacao, composicao, termo, visao)
