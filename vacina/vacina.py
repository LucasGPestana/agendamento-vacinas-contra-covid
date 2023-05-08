import tkinter as tk
from PIL import Image, ImageTk
from brazilcep import get_address_from_cep, exceptions, WebService
from datetime import date
import re

dados_pacientes = list()

def limpar_dados(entry_nome, entry_nome_mae, entry_cep, resposta_rua, 
                 resposta_complemento, resposta_bairro, resposta_cidade, 
                 resposta_estado, entry_cpf, entry_nascimento):
    entry_nome.delete(0, tk.END)
    entry_nome_mae.delete(0, tk.END)
    entry_cep.delete(0, tk.END)
    resposta_rua['text'] = ""
    resposta_complemento['text'] = ""
    resposta_bairro['text'] = ""
    resposta_cidade['text'] = ""
    resposta_estado['text'] = ""
    entry_cpf.delete(0, tk.END)
    entry_nascimento.delete(0, tk.END)

def gerarArquivo():
    arquivo = open("dados-pacientes.txt", "w", encoding="utf-8")
    
    for paciente in dados_pacientes:
        print(paciente, file=arquivo)
    
    arquivo.close()

def cadastrar_dados(entry_nome, entry_nome_mae, entry_cep, resposta_rua,
                     resposta_complemento, resposta_bairro, resposta_cidade,
                       resposta_estado, entry_cpf, entry_nascimento, label_resposta):
    
    nome = entry_nome.get()
    nome_mae = entry_nome_mae.get()
    cep = entry_cep.get()
    endereco = f"Rua: {resposta_rua['text']}, Complemento: {resposta_complemento['text']}, Bairro: {resposta_bairro['text']}, Cidade:{resposta_cidade['text']}, Estado: {resposta_estado['text']}"
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
                            label_resposta['fg'] = COR_SUCESSO
                            label_resposta['text'] = ""
                            label_resposta['text'] = "Cadastro realizado com sucesso!"
                            print(dados_pacientes)
                            limpar_dados(entry_nome, entry_nome_mae, entry_cep, resposta_rua, resposta_complemento, resposta_bairro, resposta_cidade, resposta_estado, entry_cpf, entry_nascimento)
                            entry_nome.focus_set()
                        else:
                            label_resposta['fg'] = COR_FALHA
                            label_resposta['text'] = ""
                            label_resposta['text'] = "Data de nascimento inválida!"
                            entry_nascimento.focus_set()
                    else:
                        label_resposta['fg'] = COR_FALHA
                        label_resposta['text'] = ""
                        label_resposta['text'] = "CPF do Paciente inválido!"
                        entry_cpf.focus_set()
                else:
                    label_resposta['fg'] = COR_FALHA
                    label_resposta['text'] = ""
                    label_resposta['text'] = "Endereço não encontrado!"
                    entry_cep.focus_set()
            else:
                label_resposta['fg'] = COR_FALHA
                label_resposta['text'] = ""
                label_resposta['text'] = "CEP do Paciente inválido!"
                entry_cep.focus_set()
        else:
            label_resposta['fg'] = COR_FALHA
            label_resposta['text'] = ""
            label_resposta['text'] = "Nome da Mãe inválido!"
            entry_nome_mae.focus_set()
    else:
        label_resposta['fg'] = COR_FALHA
        label_resposta['text'] = ""
        label_resposta['text'] = "Nome do Paciente inválido!"
        entry_nome.focus_set()

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

    dia = data[0] # Guarda os valores da lista em variáveis
    mes = data[1]
    ano = data[2]

    if (len(str(dia)) == 2) and (len(str(mes)) == 2 ) and len(str(ano)) == 4: # Verifica o tamanho de cada elemento

        # Converte as variáveis para inteiros
        dia, mes, ano = map(int, [dia, mes, ano]) # Itera cada elemento da lista, convertendo-o para inteiro

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

def verificar_endereco(entry_cep, resposta_rua, resposta_complemento, resposta_bairro, resposta_cidade, resposta_estado, text_endereco):
  
  text_endereco['text'] = "" # Apaga o que estiver escrito previamente
   
  cep = entry_cep.get()

  if validar_cep and cep != "": # Verifica se o cep é valido e se o cep não está vazio
       
       try:
    
          endereco = get_address_from_cep(cep, webservice=WebService.APICEP)
          
          # Substitui valores vazios por "Não Identificado"
          for info in endereco.keys():
              if endereco[info] == "":
                  endereco[info] = "Não Identificado"
          
          print(endereco)
          
          # Adiciona as informações do endereço aos Labels
          resposta_rua['text'] = endereco['street']
          resposta_complemento['text'] = endereco['complement']
          resposta_bairro['text'] = endereco['district']
          resposta_cidade['text']= endereco['city']
          resposta_estado['text'] = endereco['uf']
       
       except exceptions.CEPNotFound:
           text_endereco['fg'] = COR_FALHA # Muda a cor do texto para vermelho
           text_endereco['text'] = "CEP não encontrado"
           entry_cep.focus_set() # Foca no entry

       except exceptions.InvalidCEP:
           text_endereco['fg'] = COR_FALHA # Muda a cor do texto para vermelho
           text_endereco['text'] = "CEP inválido!"
           entry_cep.focus_set()
    
  else:
      # CEP inválido
      text_endereco['fg'] = COR_FALHA # Muda a cor do texto para vermelho
      text_endereco['text'] = "CEP inválido!"
      entry_cep.focus_set()
        
def janela_cadastro():
    
    janela_cadastro = tk.Tk()

    janela_cadastro.geometry("1000x500")
    janela_cadastro.title("Cadastro de Dados da Vacinação")
    janela_cadastro["bg"] = FUNDO_PADRAO

    # Inicialmente, a janela possui apenas uma linha e uma coluna

    # Padrão da posição dos itens, onde (linha, coluna): posição label = (x, y) e posição entry = (x, y + 1)

    # Campo Nome do paciente
    label_nome = tk.Label(master=janela_cadastro, 
                          text="Nome Completo: ", 
                          font=FONTE_PADRAO, 
                          fg=COR_FONTE_PADRAO, 
                          bg=FUNDO_PADRAO)
    label_nome.grid(row=0, column=0, padx=10, pady=10) # Posiciona na linha 1 e coluna 1 da janela

    entry_nome = tk.Entry(master=janela_cadastro, 
                          fg=COR_FONTE_PADRAO, 
                          bg=FUNDO_ELEMENTOS)
    entry_nome.grid(row=0, column=1, padx=10, pady=10) # Posiciona na linha 1 e coluna 2 da janela

    # Campo Nome da mãe
    label_nome_mae = tk.Label(master=janela_cadastro, 
                              text="Nome Completo da Mãe: ", 
                              font=FONTE_PADRAO, 
                              fg=COR_FONTE_PADRAO, 
                              bg=FUNDO_PADRAO)
    label_nome_mae.grid(row=1, column=0, padx=10, pady=10)

    entry_nome_mae = tk.Entry(master=janela_cadastro, 
                              fg=COR_FONTE_PADRAO, 
                              bg=FUNDO_ELEMENTOS)
    entry_nome_mae.grid(row=1, column=1, padx=10, pady=10)

    # Campo CEP do paciente
    label_cep = tk.Label(master=janela_cadastro, 
                         text="CEP do Paciente: ", 
                         font=FONTE_PADRAO, 
                         fg=COR_FONTE_PADRAO, 
                         bg=FUNDO_PADRAO)
    label_cep.grid(row=2, column=0, padx=10, pady=10)

    entry_cep = tk.Entry(master=janela_cadastro, 
                         fg=COR_FONTE_PADRAO, 
                         bg=FUNDO_ELEMENTOS)
    entry_cep.grid(row=2, column=1, padx=10, pady=10)

    # Resposta da verificação do CEP

    resposta_endereco = tk.Label(master=janela_cadastro, 
                                 text="", 
                                 font=FONTE_PADRAO, 
                                 fg=COR_FONTE_PADRAO, 
                                 bg=FUNDO_PADRAO)
    resposta_endereco.grid(row=2, column=3)
    
    # Labels para o endereço

    # Rua

    label_rua = tk.Label(master=janela_cadastro, 
                         text="Rua: ", 
                         font=FONTE_PADRAO, 
                         fg=COR_FONTE_PADRAO, 
                         bg=FUNDO_PADRAO)
    label_rua.grid(row=3, column=0, padx=10, pady=10)

    # O state disabled não permite que se digite no entry
    resposta_rua = tk.Label(master=janela_cadastro, 
                            text="", 
                            font=FONTE_PADRAO, 
                            fg=COR_FONTE_PADRAO, 
                            bg=FUNDO_PADRAO)
    resposta_rua.grid(row=3, column=1, padx=10, pady=10)

    # Complemento

    label_complemento = tk.Label(master=janela_cadastro, 
                                 text="Complemento: ", 
                                 font=FONTE_PADRAO, 
                                 fg=COR_FONTE_PADRAO, 
                                 bg=FUNDO_PADRAO)
    label_complemento.grid(row=4, column=0, padx=10, pady=10)

    resposta_complemento = tk.Label(master=janela_cadastro, 
                                    text="", 
                                    font=FONTE_PADRAO, 
                                    fg=COR_FONTE_PADRAO, 
                                    bg=FUNDO_PADRAO)
    resposta_complemento.grid(row=4, column=1, padx=10, pady=10)

    # Bairro

    label_bairro = tk.Label(master=janela_cadastro, 
                            text="Bairro: ", 
                            font=FONTE_PADRAO, 
                            fg=COR_FONTE_PADRAO, 
                            bg=FUNDO_PADRAO)
    label_bairro.grid(row=5, column=0, padx=10, pady=10)

    resposta_bairro = tk.Label(master=janela_cadastro, 
                               text="", 
                               font=FONTE_PADRAO, 
                               fg=COR_FONTE_PADRAO, 
                               bg=FUNDO_PADRAO)
    resposta_bairro.grid(row=5, column=1, padx=10, pady=10)

    # Cidade

    label_cidade = tk.Label(master=janela_cadastro, 
                            text="Cidade: ", 
                            font=FONTE_PADRAO, 
                            fg=COR_FONTE_PADRAO, 
                            bg=FUNDO_PADRAO)
    label_cidade.grid(row=6, column=0, padx=10, pady=10)

    resposta_cidade = tk.Label(master=janela_cadastro, 
                               text="", 
                               font=FONTE_PADRAO, 
                               fg=COR_FONTE_PADRAO, 
                               bg=FUNDO_PADRAO)
    resposta_cidade.grid(row=6, column=1, padx=10, pady=10)

    # Estado

    label_estado = tk.Label(master=janela_cadastro, 
                            text="Estado: ", 
                            font=FONTE_PADRAO, 
                            fg=COR_FONTE_PADRAO, 
                            bg=FUNDO_PADRAO)
    label_estado.grid(row=6, column=2, padx=10, pady=10)

    resposta_estado = tk.Label(master=janela_cadastro, 
                               text="", font=FONTE_PADRAO, 
                               fg=COR_FONTE_PADRAO, 
                               bg=FUNDO_PADRAO)
    resposta_estado.grid(row=6, column=3, padx=10, pady=10)

    def verificar_endereco_wrapper(): # Serve de callback
        verificar_endereco(entry_cep, resposta_rua, resposta_complemento, resposta_bairro, resposta_cidade, resposta_estado, resposta_endereco)

    # Botão para verificar o endereço
    btn_endereco = tk.Button(master=janela_cadastro, 
                             text="Verificar Endereço", 
                             font=FONTE_PADRAO, 
                             fg=COR_FONTE_PADRAO, 
                             bg=FUNDO_ELEMENTOS, 
                             border=2, 
                             command=verificar_endereco_wrapper)
    btn_endereco.grid(row=2, column=2)

    # Campo CPF do paciente (row 4)
    label_cpf = tk.Label(master=janela_cadastro, 
                         text="CPF do Paciente: ", 
                         font=FONTE_PADRAO, 
                         fg=COR_FONTE_PADRAO, 
                         bg=FUNDO_PADRAO)
    label_cpf.grid(row=7, column=0, padx=10, pady=10)

    entry_cpf = tk.Entry(master=janela_cadastro, 
                         fg=COR_FONTE_PADRAO, 
                         bg=FUNDO_ELEMENTOS)
    entry_cpf.grid(row=7, column=1, padx=10, pady=10)

    label_cpf_obs = tk.Label(master=janela_cadastro, 
                             text="Obs: CPFs já cadastrados constam como inválidos!", 
                             font=FONTE_PADRAO, 
                             fg=COR_FONTE_PADRAO, 
                             bg=FUNDO_PADRAO)
    label_cpf_obs.grid(row=7, column=2, padx=10, pady=10)

    # Campo Data de nascimento do paciente (row 5)
    label_data_nascimento = tk.Label(master=janela_cadastro, 
                                     text="Data de Nascimento (dd/mm/yyyy): ", 
                                     font=FONTE_PADRAO, 
                                     fg=COR_FONTE_PADRAO, 
                                     bg=FUNDO_PADRAO)
    label_data_nascimento.grid(row=8, column=0, padx=10, pady=10)

    entry_data_nascimento = tk.Entry(master=janela_cadastro, 
                                     fg=COR_FONTE_PADRAO, 
                                     bg=FUNDO_ELEMENTOS)
    entry_data_nascimento.grid(row=8, column=1, padx=10, pady=10)

    def cadastrar_dados_wrapper(): # Serve de callback
        cadastrar_dados(entry_nome, entry_nome_mae, entry_cep, resposta_rua, resposta_complemento, resposta_bairro, resposta_cidade, resposta_estado, entry_cpf, entry_data_nascimento, label_resposta)

    # Botão para confirmar o cadastro do paciente
    btn_cadastrar = tk.Button(master=janela_cadastro, 
                              text="Cadastrar Dados", 
                              font=FONTE_PADRAO, 
                              fg=COR_FONTE_PADRAO, 
                              bg=FUNDO_ELEMENTOS, 
                              border=5, 
                              command=cadastrar_dados_wrapper)
    btn_cadastrar.grid(row=9, column=2, padx=10, pady=10)

    # Botão para cancelar o cadastro do paciente
    btn_cancelar = tk.Button(master=janela_cadastro, 
                             text="Cancelar", 
                             height=1, 
                             font=FONTE_PADRAO, 
                             fg=COR_FONTE_PADRAO, 
                             bg=FUNDO_ELEMENTOS, 
                             border=5, 
                             command=janela_cadastro.destroy)
    btn_cancelar.grid(row=9, column=3, padx=10, pady=10)

    # Resposta do botão
    label_resposta = tk.Label(master=janela_cadastro, 
                              text="", font=FONTE_PADRAO, 
                              fg=COR_FONTE_PADRAO, 
                              bg=FUNDO_PADRAO)
    label_resposta.grid(row=10, column=2, padx=10, pady=10)

    janela_cadastro.mainloop()

# Variáveis constantes

FUNDO_PADRAO = "white"
FUNDO_ELEMENTOS = "#d3d3d3"
FONTE_PADRAO = ("Arial 10")
COR_FONTE_PADRAO = "blue"
COR_SUCESSO = "#008000"
COR_FALHA = "#FF0000"

if __name__ == "__main__": # Main do código (Início)

    main_window = tk.Tk()

    # Configuração da Janela
    main_window.geometry("600x500") # Estabelece as dimensões da janela
    main_window.title("Conecte SUS")
    main_window["bg"] = FUNDO_PADRAO # Fundo da janela

    # Título da página
    h1_principal = tk.Label(master=main_window, 
                            text="CONECT SUS", 
                            font=("Arial 12 bold"), 
                            bg=FUNDO_PADRAO, 
                            fg=COR_FONTE_PADRAO)
    h1_principal.pack(side=tk.TOP, pady=20) # Posiciona o Label na parte de cima da janela, dando uma margem externa de 20px acima

    # Logo SUS
    logo = Image.open("sus-logo-pequeno.png")
    photo = ImageTk.PhotoImage(logo) # Carrega a imagem aberta
    tk.Label(master=main_window, image=photo).pack(side=tk.TOP, pady=10) # Poe a imagem carregada dentro de um label

    btn_cadastro = tk.Button(master=main_window, 
                             width=16, 
                             text="Cadastrar Dados", 
                             font=FONTE_PADRAO, 
                             fg=COR_FONTE_PADRAO, 
                             bg=FUNDO_ELEMENTOS, 
                             border=12, 
                             command=janela_cadastro)
    btn_cadastro.pack(side=tk.TOP, pady=20) # Posiciona o botão na parte de cima da janela, dando uma margem externa de 80px acima

    btn_arquivo = tk.Button(master=main_window, 
                            width=16, text="Gerar Arquivo", 
                            font=FONTE_PADRAO, 
                            fg=COR_FONTE_PADRAO, 
                            bg=FUNDO_ELEMENTOS, 
                            border=12, 
                            command=gerarArquivo)
    btn_arquivo.pack(side=tk.TOP, pady=20)

    btn_fechar = tk.Button(master=main_window, 
                           width=16, 
                           text="Fechar", 
                           font=FONTE_PADRAO, 
                           fg=COR_FONTE_PADRAO, 
                           bg=FUNDO_ELEMENTOS, 
                           border=12, 
                           command=main_window.destroy)
    btn_fechar.pack(side=tk.TOP, pady=20)

    main_window.mainloop()