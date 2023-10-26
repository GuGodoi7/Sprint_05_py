import oracledb 

def tabela_existe(nome_tabela):
    try:
        connection = obter_connection()
        cursor = connection.cursor()

        # Consulta para verificar a existência da tabela
        sql_query = f"SELECT table_name FROM user_tables WHERE table_name = '{nome_tabela.upper()}'"
        cursor.execute(sql_query)

        # Verifique se a tabela foi encontrada
        return cursor.fetchone() is not None
    except Exception as e:
        print(f"Erro ao verificar a existência da tabela: {e}")
        return False
    finally:
        close_connection(connection)

def obter_connection():
    try:
        connection = oracledb.connect(user="RM99585", password="210305", host="oracle.fiap.com.br", port=1521, service_name="orcl")
        return connection
    except Exception as e:
        print(f"Erro ao obter conexão: {e}")
        return None

def criar_tabela_cadastro_pessoa_fisica():
    try:
        connection = obter_connection()
        cursor = connection.cursor()
        sql_query = """
        CREATE TABLE T_MGT_CADASTRO_PESSOA_FISICA (
            NM_CLIENTE VARCHAR2(100) NOT NULL,
            NR_CPF VARCHAR2(11) NOT NULL,
            NM_ENDEREÇO VARCHAR2(100) NOT NULL,
            NR_TELEFONE VARCHAR2(20) NOT NULL,
            NM_EMAIL VARCHAR2(100) NOT NULL,
            DT_NASCIMENTO DATE NOT NULL
        )
        """
        cursor.execute(sql_query)
        connection.commit()
        print("Tabela CADASTRO criada com sucesso.")
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
    finally:
        close_connection(connection)

def criar_tabela_cadastro_pessoa_juridica():
    try:
        connection = obter_connection()
        cursor = connection.cursor()
        sql_query = """
        CREATE TABLE CADASTRO_PESSOA_JURIDICA (
            NM_EMPRESA VARCHAR2(100) NOT NULL,
            NR_CPF NUMERIC(11) NOT NULL,
            NM_ENDERECO VARCHAR2(100) NOT NULL,
            NR_TELEFONE VARCHAR2(20) NOT NULL,
            NM_EMAIL VARCHAR2(100) NOT NULL,
            DT_FUNDACAO DATE NOT NULL
        )
        """
        cursor.execute(sql_query)
        connection.commit()
        print("Tabela CADASTRO criada com sucesso.")
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
    finally:
        close_connection(connection)

def criar_tabela_bike():
    try:
        connection = obter_connection()
        cursor = connection.cursor()
        sql_query = """
        CREATE TABLE T_MGT_BIKE (
            NM_MARCA VARCHAR2(50) NOT NULL,
            NR_REGISTRO VARCHAR2 (20) NOT NULL,
            NM_COR VARCHAR2(20) NOT NULL,
            DT_BIKE VARCHAR2(4) NOT NULL,
            VL_MERCADO VARCHAR2 (15) NOT NULL,
            NM_FUNCAO VARCHAR2(30) NOT NULL,
            NM_MODELO VARCHAR(30) NOT NULL
         )
        """
        cursor.execute(sql_query)
        connection.commit()
        print("Tabela BIKE criada com sucesso.")
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
    finally:
        close_connection(connection)

def criar_tabela_acessorio():
    try:
        connection = obter_connection()
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE acessorios (
                id NUMBER PRIMARY KEY,
                nome VARCHAR2(255),
                preco NUMBER
            )
        ''')
        connection.commit()
        cursor.close()
        print("Tabela CADASTRO criada com sucesso.")
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
    finally:
        close_connection(connection)

def select_cadastro():
    try:
        connection = obter_connection()
        cursor = connection.cursor()
        sql_query = "SELECT * FROM CT_MGT_CADASTRO_PESSOA_FISICA" 
        cursor.execute(sql_query)
        for result in cursor:
            print(result)
    except Exception as e:
        print(f"{e}")
    finally:
        close_connection(connection)

def select_bike():
    try:
        connection = obter_connection()
        cursor = connection.cursor()
        sql_query = "SELECT * FROM T_MGT_BIKE"
        cursor.execute(sql_query)
        for result in cursor:
            print(result)
    except Exception as e:
        print(f"{e}")
    finally:
        close_connection(connection)

def inserir_dados_cadastro_pessoa_fisica(dados_cadastro):
    try:
        connection = obter_connection()
        cursor = connection.cursor()
        sql_query = """
        INSERT INTO T_MGT_CADASTRO_PESSOA_FISICA (NM_CLIENTE, NR_CPF, NM_ENDEREÇO, NR_TELEFONE, NM_EMAIL, DT_NASCIMENTO) 
        VALUES (:nome, :cpf, :endereco, :telefone, :email, :nascimento)
        """
        cursor.execute(sql_query, {
            'nome': dados_cadastro['Nome'],
            'cpf': dados_cadastro['Cpf'],
            'endereco': dados_cadastro['Endereço'],
            'telefone': dados_cadastro['Telefone'],
            'email': dados_cadastro['E-mail'],
            'nascimento': dados_cadastro['Data de Nascimento']
        })
        connection.commit()
        print("Dados inseridos com sucesso.")
    except Exception as e:
        print(f"Erro ao inserir dados na tabela: {e}")
    finally:
        close_connection(connection)

def inserir_dados_pessoa_juridica(dados_juridicos):
    try:
        connection = obter_connection()
        cursor = connection.cursor()
        
        sql_query = """
        INSERT INTO CADASTRO_PESSOA_JURIDICA (NM_EMPRESA, NR_CNPJ, NM_ENDERECO, NR_TELEFONE, NM_EMAIL, DT_FUNDACAO)
        VALUES (:nome_empresa, :cnpj, :endereco, :telefone, :email, :data_fundacao)
        """
        cursor.execute(sql_query, {
            'nome_empresa': dados_juridicos['Nome'],
            'cnpj': dados_juridicos['Cnpj'],
            'endereco': dados_juridicos['Endereço'],
            'telefone': dados_juridicos['Telefone'],
            'email': dados_juridicos['E-mail'],
            'data_fundacao': dados_juridicos['Data de Fundação']
        })

        connection.commit()
        print("Dados de pessoa jurídica inseridos com sucesso.")
    except Exception as e:
        print(f"Erro ao inserir dados de pessoa jurídica na tabela: {e}")
    finally:
        close_connection(connection)

def inserir_dados_bike(dados_bike):
    try:
        connection = obter_connection()
        cursor = connection.cursor()

        for bike in dados_bike:
            cores = bike['cores']
            for cor in cores:
                sql_query = sql_query = """
                INSERT INTO T_MGT_BIKE (NM_MARCA, NR_REGISTRO, NM_COR, DT_BIKE, VL_MERCADO, NM_FUNCAO, NM_MODELO) 
                VALUES (:marca, :registro, :cor, :data_bike,  :valor_mercado, :funcao, :modelo)
                """
                cursor.execute(sql_query, {
                'marca': bike['Marca'],
                'registro': bike['Numeracao'],
                'cor': ', '.join(cores),
                'data_bike': bike['Ano'],
                'valor_mercado': bike['Valor de Mercado'],
                'funcao': bike['Função'],
                'modelo': bike['Modelo']
                })

        connection.commit()
        print("Dados da bicicleta inseridos com sucesso.")
    except Exception as e:
        print(f"Erro ao inserir dados na tabela: {e}")
    finally:
        close_connection(connection)

def inserir_acessorios_bike(lista_acessorios):
    try:
        connection = obter_connection()
        cursor = connection.cursor()
        
        sql_query = """
        INSERT INTO CADASTRO_PESSOA_JURIDICA (NR_PRECO, NM_ACESSORIO)
        VALUES (:preco, :nome)
        """
        cursor.execute(sql_query, {
            'nome_acessorio': lista_acessorios ['acessorio'],
            'preco': lista_acessorios['preco']
        })

        connection.commit()
        print("Dados de pessoa jurídica inseridos com sucesso.")
    except Exception as e:
        print(f"Erro ao inserir dados de pessoa jurídica na tabela: {e}")
    finally:
        close_connection(connection)

def close_connection(connection):
    connection.close()
