import psycopg2

# Configurações de conexão
db_config = {
    'dbname': 'banco_teste',
    'user': 'postgres',
    'password': 'Luna1!',
    'host': 'localhost',  # ou o endereço do seu servidor de banco de dados
    'port': '5432'  # porta padrão do PostgreSQL
}

# Função para conectar ao banco de dados
def connect():
    try:
        conn = psycopg2.connect(**db_config)
        return conn
    except (Exception, psycopg2.Error) as error:
        print("Erro ao conectar ao PostgreSQL:", error)
        return None

def create_table(nome_tabela):
    conn = connect()
    if conn:
        cursor = conn.cursor()
        create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {nome_tabela} (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            altura NUMERIC(5, 2) NOT NULL,
            peso NUMERIC(5, 2) NOT NULL
        );
        '''
        cursor.execute(create_table_query)
        conn.commit()
        cursor.close()
        conn.close()
        print("Tabela criada com sucesso!")

def add_pessoa(nome: str, altura: float, peso: float):
    conn = connect()
    if conn:
        cursor = conn.cursor()
        insert_query = '''
        INSERT INTO pessoa (nome, altura, peso) VALUES (%s, %s, %s)
        RETURNING id;
        '''
        cursor.execute(insert_query, (nome, altura, peso))
        conn.commit()
        pessoa_id = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        print(f"Pessoa com ID {pessoa_id} adicionada com sucesso!")

def listar_pessoas():
    conn = connect()
    if conn:
        cursor = conn.cursor()
        select_query = '''
        SELECT * FROM pessoa;
        '''
        cursor.execute(select_query)
        pessoas = cursor.fetchall()
        cursor.close()
        conn.close()
        for pessoa in pessoas:
            print(f"ID: {pessoa[0]}, Nome: {pessoa[1]}, Altura: {pessoa[2]}, Peso: {pessoa[3]}")

def update_person(pessoa_id: int, nome: str=None, altura: float=None, peso: float=None):
    conn = connect()
    if conn:
        cursor = conn.cursor()
        update_query = '''
        UPDATE pessoa SET nome = %s, altura = %s, peso = %s WHERE id = %s;
        '''
        cursor.execute(update_query, (nome, altura, peso, pessoa_id))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Pessoa com ID {pessoa_id} atualizada com sucesso!")

# Função para deletar uma pessoa
def delete_pessoa(pessoa_id: int):
    conn = connect()
    if conn:
        cursor = conn.cursor()
        delete_query = '''
        DELETE FROM pessoa WHERE id = %s;
        '''
        cursor.execute(delete_query, (pessoa_id,))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Pessoa com ID {pessoa_id} deletada com sucesso!")