# Biblioteca utilizada para gerar links curtos a partir de longos
import pyshorteners

# Model
class Link:
    def __init__(self, long, short, index = ''):
        self.long = long
        self.short = short
        self.index = index

# DAO
class DaoLink:
    @classmethod
    def salvar(cls, link: Link):
        with open('links.txt', 'a') as arq:
            arq.writelines(str(cls.return_len_links_salvos()) + '|' + link.long + '|' + link.short)
            arq.writelines('\n')

    @classmethod
    def ler(cls):
        with open('links.txt', 'r') as arq:
            cls.links_txt = arq.readlines()

        cls.links_txt = list(map(lambda x: x.replace('\n', ''), cls.links_txt))
        cls.links_txt = list(map(lambda x: x.split('|'), cls.links_txt))
        
        links = []

        for i in cls.links_txt:
            links.append(Link(i[1], i[2], i[0]))

        return links

    @classmethod
    def return_len_links_salvos(cls):
        with open('links.txt', 'r') as arq:
            cls.links_txt = arq.readlines()

        next_index = len(cls.links_txt) + 1

        return next_index

# Controller
class ControllerLink:
    def salvalink(self, novolinklong):
        self.novolinklong = novolinklong
        existe = False

        x = DaoLink.ler()

        for i in x:
            if i.long == self.novolinklong:
                existe = True
                break

        if not existe:
            novolink = self.encurtar_long_url(self.novolinklong)

            if novolink == False:
                return '\nAlgo deu errado.'

            DaoLink.salvar(novolink)
            return f'''
            Link curto: {novolink.short}

            Link salvo com sucesso!'''
        else:
            return '\nLink já existe.'

    def deletalink(self, indexdelete):
        x = DaoLink.ler()

        links_atua = list(filter(lambda x: x.index == indexdelete, x))

        if len(links_atua) <= 0:
            return '\nO index do link que deseja remover não existe.'
        else:
            for i in range(0, len(x)):
                if x[i].index == indexdelete:
                    del x[i]
                    break

            with open('links.txt', 'w') as arq:
                index = 1
                for link in x:
                    arq.writelines(str(index) + '|' + link.long + '|' + link.short)
                    arq.writelines('\n')

                    index += 1

            return '\nLink removido com sucesso!'

    def encurtar_long_url(self, link_long):
        self.link_long = link_long
        try:
            funct_encurtar = pyshorteners.Shortener()
            link_short = funct_encurtar.tinyurl.short(self.link_long)

            novolink = Link(self.link_long, link_short)
            
            return novolink

        except:
            return False

    def retorna_valores_format(self, links):
        for link in links:
            yield f'Index: {link.index} | Link longo: {link.long} | Link curto: {link.short}'

# View
def view():
    decisao = input('''\nDigite para

    Encurtar um link [1]
    Deletar um link salvo [2]
    Visualizar links salvos [3]
    Sair [4]
    
    R: ''')

    start = ControllerLink()

    if decisao == '1':
        novolinklong = input('\nInforme o link para encurtar: ')
        print(start.salvalink(novolinklong))
        view()
    elif decisao == '2':
        novoindexdelete = input('\nInforme o index do link que deseja deletar: ')
        print(start.deletalink(novoindexdelete))
        view()
    elif decisao == '3':
        links = start.retorna_valores_format(DaoLink.ler())
        for link in links:
            print(link)
        view()
    elif decisao == '4':
        print('\nSaindo...')
    else:
        print('\nValor inválido!')
        view()

view()
