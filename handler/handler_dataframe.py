import re

import pandas as pd

from utils.functions import remove_rbar
from utils.variables import COMPOSICAO_COLUMNS, TERMO_COLUMNS


def handler_faturamento(dataframe: pd.DataFrame):
    df = dataframe[["Unnamed: 0", "Fat. Simulação\rigo GrupoSe"]]
    df.columns = ["Fat Atual", "Fat Simulação"]
    regex = r"R\$\s*(?:(?:\d{1,3}(?:,\d{3})*|\d+)(?:,\d{2})|\d{1,3}(?:,\d{3})*\.\d{2})"

    for column in df.columns:
        df.loc[:, column] = df[column].apply(
            lambda x: re.search(regex, x).group(0).replace("R$ ", "").replace(",", ".")
        )

    df.loc[:, "delta"] = df["Fat Simulação"].astype(float) - df["Fat Atual"].astype(float)
    df.to_excel("output/simulação.xlsx", index=False)


def handler_visao(dataframe: pd.DataFrame):
    dataframe.to_excel("output/visão.xlsx", index=False)


def handler_termo(extracted_text: str):
    termo_complementar = [
        item for item in extracted_text.split("\n")[11:-7] if item not in TERMO_COLUMNS
    ]

    sublistas = []

    for i in range(0, len(termo_complementar), 4):
        sublista = termo_complementar[i : i + 4]
        sublistas.append(sublista)

    dataframe = pd.DataFrame(sublistas, columns=TERMO_COLUMNS)
    dataframe["Comp."] = dataframe["Comp."].str.replace("000000", "")
    dataframe.to_excel("output/termo complementar.xlsx", index=False)


def handler_composicao(dataframe: pd.DataFrame):
    dataframe = dataframe.iloc[2:, 0:26]

    if dataframe["Unnamed: 14"].isnull().any():
        dataframe["Unnamed: 14"] = "Não Informado"

    dataframe.dropna(axis=1, inplace=True)
    dataframe.columns = COMPOSICAO_COLUMNS

    for column in dataframe.columns:
        dataframe[column] = dataframe[column].apply(lambda x: remove_rbar(x))

    dataframe.to_excel("output/descrição da composição.xlsx", index=False)
