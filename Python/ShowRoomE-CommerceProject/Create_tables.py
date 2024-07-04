from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ModelosEx import Base

# Configuração da conexão com o banco de dados
DATABASE_TYPE = 'mysql'
ENGINE = 'pymysql'
DATABASE_USER = 'userdev'
DATABASE_PASS = 'passdev'
DATABASE_HOST = 'localhost'
DATABASE_PORT = '3306'
DATABASE_NAME = 'project'

# Criando a URL de conexão com o banco de dados
connection_string = f"{DATABASE_TYPE}+{ENGINE}://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

# Criando uma instância do engine
engine = create_engine(connection_string)

# Criando as tabelas no banco de dados
Base.metadata.create_all(engine)

print("Tabelas criadas com sucesso!")