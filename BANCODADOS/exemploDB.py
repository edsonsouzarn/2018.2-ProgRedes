import json
import requests
import psycopg2

urls = { "token":"https://suap.ifrn.edu.br/api/v2/autenticacao/token/",
         "dados":"https://suap.ifrn.edu.br/api/v2/minhas-informacoes/meus-dados/"}

autenticacao = {
    "username": "SUA_MATRICULA",
    "password": "SUA_SENHA"
}

strConexaoDefault  = "dbname=postgres user=postgres host=localhost"
strConexaoDBAlunos = "dbname=alunos user=postgres host=localhost"
strSQLCriaDatabase = "CREATE DATABASE alunos"
strSQLCriaTable    = "CREATE TABLE alunos (matricula BIGINT PRIMARY KEY, nome VARCHAR(100), email VARCHAR(200));"


#---------------------------------------------------------------------
# Metodo principal
#---------------------------------------------------------------------
def principal():
   if (table_exists("alunos")):
      print("Banco e tabela encontrados...")
   else:
       print("Criando banco e tabela...")
       criarBanco()
   print("Inserindo os Dados"...)
   insereAluno(iMatricula, sNome, sEmail)


#---------------------------------------------------------------------
# Metodo de obtencao do Token no SUAP
#---------------------------------------------------------------------
def getToken():
   response = requests.post(urls['token'], data=autenticacao)
   if response.status_code == 200:
      return json.loads(response.content.decode('utf-8'))['token']
   return None


cabecalho={'Authorization': 'JWT {0}'.format(getToken())}


#---------------------------------------------------------------------
# Metodo que obtem as informacoes dos alunos
#---------------------------------------------------------------------
def getInformacoes():
    response = requests.get(urls['dados'], headers=cabecalho)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    return None

informacoes = json.loads(getInformacoes())
iMatricula  = int(informacoes['matricula'])
sNome       = informacoes['nome_usual']
sEmail      = informacoes['email']

#---------------------------------------------------------------------
# Metodo que verifica se a tabela existe
#---------------------------------------------------------------------
def table_exists(strNomeTabela):
   exists = False
   try:
      strSQL = "SELECT EXISTS(SELECT relname FROM pg_class WHERE relname='{0}'".format(strNomeTabela)
      con = psycopg2.connect(strConexaoDBAlunos)
      cur = con.cursor()
      cur.execute(strSQL)
      exists = cur.fetchone()[0]
      cur.close()
   except psycopg2.Error as e:
      print (e)
   return exists


#---------------------------------------------------------------------
# Metodo que cria o banco e a tabela
#---------------------------------------------------------------------
def criarBanco():
   from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
   conn = psycopg2.connect(strConexaoDefault)
   conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
   cur = conn.cursor()
   cur.execute(strSQLCriaDatabase)
   conn = psycopg2.connect(strConexaoDBAlunos)
   cur = conn.cursor()
   cur.execute(strSQLCriaTable)
   conn.commit()
   conn.close()


#---------------------------------------------------------------------
# Metodo que insere o aluno no banco
#---------------------------------------------------------------------
def insereAluno(intMatricula,strNome,strEmail):
   conn = psycopg2.connect(strConexaoDBAlunos)
   cur = conn.cursor()
   strSQLInsereDados = "INSERT INTO alunos (matricula, nome, email) VALUES ({0}, '{1}', '{2}')".format(intMatricula,strNome,strEmail)
   cur.execute(strSQLInsereDados)
   conn.commit()
   conn.close()


if __name__ == "__main__": principal()
