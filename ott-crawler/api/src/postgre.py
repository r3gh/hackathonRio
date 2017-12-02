import psycopg2
from datetime import datetime

class Postgres:

  def __init__(self):
    self.conn = None;
  
  def open(self):
    try:
        self.conn = psycopg2.connect("dbname='hackathon' user='postgres' host='localhost' password='123456'")
    except:
        print ("I am unable to connect to the database")

  def insertOndeFoiRoubado(self, json):
    cur = self.conn.cursor()
    hashmap = {}
    print(json[0])
    for idx in range(len(json)):
      hashmap[json[idx]['created_at']]=json[idx]

    for k,violence in hashmap.items():
      strData = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      if violence['created_at'] != None:
        idxEnd = violence['created_at'].find('.')
        violence['created_at'] = violence['created_at'][:idxEnd]
        date = datetime.strptime(violence['created_at'], '%Y-%m-%dT%H:%M:%S');
        strData = date.strftime('%Y-%m-%d %H:%M:%S')
      violence['titulo'] = ( violence['titulo'] if violence['titulo'] != None  else 'Não Informado')
      queryStr = "INSERT INTO violence_data(title, latitude, longitude, event_data) VALUES ('"\
+violence['titulo']+"',"+str(violence['latitude'])+","+str(violence['longitude'])+",'"+ strData +"')"
      try:
        cur.execute(queryStr)
        self.conn.commit()
      except:
        print ("Erro ao inserir")
    cur.close()
   
    
  def close(self):
    try:
      self.conn.close()
    except:
      print ("I am unable to connect to the database")




      {'hashid': 'VKEmM9',
       'registrou_bo': None, 
       'data': '2017-11-29', 
       'uri': '/denuncias/VKEmM9-jovens-da-roda-de-rima-quarta-feira', 
       'valor_prejuizo': '10.0', 
       'votos': 0, 
       'bairro': 'Todos os Santos', 
       'email': '', 'hora': '2000-01-01T21:30:32.000Z', 
       'gmaps': None, 
       'titulo': 
       'Jovens da roda de rima (Quarta feira)', 
       'municipio_id': 3654, 
       'nome': None, 
       'ip_address_origin': None, 
       'aasm_state': 'active', 
       'id': 86488, 
       'longitude': -43.2836724479575, 
       'tipo_assalto_id': 10, 
       'latitude': -22.8979315656398, 
       'updated_at': '2017-11-30T11:44:26.575-02:00', 
       'descricao': 'Segundo a vítimas, um grupo elementos de pele escura saíram de um carro prata, posteriormente roubado, onde elementos  realizaram o arrastão, além dos jovens que estavam na praça bebendo e conversando, moradores que passavam pelo local também foram abordados e quem observada de longe conseguiram correr dos assaltantes entrando em condomínios nas proximidades.', 
       'created_at': '2017-11-30T11:44:26.575-02:00', 
       'sexo': 1, 
       'ativo': False, 
       'data_hora_registro': None, 
       'user_id': None, 
       'endereco': 'Rua Silva Rabelo, 156, Todos os Santos'}
