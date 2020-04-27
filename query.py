import time
import mysql.connector

# Dados para insercao nas 'string queries'
assunto_humd = "Humidade excedida"
assunto_temp = "Temperatura excedida"
prioridade =  0
area = 3
texto_humd =  "O sensor do laboratório está acusando uma humidade maior que 60%"
texto_temp =  "O sensor do laboratório está acusando uma temperatura maior que 30°C"
data = time.strftime('%Y-%m-%d %H:%M:%S')
id_colaborador = 7
mac = "b8:27:eb:9c:07:48"
departamento = 3
status = 0
atendente = 0

# 'String queries' para chamados
query_fields = "INSERT INTO chamado(assunto, prioridade, area, texto, id_colaborador, data, mac, departamento, status, atendente) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
query_values_humd = (assunto_humd, prioridade, area, texto_humd, id_colaborador, data, mac, departamento, status, atendente)
query_values_temp = (assunto_temp, prioridade, area, texto_temp, id_colaborador, data, mac, departamento, status, atendente)

# Variavel global para receber o resultado de uma query
query_result = "receives string result"

def query_and_print(cursor, string_query):
    """ Realiza uma query no banco de dados e printa o resultado no console"""
    cursor.execute(string_query)
    ret = cursor.fetchall()
    for x in ret:
        print(x)

def query_and_save(cursor, string_query):
    """ Realiza uma query no banco de dados e salva o resultado em uma variavel 
    global chamada 'query_result'"""
    global query_result
    cursor.execute(string_query)
    query_result = cursor.fetchall()
    
def query(cursor, string_query):
    """ Realiza uma query no banco de dados"""
    cursor.execute(string_query)

def query_chamado(cursor, string_query_fields, string_query_values):
    """ Realiza uma query para criar um chamado no banco de dados"""
    cursor.execute(string_query_fields, string_query_values)