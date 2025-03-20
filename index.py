import sqlite3
import os

# Caminho do banco de dados no Disco J
db_path = "credilink.db"

# Diretório temporário no Disco J
temp_dir = "J:/temp"

# Garantir que o diretório temporário exista
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

# Conexão com o banco de dados
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Configurar o diretório temporário
    cursor.execute(f"PRAGMA temp_store_directory = '{temp_dir}';")

    # Criar índice na tabela credilink_basic para a coluna nome
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_CBO_credilink ON credilink_basic (nome_mae);
    """)
    
#    CREATE INDEX IF NOT EXISTS idx_CBO_credilink ON credilink_basic (cbo);
#    CREATE INDEX IF NOT EXISTS idx_mae_credilink ON credilink_basic (nome_mae);

    
    conn.commit()
    print("Índice criado com sucesso e arquivos temporários alocados no disco J!")
except sqlite3.Error as e:
    print(f"Erro ao criar índice: {e}")
finally:
    if conn:
        conn.close()
