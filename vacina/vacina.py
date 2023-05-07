import tkinter as tk
from pycep_correios import get_address_from_cep, exceptions, WebService
from datetime import date
import re

dados_pacientes = list()

def gerarArquivo():
    arquivo = open("dados-pacientes.txt", "a")
    
    for paciente in dados_pacientes:
        print(paciente, file=arquivo)
    
    arquivo.close()

def cadastrar_dados(entry_nome, entry_nome_mae, entry_cep, text_endereco, entry_cpf, entry_nascimento, label_resposta):
    
    nome = entry_nome.get()
    nome_mae = entry_nome_mae.get()
    cep = entry_cep.get()
    endereco = text_endereco['text']
    cpf = entry_cpf.get()
    data_nascimento = entry_nascimento.get()


    # Verifica se todos os dados estão corretamente preenchidos

    if validar_nome(nome):
        if validar_nome(nome_mae):
            if validar_cep(cep):
                if endereco != "":
                    if validar_cpf(cpf):
                        if validar_data_nascimento(data_nascimento):
                            dados_pacientes.append({"Nome": nome.capitalize(), "Nome da Mãe": nome_mae.capitalize(), "CEP": cep, "Endereço": endereco, "CPF": cpf, "Data de Nascimento": data_nascimento})
                            label_resposta['fg'] = "#008000"
                            label_resposta['text'] = ""
                            label_resposta['text'] = "Cadastro realizado com sucesso!"
                            print(dados_pacientes)
                        else:
                            label_resposta['fg'] = "#FF0000"
                            label_resposta['text'] = ""
                            label_resposta['text'] = "Data de nascimento inválida!"
                    else:
                        label_resposta['fg'] = "#FF0000"
                        label_resposta['text'] = ""
                        label_resposta['text'] = "CPF do Paciente inválido!"
                else:
                    label_resposta['fg'] = "#FF0000"
                    label_resposta['text'] = ""
                    label_resposta['text'] = "Endereço não encontrado!"
            else:
                label_resposta['fg'] = "#FF0000"
                label_resposta['text'] = ""
                label_resposta['text'] = "CEP do Paciente inválido!"
        else:
            label_resposta['fg'] = "#FF0000"
            label_resposta['text'] = ""
            label_resposta['text'] = "Nome da Mãe inválido!"
    else:
        label_resposta['fg'] = "#FF0000"
        label_resposta['text'] = ""
        label_resposta['text'] = "Nome do Paciente inválido!"

def validar_nome(nome_completo): # Serve para verificar o nome do paciente e o nome da mãe

    if nome_completo == "":
        return False

    nome_completo = nome_completo.split() # isalpha não identifica espaços como alfa-numérico. Por isso, há a necessidade do split

    for nome in nome_completo:
        if not nome.isalpha(): # isalpha não identifica espaços 
            return False
    return True

def validar_cpf(cpf):

    if cpf == "":
        return False
    
    for paciente in dados_pacientes:
        if cpf == paciente['CPF']: # Verifica se o cpf em questão já existe entre os cadastrados
            return False
    
    cpf = "".join(cpf.replace("-", " ").replace(".", " ").split()) # Substitui todos os simbolos por espaços para dividir com o split
    # Após isso, junta todos os elementos da lista em uma string sem espaços entre eles com o join

    if len(cpf) == 11:
        return True
    else:
        return False

def validar_data_nascimento(data):

    padrao_data = re.compile("\d\d/\d\d/\d\d\d\d") # Padrão: dd/mm/yyyy

    if data == "" or re.fullmatch(padrao_data, data) == None: # Verifica se a data é vazia ou se a data não segue o padrão estabelecido
        return False
    
    data_atual = date.today()
    data = data.split("/") # Divide a string em substrings e adiciona essas substrings dentro de uma lista

    dia = int(data[0]) # Converte os valores string da lista para inteiros
    mes = int(data[1])
    ano = int(data[2])

    if len(str(dia)) == 2 and (len(str(mes)) == 2 or len(str(mes)) == 1) and len(str(ano)) == 4: # Verifica o tamanho de cada elemento
        if 1900 < ano <= data_atual.year: # Verifica se o ano está entre 1900 e o ano atual
            if 1 <= mes <= 12:
                if mes != 2:
                    if mes < 8: # Meses pares anteriores a agosto possuem 30 dias, enquanto os impares possuem 31.
                        if mes % 2 == 0:
                            # Tem trinta dias
                            if 1 <= dia <= 30:
                                return True
                            else:
                                return False
                        else:
                            if 1 <= dia <= 31:
                                return True
                            else:
                                return False
                    elif mes == 8:
                        if 1 <= dia <= 31:
                            return True
                        else:
                            return False
                    else: # Meses pares posteriores a agosto possuem 31 dias, enquanto os impares possuem 30.
                        if mes % 2 == 0:
                            # Tem trinta e um dias
                            if 1 <= dia <= 31:
                                return True
                            else:
                                return False
                        else:
                            if 1 <= dia <= 30:
                                return True
                            else:
                                return False
                else:
                    if 1 <= dia <= 29: # Não verifica se o ano é bissexto ou não
                        return True
                    else:
                        return False
            else:
                return False
        else:
            return False
    else:
        return False
    
def validar_cep(cep):

    if cep == "":
        return False
    
    # Junta em uma string o cep sem o hífen, que foi dividido em uma lista pelo split
    cep = "".join(cep.replace("-", " ").split())

    # Verifica se o CEP possui o tamanho correto e se contém apenas números
    if len(cep) == 8 and cep.isnumeric():
        return True
    else:
        return False

def verificar_endereco(entry_cep, text_endereco):
   
  cep = entry_cep.get()

  if validar_cep and cep != "": # Verifica se o cep é valido e se o cep não está vazio
       
       try:
    
          endereco = get_address_from_cep(cep, webservice=WebService.APICEP)
          
          text_endereco['text'] = "" # Apaga o que estiver escrito previamente

          for info in endereco.keys():
              if endereco[info] == "":
                  endereco[info] = "Não identificado"
              text_endereco['fg'] = "#008000" # Muda a cor do texto para verde
              print(f"{info} - {endereco[info]}")
              text_endereco['text'] += f"| {info} - {endereco[info]} " # Adiciona a string à string vazia
          text_endereco['text'] += "|"
       
       except exceptions.CEPNotFound:
           text_endereco['fg'] = "#FF0000" # Muda a cor do texto para vermelho
           text_endereco['text'] = "CEP não encontrado"
    
  else:
      text_endereco['fg'] = "#FF0000" # Muda a cor do texto para vermelho
      text_endereco['text'] = "" # Apaga o que estiver escrito previamente
      text_endereco['text'] = "CEP inválido!"
        
def janela_cadastro():
    
    janela_cadastro = tk.Tk()

    janela_cadastro.geometry("1000x400")
    janela_cadastro.title("Cadastro de Dados da Vacinação")
    janela_cadastro["bg"] = FUNDO_PADRAO

    # Inicialmente, a janela possui apenas uma linha e uma coluna

    # Padrão da posição dos itens, onde (linha, coluna): posição label = (x, y) e posição entry = (x, y + 1)

    # Campo Nome do paciente
    label_nome = tk.Label(master=janela_cadastro, text="Nome Completo: ", font=FONTE_PADRAO, fg=COR_FONTE_PADRAO, bg=FUNDO_PADRAO)
    label_nome.grid(row=0, column=0) # Posiciona na linha 1 e coluna 1 da janela

    entry_nome = tk.Entry(master=janela_cadastro)
    entry_nome.grid(row=0, column=1) # Posiciona na linha 1 e coluna 2 da janela

    # Campo Nome da mãe
    label_nome_mae = tk.Label(master=janela_cadastro, text="Nome Completo da Mãe: ", font=FONTE_PADRAO, fg=COR_FONTE_PADRAO, bg=FUNDO_PADRAO)
    label_nome_mae.grid(row=1, column=0)

    entry_nome_mae = tk.Entry(master=janela_cadastro)
    entry_nome_mae.grid(row=1, column=1)

    # Campo CEP do paciente
    label_cep = tk.Label(master=janela_cadastro, text="CEP do Paciente: ", font=FONTE_PADRAO, fg=COR_FONTE_PADRAO, bg=FUNDO_PADRAO)
    label_cep.grid(row=2, column=0)

    entry_cep = tk.Entry(master=janela_cadastro)
    entry_cep.grid(row=2, column=1)

    # Resposta da verificação do CEP

    text_endereco = tk.Label(master=janela_cadastro, text="", font=FONTE_PADRAO, fg=COR_FONTE_PADRAO, bg=FUNDO_PADRAO)
    text_endereco.grid(row=3, column=0)

    def verificar_endereco_wrapper(): # Serve de callback
        verificar_endereco(entry_cep, text_endereco)

    # Botão para verificar o endereço
    btn_endereco = tk.Button(master=janela_cadastro, text="Verificar Endereço", font=FONTE_PADRAO, fg=COR_FONTE_PADRAO_2, border=2, command=verificar_endereco_wrapper)
    btn_endereco.grid(row=2, column=2, padx=5)

    # Campo CPF do paciente (row 4)
    label_cpf = tk.Label(master=janela_cadastro, text="CPF do Paciente: ", font=FONTE_PADRAO, fg=COR_FONTE_PADRAO, bg=FUNDO_PADRAO)
    label_cpf.grid(row=4, column=0)

    entry_cpf = tk.Entry(master=janela_cadastro)
    entry_cpf.grid(row=4, column=1)

    label_cpf_obs = tk.Label(master=janela_cadastro, text="Obs: CPFs já cadastrados constam como inválidos!", font=FONTE_PADRAO, fg=COR_FONTE_PADRAO, bg=FUNDO_PADRAO)
    label_cpf_obs.grid(row=4, column=2)

    # Campo Data de nascimento do paciente (row 5)
    label_data_nascimento = tk.Label(master=janela_cadastro, text="Data de Nascimento (dd/mm/yyyy): ", font=FONTE_PADRAO, fg=COR_FONTE_PADRAO, bg=FUNDO_PADRAO)
    label_data_nascimento.grid(row=5, column=0)

    entry_data_nascimento = tk.Entry(master=janela_cadastro)
    entry_data_nascimento.grid(row=5, column=1)

    def cadastrar_dados_wrapper(): # Serve de callback
        cadastrar_dados(entry_nome, entry_nome_mae, entry_cep, text_endereco, entry_cpf, entry_data_nascimento, label_resposta)

    # Botão para confirmar o cadastro do paciente
    btn_cadastrar = tk.Button(master=janela_cadastro, text="Cadastrar dados", font=FONTE_PADRAO, fg=COR_FONTE_PADRAO_2, border=5, command=cadastrar_dados_wrapper)
    btn_cadastrar.grid(row=6, column=2)

    # Resposta do botão
    label_resposta = tk.Label(master=janela_cadastro, text="", font=FONTE_PADRAO, fg=COR_FONTE_PADRAO, bg=FUNDO_PADRAO)
    label_resposta.grid(row=7, column=2)

    janela_cadastro.mainloop()

if __name__ == "__main__": # Main do código (Início)

    # Variáveis constantes

    FUNDO_PADRAO = "#2d2d30"
    FONTE_PADRAO = ("Arial 10")
    COR_FONTE_PADRAO = "#FFFFFF"
    COR_FONTE_PADRAO_2 = "#000000"


    main_window = tk.Tk()

    # Configuração da Janela
    main_window.geometry("600x400") # Estabelece as dimensões da janela
    main_window.title("Conecte SUS")
    main_window["bg"] = FUNDO_PADRAO # Fundo da janela

    # Título da página
    h1_principal = tk.Label(master=main_window, text="CONECT SUS", font=("Arial 12 bold"), bg=FUNDO_PADRAO, fg=COR_FONTE_PADRAO)
    h1_principal.pack(side=tk.TOP, pady=20) # Posiciona o Label na parte de cima da janela, dando uma margem externa de 20px acima


    btn_cadastro = tk.Button(master=main_window, width=16, text="Cadastrar Dados", font=FONTE_PADRAO, fg=COR_FONTE_PADRAO_2, border=12, command=janela_cadastro)
    btn_cadastro.pack(side=tk.TOP, pady=80) # Posiciona o botão na parte de cima da janela, dando uma margem externa de 80px acima

    btn_arquivo = tk.Button(master=main_window, width=16, text="Gerar Arquivo", font=FONTE_PADRAO, fg=COR_FONTE_PADRAO_2, border=12, command=gerarArquivo)
    btn_arquivo.pack(side=tk.TOP)

    main_window.mainloop()