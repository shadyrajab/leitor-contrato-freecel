import re

import pandas as pd

from utils.variables import INDEX_COLUMNS


def read_dataframes():
    simulacao = pd.read_excel("output/simulação.xlsx")
    composicao = pd.read_excel("output/descrição da composição.xlsx")
    termo = pd.read_excel("output/termo complementar.xlsx")
    visao = pd.read_excel("output/visão.xlsx")

    return simulacao, composicao, termo, visao


def merge_termo_composicao(composicao: pd.DataFrame, termo: pd.DataFrame):
    termo_composicao = pd.merge(termo, composicao, how="right", on="Comp.")
    termo_composicao.loc[:, "Nº da Linha"] = termo_composicao[
        "Nº da Linha"
    ].str.replace("-", "")
    termo_composicao.loc[:, "Telefone"] = (
        termo_composicao["DDD_x"].astype(str) + termo_composicao["Nº da Linha"]
    )

    return termo_composicao


def get_flags(m: int, recomendacao: int, recomendacaoup: int, plano: int, delta: float):
    if m < 7:
        return "Não Remunerado"

    elif (m >= 7 and m <= 17) and (recomendacaoup >= plano):
        return "Positiva"

    if m >= 17:
        if delta > 0:
            return "Positiva"
        elif delta == 0:
            return "Padrão"
        elif delta < 0:
            if plano >= recomendacaoup:
                return "Positiva"
            elif plano >= recomendacao:
                return "Padrão"

    return "Padrão"


def merge_dataframes(simulacao, composicao, termo, visao):
    regex = r"\b\d{1,4}GB\b"
    termo_composicao = merge_termo_composicao(composicao, termo)

    visao["Telefone"] = visao["Telefone"].astype(str)
    final = pd.merge(visao, termo_composicao, on="Telefone", how="right")[INDEX_COLUMNS]
    final["Fat Atual"] = simulacao["Fat Atual"][0]
    final["Fat Simulação"] = simulacao["Fat Simulação"][0]
    final["delta"] = simulacao["delta"][0]

    for column in ["Plano e Vlr. Unit.", "Recomendação", "Recomendação UP"]:
        final[column] = final[column].apply(
            lambda x: re.search(regex, x).group(0).replace("GB", "")
        )

    final["Remuneração"] = final.apply(
        lambda row: get_flags(
            row["M"],
            row["Recomendação"],
            row["Recomendação UP"],
            row["Plano e Vlr. Unit."],
            row["delta"],
        ),
        axis=1,
    )

    final.rename(columns={"DDD_x": "DDD"}).to_excel("output/final.xlsx", index=False)
