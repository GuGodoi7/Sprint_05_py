from datetime import date
import re 
from Connection import criar_tabela_cadastro_pessoa_fisica, criar_tabela_acessorio, inserir_acessorios_bike, inserir_dados_cadastro_pessoa_fisica, criar_tabela_bike, inserir_dados_bike, tabela_existe, select_cadastro, select_bike

# Menu para escolha de Pessoa fisica ou Juridica
def menu_pessoa():
    while True:
            print ('''
=======INFORME COMO DESEJA LOGAR NO SITE=======
(1) Pessoa física 
(2) Pessoa Jurídica
(3) Sair
==============================================''')
            try:
                escolha_pessoa = int(input("Escolha: "))
                list_escolha = (1, 2, 3)

                if escolha_pessoa in list_escolha:
                    return escolha_pessoa
                else:
                    print("Escolha inválida. Tente novamente.")
            except ValueError:
                print ("Valor de entrada incorreta. Tente novamente.")

# Função para autenticar o usuário
def Cadastro(escolha):
        dados_cadastro = {}
        match escolha:
            case 1:
                while True:
                    try:
                        while True:
                            nome = input("Nome: ")
                            if nome.replace(" ", "").isalpha():
                                break
                            else:
                                print("Por favor, digite um nome válido contendo apenas letras e espaços. Tente novamente.")
                        while True:
                            cpf = input("CPF: ")
                            # Valida cpf
                            cpf_digitos = [int(c) for c in cpf if c.isdigit()] # cria uma lista chamada cpf_digitos que contém apenas os dígitos numéricos do CPF
                            if Verifica_cpf(cpf_digitos):
                                    break
                            else:
                                print("CPF inválido! Digite Novamente")
                        
                        endereco = input("Endereço: ")

                        while True:
                            telefone = (input("Telefone (no formato (XX) XXXXXXXX ou (XX) XXXXXXXXX): "))
                            if verifica_telefone(telefone):
                                break
                            else:
                                print("Número de telefone inválido.")
                        while True:
                            email = input("E-mail: ")
                            if verifca_email(email):
                                break
                            else:
                                print("Endereço de e-mail inválido.")
                        try:
                            while True:
                                data_input = input("Insira a data de nascimento (DD/MM/AAAA): ")
                                dia, mes, ano = data_input.split('/')
                                dia = int(dia)
                                mes = int(mes)
                                ano = int(ano)
                                if verificarIdade(date(ano, mes, dia)):
                                    dados_cadastro = {"Nome": nome, "Cpf": cpf, "Endereço": endereco, "Telefone": telefone, "E-mail": email,
                                                    "Data de Nascimento": date(ano, mes, dia)}
                                    break
                                else:
                                    print("Você deve ter pelo menos 18 anos para se cadastrar.")
                                    exit()
                        except ValueError:
                            print("Formato de data inválido. Use DD/MM/AAAA e tente novamente.")
                    except ValueError:
                        print("Formato de entrada Invalido ")
                    break
                                    
            case 2:
                try:
                    while True:
                        nome = input("Nome: ")
                        if nome.replace(" ", "").isalpha():
                            break
                        else:
                            print("Por favor, digite um nome válido contendo apenas letras e espaços. Tente novamente.")
                    while True:
                        # Valida CNPJ
                        cnpj = input("CNPJ: ")
                        if verifica_cnpj(cnpj):
                            break
                        else:
                            print("CNPJ inválido. Digite Novamente")
                    endereco = input("Endereço: ")
                    while True:
                        telefone = (input("Telefone (no formato (XX) XXXXXXXX ou (XX) XXXXXXXXX): "))
                        if verifica_telefone(telefone):
                            break
                        else:
                            print("Número de telefone inválido.")
                    while True:
                        email = input("E-mail: ")
                        if verifca_email(email):
                            break
                        else:
                            print("Endereço de e-mail inválido.")
                    while True:
                        data_fundacao = input("Digite o ano de fundação: ")
                        if  data_fundacao < date.today().year:
                            break
                        else:
                            print("Data invalida")

                    dados_cadastro = {"Nome" : nome , "Cnpj" : cnpj , "Endereço" : endereco, "Telefone" : telefone, "E-mail" : email, "Data de Fundação" : data_fundacao}
                except ValueError:
                    print("Valor de entrada invalido ")
            case _:
                exit(print("Programa Finalizado. Volte sempre!"))
        return dados_cadastro

# Verificar se o cpf é valido
def Verifica_cpf(num):

    # Verifica se o dados possui 14 digitos
    if len(num) != 11:
        return False

    soma = 0
    j = 10
    # Percorre os 9 digitos
    for i in range(9):
        soma += num[i] * j
        j -= 1
    resto = soma % 11
    if resto < 2:
        dv1 = 0
    else:
        dv1 = 11 - resto
    # Dígito verificador #2
    soma = 0
    j = 11
    for i in range(10):
        soma += num[i] * j
        # Toda vez que passa aqui subtrai 1
        j -= 1
    resto = soma % 11
    if resto < 2:
        dv2 = 0
    else:
        dv2 = 11 - resto
    if num[9] == dv1 and num[10] == dv2:
        return True
    else:
        return False

# Verificar se telefone é valido
def verifica_telefone(telefone):
    # Padrão de expressão regular para validar números de telefone brasileiros
    padrao = r"^\(\d{2}\)\s\d{4,5}\d{4}$"

    if re.match(padrao, telefone):
        return True
    else:
        return False

# Verificar se email é valido
def verifca_email(email):
    # Padrão de expressão regular para validar e-mails
    padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    
    if re.match(padrao, email):
        return True
    else:
        return False

#Verifica cnpj
def verifica_cnpj(cnpj):
    # Verifica se o dados possui 14 digitos
    if len(cnpj) != 14:
        return False
    
    # Calcula o primeiro dígito verificador
    soma = 0
    j = 5
    # Pecorre os 12 primeiros digitos 
    for i in range(12):
        soma += int(cnpj[i]) * j
        # Toda vez que passa aqui subtrai 1
        j -= 1
        # Quando chega no 1 ele volta para o 9
        if j == 1:
            j = 9
        # Calcula o resto da divisão da soma por 11,
    resto = soma % 11
    # Caso o resto da divisão seja menor que 2 o primeiro digito vai ser 0
    if resto < 2:
        digito_verificador_1 = 0
    # Caso seja maior que dois fazer resto - 11
    else:
        digito_verificador_1 = 11 - resto
    
    # Calcula o segundo dígito verificador
    soma = 0
    j = 6
    for i in range(13):
        soma += int(cnpj[i]) * j
        j -= 1
        if j == 1:
            j = 9
    resto = soma % 11
    if resto < 2:
        digito_verificador_2 = 0
    else:
        digito_verificador_2 = 11 - resto
    
    # Verifica se os dígitos verificadores calculados coincidem com os dígitos originais
    if int(cnpj[12]) == digito_verificador_1 and int(cnpj[13]) == digito_verificador_2:
        return True
    else:
        return False

# Verifica se usuario é maior de idade
def verificarIdade(data_nascimento):
    # Calcula a data atual
    data_atual = date.today()

    # Calcula a data há 18 anos atrás
    data_limite = data_atual.replace(year=data_atual.year - 18)

    # Compara a data de nascimento com a data limite
    return data_nascimento <= data_limite

# Coletar dados da bike 
def coleta_dados_bike():
    try:
        while True:
            qtd_bike = int(input("Informe quantas bicicletas deseja cadastrar: "))
            if qtd_bike > 0:
                break
            else:
                print("Quantidade invalida")

        for i in range(qtd_bike):
            dados = []
            bike = {}
            print(f"Bicicleta {i + 1}:")
            Marca = input("Digite a Marca da bike: ")
            bike["Marca"] = Marca
            Numeracao = float(input("Digite a numeração da bike: "))
            bike["Numeracao"] = Numeracao
            cor = input("Digite a cor da bike (Ex: Amarela, Preta): ")
            cores = [cor.strip() for cor in cor.split(',')]
            if len(cores) >= 1:
                cor1 = cores[0]
            if len(cores) >= 2:
                cor2 = cores[1]
            bike["cores"] = cores
            while True:
                # valida data
                ano_bike = int(input("Digite o ano de fabricação da bike: "))
                if  ano_bike < date.today().year:
                    bike["Ano"] = ano_bike
                    break
                else:
                    print("Data invalida. Tente Novamente")
            while True:
                # validavalor
                valor_mercado = float(input("Digite o valor de mercado da bike: "))
                if valor_mercado >= 2000:
                    bike["Valor de Mercado"] = valor_mercado
                    break
                else:
                    print("Valor deve ser maior que 2000. Digite Novamente")
            funcao = input("Digite a função da bike (ex: Trabalho, lazer, competição): ")
            if funcao.replace(" ", "").isalpha():
                bike["Função"] = funcao
            else:
                print("Por favor, digite um nome válido contendo apenas letras e espaços. Tente novamente.")
            modelo = input("Informe o modelo da sua bike (Ex: Bmx, Dobrável, Elétrica, Elétrica e Dobrável, Downhill, etc): ")
            if modelo.replace(" ", "").isalpha():
                bike["Modelo"] = modelo
            else:
                print("Por favor, digite um nome válido contendo apenas letras e espaços. Tente novamente.")
            dados.append(bike)
    except ValueError:
        print("Valor de entrada invalido")
    return dados

# Menu para escolher se a bike possui acessórios
def menu_acessorio():
    while True:
        print('''
================== Acessório ==================
(1) Caso sua bike tenha acessórios
(2) Caso não tenha acessórios
===============================================''')
        try:
            escolha_acessorio = int(input("Escolha: "))
            list_escolha_acessorio = (1,2)

            if escolha_acessorio in list_escolha_acessorio:
                return escolha_acessorio
            else:
                print("Escolha inválida. Tente novamente.")
        except ValueError:
                print ("Valor de entrada incorreta. Tente novamente.")

# Coletar informações sobre acessórios
def acessorios(escolha_acessorio):
    lista_acessorios = []
    match escolha_acessorio:
        case 1: 
            qtd = int(input("Quantos acessórios deseja cadastrar: "))
            for _ in range(qtd):
                acessorio = input("Nome do acessório: ")
            while True:
                try:
                    preco = float(input(f"Preço do acessório '{acessorio}': "))
                    break
                except ValueError:
                    print("Preço inválido. Insira um valor numérico válido.")

            lista_acessorios.append({"Acessório": acessorio, "Preço": preco})
            return lista_acessorios
        case 2:
            print("sem acessorios")
            return None
        case _:
            print("Escolha inválida.")

# Função para corrigir dados do usuário TERMINARRRARARARARARARRA
def corrigir_dados(dados_cadastro):
    print (''' 
    oq deseja alterar
    (1) Dados do Cadastro
    (2) dados da bike
    (3) Sair
''')
    try:
        escolha_correcao = int(input("Escolha: "))
        match escolha_correcao:
            case 1:
                while True:
                    print("O que você deseja corrigir?")
                    print("(1) Nome")
                    print("(2) CPF")
                    print("(3) Endereço")
                    print("(4) Telefone")
                    print("(5) E-mail")
                    print("(6) Data de Nascimento")
                    print("(7) Sair")
                    
                    escolha_alteracao = int(input("Escolha a opção desejada: "))
                    
                    match escolha_alteracao:
                        case 1:
                            dados_cadastro['Nome'] = input("Novo nome: ")
                        case 2:
                            novo_cpf = input("Novo CPF: ")
                            if Verifica_cpf([int(c) for c in novo_cpf if c.isdigit()]):
                                dados_cadastro['Cpf'] = novo_cpf
                            else:
                                print("CPF inválido. Tente novamente.")
                        case 3:
                            dados_cadastro['Endereço'] = input("Novo endereço: ")
                        case 4:
                            dados_cadastro['Telefone'] = input("Novo telefone: ")
                        case 5:
                            dados_cadastro['E-mail'] = input("Novo e-mail: ")
                        case 6:
                            nova_data = input("Nova data de nascimento (AAAA-MM-DD): ")
                            try:
                                dia, mes, ano = map(int, nova_data.split('-'))
                                nova_data_nascimento = date(ano, mes, dia)
                                if verificarIdade(nova_data_nascimento):
                                    dados_cadastro['Data de Nascimento'] = nova_data_nascimento
                                else:
                                    print("Você deve ter pelo menos 18 anos para se cadastrar.")
                            except ValueError:
                                print("Data de nascimento inválida. Tente novamente.")
                        case _:
                            print("Opção inválida. Tente novamente.")
                    return dados_cadastro
            case 2:
                        print("O que você deseja corrigir nesta bicicleta?")
                        print("(1) Marca")
                        print("(2) Numeração")
                        print("(3) Cores")
                        print("(4) Ano de Fabricação")
                        print("(5) Valor de Mercado")
                        print("(6) Função")
                        print("(7) Modelo")
                        print("(8) Sair da correção desta bicicleta")
                        
                        escolha_alteracao = int(input("Escolha a opção desejada: "))
            case 3:
                print("Saindo da correção de dados.")
            case _:
                print
    except ValueError:
        print ("Valor de entrada incorreta. Tente novamente.")

def calcular_preco_total(dados):
    preco_total = 0.0
    for bike in dados:
        valor_mercado = bike.get("Valor de Mercado", 0.0)  # Obtém o valor de mercado da bicicleta
        acessorios = bike.get("Acessórios", [])  # Obtém a lista de acessórios da bicicleta
        preco_acessorios = sum(acessorio.get("Preço", 0.0) for acessorio in acessorios)  # Soma os preços dos acessórios
        preco_total += valor_mercado + preco_acessorios  # Adiciona o valor de mercado e o preço dos acessórios

    return preco_total

# Exibir os dados da bike e acessórios
def exibir_dados(dados, dados_cadastro):
    print("=============== CONFIRMAÇÃO DE DADOS ================")
    print("Dados do Cadastro:")
    for key, value in dados_cadastro.items():
        print(f"{key}: {value}")

    for i, bike in enumerate(dados):
        print(f"\nCadastro da Bicicleta {i + 1}:")
        for key, value in bike.items():
            if key == "Acessórios":
                print(f"{key}:")
                for acessorio_item in value:
                    print(f"{acessorio_item}")
            else:
                print(f"{key}: {value}")
    preco_total = calcular_preco_total(dados)
    print(f"Preço total de todas as bicicletas com acessórios: R${preco_total:.2f}")

    try:
        confirma = input("\n(sim) se os dados estão corretos. (não) caso não estejam corretos: ")
        if confirma.lower() == 'não' or confirma.lower() == 'n':
            # Se o usuário optar por corrigir os dados, chame a função corrigir_dados
            dados_cadastro = corrigir_dados(dados_cadastro)
            # Exibe os dados corrigidos
            exibir_dados(dados, dados_cadastro)
        else:
            print("Etapa Concluída.")
    except ValueError:
        print ("Valor de entrada incorreta. Tente novamente.")

# Função principal
def principal():
    # Chama a função para escolher o tipo de pessoa
    escolha = menu_pessoa()
    # Faz o login de acordo com a escolha
    tipo_pessoa = Cadastro(escolha)

    if 'nome' in tipo_pessoa:
        print(f"\nSeja Bem-vindo {tipo_pessoa['Nome']}")
    else:
        print("Nome não encontrado nos dados do tipo_pessoa.")

    # Coleta dados sobre bicicletas
    dados = coleta_dados_bike()
    # Loop para cada bicicleta
    for i in range(len(dados)):
        # Exibe o número da bicicleta
        print(f"\nCadastro da Bicicleta {i + 1}")
        # Permite ao usuário escolher se a bicicleta possui acessórios
        escolha_acessorio = menu_acessorio()
        # Coleta informações sobre os acessórios
        acessorio = acessorios(escolha_acessorio)
        if acessorio:
            # Adiciona os acessórios aos dados da bicicleta
            dados[i]["Acessórios"] = acessorio.get("Acessórios", []) 

    # Exibe todos os dados coletados
    exibir_dados(dados, tipo_pessoa)

    # Agora, você pode chamar funções relacionadas ao banco de dados
    if tabela_existe('T_MGT_CADASTRO_PESSOA_FISICA'):
        print("...")
    else:
        criar_tabela_cadastro_pessoa_fisica()
    inserir_dados_cadastro_pessoa_fisica(tipo_pessoa)
    
    if tabela_existe('T_MGT_BIKE'):
        print("...")
    else:
        criar_tabela_bike()
    inserir_dados_bike(dados)

    if tabela_existe('T_MGT_ACESSORIO'):
        print("...")
    else:
        criar_tabela_acessorio()
    inserir_acessorios_bike()

#PRICIPAL
principal()