#!/bin/usr/python3
""" LISTAR-PASS: lista todas as informações.
Principal Referência: https://docs.microsoft.com/pt-br/azure/mysql/connect-python
apt install python3 python3-pip
pip3 install flask mysql-connector-python"""

import os
from flask import Flask
from mysql.connector import errorcode
import mysql.connector

container_atualizar = os.getenv('CONTAINER_ATUALIZAR')
container_listar = os.getenv('CONTAINER_LISTAR')
gerador_pass_port = os.getenv('GERADOR_PASS_PORT')
atualizar_pass_port = os.getenv('ATUALIZAR_PASS_PORT')
listar_pass_port = os.getenv('LISTAR_PASS_PORT')
database_host = os.getenv('DATABASE_HOST')
mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_PASSWORD')
mysql_database = os.getenv('MYSQL_DATABASE')
pontuacao = os.getenv('PONTUACAO') #'@#$%()[]<>'

app = Flask(__name__)
output1 = '''<h1>LISTAR_PASS</h1>
Lista todos os serviços usuários e senhas.
/listar
'''
@app.route('/')
def root_server():
    """ Server Root """
    return output1, 200

@app.route('/listar')
def list_data_base():
    """ Server function listar """
    data_base_config = {
        'host':database_host,
        'user':mysql_user,
        'password':mysql_password,
        'database':mysql_database
    }
    result = [False, "ERRO", 500]
    try:
        conn = mysql.connector.connect(**data_base_config)
        print("Conexao bem sucedida")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("ERRO: Nome ou senha do banco incorretas (permissao)")
            result = [False, "ERRO: Nome ou senha do banco incorretas (permissao)", 501]
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("ERRO: Banco não existe no servidor consultado")
            result = [False, "ERRO: Banco nao existe no servidor consultado", 502]
        else:
            print("ERRO: não identificado no codigo")
            print(err)
            result = [False, "ERRO: não identificado no codigo", 503]
    else:
        cursor = conn.cursor()
        print("Verificando registros na base")
        cursor.execute("SELECT * FROM dados_logon;")
        registers = cursor.fetchall()
        print("Resultado: ", cursor.rowcount, " registros.")
        #result = []
        #for register in registers:
        #    result.append(register)
        conn.commit()
        cursor.close()
        conn.close()
        print("Done.")
        result = [True, registers, 200]
    return result

app.run(host='0.0.0.0', port=listar_pass_port, debug=False)
