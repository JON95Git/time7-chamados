import time
import datetime
import Adafruit_DHT
import mysql.connector
import query

# Valor do conector para uma query com retorno nulo
QUERY_NULL = '[]'

# Dados para utilizacao do sensor DHT22
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
MAX_TEMP = 30 
MAX_HUM = 100

# Dados de conexao com banco de dados
db_host = "projeto.sytes.net"
db_user = "root"
db_passwd = "Projeto@2020!!"
db_database = "sistema"

def get_range_datetime():
    global today_str, earlier_str
    # Obtem a data atual
    today = datetime.datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    print("today_str  : %s" % today_str)
    # Calcula a data de "days" (no caso, 5) dias atras
    DD = datetime.timedelta(days=5)
    earlier = today - DD
    earlier_str = earlier.strftime("%Y-%m-%d")
    print("earlier_str: %s" %earlier_str)

# Conexao com o banco
try: 
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        passwd=db_passwd,
        database=db_database
    )
except:
    print ("ERRO: Nao foi possivel conectar ao banco")
    print ("Verifique os dados de host, user, database e password")
    exit()

# Objeto "cursor" usado para "percorrer" o banco de dados
cursor = connection.cursor()

print ("Conexao realizada com sucesso!")

# Query de teste para printar todas os chamados do banco da area 3 (area tecnica)
# query.query_and_print(cursor, "SELECT * FROM chamado WHERE area = 3")

# Printa informacoes de data e hora
data = time.strftime("%d/%m")
hora = time.strftime("%H:%M")
print (hora)
print (data)

# Obtem a data atual e calcula a data de 5 dias atras
get_range_datetime()

# Query que busca todos os chamados realizados pelo Raspberry Pi num periodo especifico
query.query_and_save(cursor, "select * from chamado where mac = 'b8:27:eb:9c:07:48' and date(data) between '%s' and '%s'" %(earlier_str, today_str))
ret = str(query.query_result)
if ret == QUERY_NULL:
    print("A query nao retornou nenhum resultado")
else:
    for x in query.query_result:
        print(x)

# Loop infinito
# Caso temperatura e humidade excedam o limite, abre chamado
while True:
    dia = time.strftime("%H:%M")
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    print("Temp={0:0.1f}°C  Humidade ={1:0.1f}%".format(temperature, humidity))

    if humidity > MAX_HUM:
        # Obtem a data atual e calcula a data de 5 dias atras
        get_range_datetime()
        # Query que busca todos os chamados realizados pelo Raspberry Pi num periodo especifico
        query.query_and_save(cursor, "select * from chamado where mac = 'b8:27:eb:9c:07:48' and date(data) between '%s' and '%s'" %(earlier_str, today_str))
        ret = str(query.query_result)
        if ret == QUERY_NULL:
            query.query_chamado(cursor, query.query_fields, query.query_values_humd)
            print('Cadastrando chamado do sensor de humidade')
            connection.commit()
        
    if temperature > MAX_TEMP:    
        # Obtem a data atual e calcula a data de 5 dias atras
        get_range_datetime()            
        # Query que busca todos os chamados realizados pelo Raspberry Pi num periodo especifico
        query.query_and_save(cursor, "select * from chamado where mac = 'b8:27:eb:9c:07:48' and date(data) between '%s' and '%s'" %(earlier_str, today_str))
        ret = str(query.query_result)
        if ret == QUERY_NULL:
            # Caso nao haja um chamado aberto num periodo de 5 dias atras, cria um novo chamado
            query.query_chamado(cursor, query.query_fields, query.query_values_temp)
            print('Cadastrando chamado do sensor de temperatura')
            connection.commit()
