"""Funções para normalização e limpeza de texto e listas de textos."""
import unicodedata


def ascii_sanitizar(text):
    """Remove marcas de diacríticos (acentos e caracteres especiais).

    Retorna NFC normalizado ASCII
    """
    if not text:
        return None
    return unicodedata.normalize('NFKD', text) \
        .encode('ASCII', 'ignore') \
        .decode('ASCII')


def unicode_sanitizar(text):
    """Remove marcas de diacríticos (acentos e caracteres especiais).

    Retorna NFC normalizado unicode
    """
    if not text:
        return None
    norm_txt = unicodedata.normalize('NFD', text)
    shaved = ''.join(char for char in norm_txt
                     if not unicodedata.combining(char))
    if not shaved:
        return None
    return unicodedata.normalize('NFC', shaved)


def mongo_sanitizar(text):
    """Remove todo caractere que pode ser usado em ataque MongoDB injection."""
    LETRAS = u'abcdefghijklmnopqrstuvwxyz'
    NUMEROS = u'0123456789'
    SINAIS = u'*.,+&%@! _-:/'
    secure = LETRAS + LETRAS.upper() + NUMEROS + SINAIS
    if not text:
        return None
    norm_txt = unicodedata.normalize('NFD', text)
    shaved = ''.join(char for char in norm_txt
                     if char in secure)
    if not shaved:
        return None
    return unicodedata.normalize('NFC', shaved)


def sanitizar(text, norm_function=unicode_sanitizar):
    """Faz uma sequência de acões de normalização/sanitização de texto.

    Remove espaços à direita e esquerda, passa para "casefold"(caixa baixa),
    usa função normalização norm_function para retirar marcas de diacríticos
    (acentos e caracteres especiais), remove espaços adicionais entre palavras.
    Retorna texto sanitizado e normalizado
    Depois desse produto, suas buscas nunca mais serão as mesmas!!! :-p
    """
    if text is None or text == '':
        return text
    text = text.strip()
    text = text.casefold()
    text = norm_function(text)
    if text is None or text == '':
        return text
    word_list = text.split()
    text = ' '.join(word.strip() for word in word_list
                    if len(word.strip()))
    return text


def sanitizar_lista(lista, norm_function=unicode_sanitizar):
    """Percorre lista de listas sanitizando inline.

    Por ora só suporta lista 'bidimensional', como um csv,
    uma lista de strings, ou uma lista contendo listas de strings.
    """
    for row in range(len(lista)):
        linha = lista[row]
        if isinstance(linha, str):
            lista[row] = sanitizar(linha, norm_function)
        elif isinstance(linha, list):
            for col in range(len(lista[row])):
                lista[row][col] = sanitizar(lista[row][col], norm_function)
        else:
            raise TypeError('Tipo não suportado (tipos suportados, list(str)' +
                            'ou list(list(str). Ver documentação.')
    return lista
