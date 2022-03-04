# Biblioteca utilizada para gerar links curtos a partir de longos
import pyshorteners

def encurtar_long_url():
    link_long = input('Informe a URL: ')

    funct_encurtar = pyshorteners.Shortener()

    link_short = funct_encurtar.tinyurl.short(link_long)

    print(f'Link curto: {link_short}')

encurtar_long_url()