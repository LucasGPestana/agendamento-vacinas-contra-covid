import tkinter as tk
from pycep_correios import get_address_from_cep, exceptions, WebService

dados_pacientes = list()

def cadastrar_dados(entry_nome, entry_nome_mae, entry_cep, text_endereco, entry_cpf, entry_nascimento):
    
    nome = entry_nome.get()
    nome_mae = entry_nome_mae.get()
    cep = entry_cep.get()
    endereco = text_endereco['Text']
    cpf = entry_cpf.get()
    data_nascimento = entry_nascimento.get()


    # Verifica se todos os dados estão corretamente preenchidos

    dados_pacientes.append({"Nome": nome, "Nome da Mãe": nome_mae, "CEP": cep, "Endereço": endereco, "CPF": cpf, "Data de Nascimento": data_nascimento})

def validar_cep(cep):
    
    # Junta em uma string o cep sem o hífen, que foi dividido em uma lista pelo split
    cep = "".join(cep.replace("-", " ").split())

    # Verifica se o CEP possui o tamanho correto e se contém apenas números
    if len(cep) == 8 and cep.isnumeric():
        return True
    else:
        return False

def verificar_endereco(entry_cep, text_endereco):
   
  cep = entry_cep.get()

  if validar_cep:
       
       try:
    
          endereco = get_address_from_cep(cep, webservice=WebService.APICEP)

          for info in endereco.keys():
              text_endereco['fg'] = "#008000" # Muda a cor do texto para verde
              text_endereco['Text'] = f"{info} - {endereco[info]}\n"
       
       except exceptions.CEPNotFound:
           text_endereco['fg'] = "#FF0000" # Muda a cor do texto para vermelho
           text_endereco['Text'] = "CEP não encontrado"
    
  else:
      text_endereco['fg'] = "#FF0000" # Muda a cor do texto para vermelho
      text_endereco['Text'] = "CEP inválido!"
           

def janela_cadastro():
    
    janela_cadastro = tk.Tk()

    janela_cadastro.geometry("600x400")
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

    # Botão para verificar o endereço
    btn_endereco = tk.Button(master=janela_cadastro, text="Verificar Endereço", font=FONTE_PADRAO, fg=COR_FONTE_PADRAO_2, border=2, command=verificar_endereco)
    btn_endereco.grid(row=2, column=2, padx=5)

    # Campo CPF do paciente (row 4)

    # Campo Data de nascimento do paciente (row 5)

    # Botão para confirmar o cadastro do paciente
    btn_cadastrar = tk.Button(master=janela_cadastro, text="Cadastrar dados", font=FONTE_PADRAO, fg=COR_FONTE_PADRAO_2, border=5)
    btn_cadastrar.grid(row=6, column=2)

    janela_cadastro.mainloop()

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
btn_cadastro.pack(side=tk.TOP, pady=100) # Posiciona o botão na parte de cima da janela, dando uma margem externa de 100px acima


main_window.mainloop()