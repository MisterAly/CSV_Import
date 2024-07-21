import psycopg2
import pandas as pd
from psycopg2.extras import execute_values

# Configuração da conexão
host = 'localhost'  # Endereço do servidor PostgreSQL no Docker
port = '5432'  # Porta padrão do PostgreSQL
database = 'dbname'
username = 'postgres'
password = 'PostgresPassword1234'

try:
    # Conectando ao banco de dados
    conn = psycopg2.connect(
        host=host,
        port=port,
        dbname=database,
        user=username,
        password=password
    )
    cursor = conn.cursor()

    # Exemplo: Executando uma query
    print('Versão do PostgreSQL')
    cursor.execute('SELECT version();')
    row = cursor.fetchone()
    print(row[0])

    # Carregar o CSV com o delimitador correto
    csv_file_path = '/Users/alysonwee/Projects/CSV_import/35_SP.csv'
    data = pd.read_csv(csv_file_path, delimiter=';')
    print(f"CSV {csv_file_path} carregado com sucesso: {data.shape[0]} linhas, {data.shape[1]} colunas")

    # Criar a tabela (se não existir)
    create_table_query = """
    CREATE TABLE IF NOT EXISTS tablename (
        columns
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    print("Tabela `tablename` criada ou já existe.")

    # Inserir os dados
    insert_query = f"INSERT INTO SP_IBGE ({', '.join(data.columns)}) VALUES %s"
    values = [tuple(row) for row in data.to_numpy()]
    execute_values(cursor, insert_query, values)

    conn.commit()
    print("Dados inseridos na tabela `tablename` com sucesso.")

except psycopg2.Error as e:
    print(f"Erro PostgreSQL: {e}")

finally:
    if 'conn' in locals():
        conn.close()
