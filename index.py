import sqlite3

# Função para extrair as linhas que contêm "registrationID":""
def extract_registration_ids(filename):
    registration_ids = []

    with open(filename, 'r') as file:
        for line in file:
            if '"registrationID": "' in line:  # Note o espaço extra aqui
                # Extrair o valor após "registrationID": "
                start_index = line.find('"registrationID": "') + len('"registrationID": "')
                end_index = line.find('"', start_index)
                reg_id = line[start_index:end_index].strip()  # Use strip() para remover espaços em branco extras
                registration_ids.append(reg_id)

    return registration_ids

# Nome do arquivo que você deseja processar (certifique-se de que o caminho esteja correto)
arquivo = '/home/usuario/pasta/arquivo.txt'

try:
    # Conectar-se ao banco de dados (ou criá-lo se não existir)
    connection = sqlite3.connect('nome_banco.db')  # Substitua pelo nome que desejar

    # Criar uma tabela para armazenar os registration IDs
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registration_ids (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_id TEXT UNIQUE
        )
    ''')

    # Extrair os registration IDs do arquivo
    registration_ids = extract_registration_ids(arquivo)

    # Inserir IDs no banco de dados
    for reg_id in registration_ids:
        cursor.execute("INSERT OR IGNORE INTO registration_ids (registration_id) VALUES (?)", (reg_id,))

    # Commit (salvar) as alterações e fechar a conexão com o banco de dados
    connection.commit()
    connection.close()

    print(f"Foram armazenados {len(registration_ids)} IDs no banco de dados.")
except Exception as e:
    print(f"Ocorreu um erro: {str(e)}")
