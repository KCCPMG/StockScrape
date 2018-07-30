import requests
from bs4 import BeautifulSoup as bs

# Takes an input list of strings. Strings that generate
# true stock pages are kept, bad ones are tossed

# Checks if a single symbol is valid
def is_valid_symbol(symbol):
    if type(symbol) != str:
        return False
    else:
        try:
            url = 'https://finance.yahoo.com/quote/%s?p=%s' % (symbol, symbol)
            soup = bs(requests.get(url).text, 'html.parser')
            if 'Summary for' in str(soup.title):
                return True
            else:
                return False
        except requests.exceptions.TooManyRedirects:
            return False

def get_valid_symbols(sym_list, output_incorrect=False):
    valid_syms = []
    incorrect_syms = []
    for sym in sym_list:
        if is_valid_symbol(sym):
            valid_syms.append(sym)
        else:
            if output_incorrect is True:
                incorrect_syms.append(sym)
    if output_incorrect is False:
        return valid_syms
    else:
        return valid_syms, incorrect_syms
