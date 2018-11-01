import psycopg2


strConexao = "dbname=alunos user=postgres host=localhost"
connConexao = psycopg2.connect(strConexao)
curConexao = connConexao.cursor()

curConexao.execute("select * from alunos")

resultado = curConexao.fetchall()

for aluno in resultado:
   print ("Matrícula: {0} Nome: {1} Email: {2}\n".format(aluno[0], aluno[1], aluno[2]))