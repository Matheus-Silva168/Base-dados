import mysql.connector
from mysql.connector import Error


def criar_conexao():
    #Conecta a uma database do MySQL
    conexao = None
    try:
        conexao = mysql.connector.connect(
            host='SEU HOST',
            user='SEU USUARIO',
            password='SUA SENHA',
            database='SUA DATABASE'
        )
        if conexao.is_connected():
            print("Conexão com o MySQL estabelecida com sucesso!")
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
    return conexao


def criar_tabela(conexao):
    # Cria uma tabela na database do MySQL
    cursor = conexao.cursor()
    query = '''
    CREATE TABLE IF NOT EXISTS pagamentos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        valor DECIMAL(10, 2) NOT NULL,
        data_vencimento DATE NOT NULL
    )
    '''
    try:
        cursor.execute(query)
        print("Tabela criada com sucesso")
    except Error as e:
        print(f"Erro ao criar a tabela no MySQL: {e}")


def inserir_pagamento(conexao, nome,  valor, data_vencimento):
    # Insere um resgistro na tabela
    cursor = conexao.cursor()
    query = 'INSERT INTO pagamentos (nome, valor, data_vencimento) VALUES (%s, %s, %s)'
    try:
        cursor.execute(query, (nome, valor, data_vencimento))
        conexao.commit()
        print("Registro concluido")
    except Error as e:
        print(f"Erro ao inserir o registro: {e}")


def ler_pagamento(conexao):
    # Lê a tabela
    cursor = conexao.cursor()
    query = f'SELECT * FROM pagamentos'
    cursor.execute(query)
    print(cursor.fetchall())


def atualizar_pagamento(conexao, nome, valor):
    # Atualiza valores na tabela
    cursor = conexao.cursor()
    query = f'UPDATE pagamentos SET valor = {valor} WHERE nome = "{nome}"'
    cursor.execute(query)
    conexao.commit()


def deletar_pagamento(conexao, nome):
    cursor = conexao.cursor()
    query = f'DELETE FROM pagamentos WHERE nome = "{nome}"'
    cursor.execute(query)
    conexao.commit()


def menu():
    # Menu principal
    while True:
        print('\nOPÇÕES\n')
        opcao=int(input('1 - Inserir pagamento.\n2 - Mostrar tabela.\n3 - Atualizar entrada.\n4 - Deletar entrada.\n5 - Sair.\n'))
        if opcao in range(1, 6):
            return opcao
            break


def main():
    conexao = criar_conexao()
    if conexao is not None and conexao.is_connected():
        criar_tabela(conexao)
        while True:
            opcao = menu()
            if opcao == 1:
                nome = input("Digite o nome: ")
                valor = float(input("Digite o valor: R$ ").strip())
                data_vencimento = input("Digite a data de vencimento (YYYY-MM-DD): ").strip()
                inserir_pagamento(conexao, nome, valor, data_vencimento)
            if opcao == 2:
                ler_pagamento(conexao)
            if opcao == 3:
                nome = input("Digite o nome: ")
                valor = float(input("Digite o novo valor: R$ ").strip())
                atualizar_pagamento(conexao, nome, valor)
            if opcao == 4:
                nome = input("Digite o nome da entrada que deseja apagar: ")
                deletar_pagamento(conexao, nome)
            if opcao == 5:
                break
        conexao.close()


if __name__ == "__main__":
    main()