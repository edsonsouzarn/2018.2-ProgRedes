#!/usr/bin/env python3

import cgi

form = cgi.FieldStorage()

print ("Content-type: text/html\n\n" )
print ("<html><body>")
print ("Nome: {}".format(form.getvalue("nome")))
print ("<br>Senha: {}".format(form.getvalue("senha")))
print ("<br>Sexo: {}".format(form.getvalue("sexo")))
print ("<br>Estado Civil: {}".format(form.getvalue("estado_civil")))
print ("</body></html>")
