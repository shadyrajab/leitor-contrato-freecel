def remove_rbar(x):
    if type(x) is not str:
        return x
    return x.replace("\r", " ")


def found_page(reader):
    for i, page in enumerate(reader.pages):
        if (
            "7\n.\nAnexo II\nTermo Complementar \nRelação de Terminais da Negociação"
            in page.extract_text()
        ):
            termo = page.extract_text()

        if ("\nUnit.\nServiço Vlr. Unit.\n") in page.extract_text():
            found_page = i + 1

    return termo, found_page
