import pandas as pd

from utils.functions import remove_rbar
from utils.variables import COMPOSICAO_COLUMNS, TERMO_COLUMNS


def handler_termo(extracted_text: str):
    termo_complementar = [
        item for item in extracted_text.split("\n")[11:-7] if item not in TERMO_COLUMNS
    ]

    sublistas = []

    for i in range(0, len(termo_complementar), 4):
        sublista = termo_complementar[i : i + 4]
        sublistas.append(sublista)

    dataframe = pd.DataFrame(sublistas, columns=TERMO_COLUMNS)
    dataframe.to_excel("termo complementar.xlsx", index=False)


def handler_composicao(dataframe: pd.DataFrame):
    dataframe = dataframe.iloc[2:, 0:26]

    if dataframe["Unnamed: 14"].isnull().any():
        dataframe["Unnamed: 14"] = "Não Informado"

    dataframe.dropna(axis=1, inplace=True)
    dataframe.columns = COMPOSICAO_COLUMNS

    for column in dataframe.columns:
        dataframe[column] = dataframe[column].apply(lambda x: remove_rbar(x))

    dataframe.to_excel("descrição da composição.xlsx", index=False)
