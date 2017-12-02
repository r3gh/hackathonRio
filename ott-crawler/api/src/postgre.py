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

    for idx in range(len(json)):
      strData = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      if json[idx]['created_at'] != None:
        idxEnd = json[idx]['created_at'].find('.')
        json[idx]['created_at'] = json[idx]['created_at'][:idxEnd]
        date = datetime.strptime(json[idx]['created_at'], '%Y-%m-%dT%H:%M:%S');
        strData = date.strftime('%Y-%m-%d %H:%M:%S')
      json[idx]['created_at'] = strData
      hashmap[json[idx]['created_at']]=json[idx]

    for k,violence in hashmap.items():
      violence['titulo']  = (violence['titulo'] if violence['titulo'] != None  else 'Não Informado')
      violence['registrou_bo']  = (str(violence['registrou_bo']) if str(violence['registrou_bo']) != None  else 'Não Informado')
      violence['valor_prejuizo']  = (violence['valor_prejuizo'] if violence['valor_prejuizo'] != None  else 'Não Informado')
      violence['bairro']  = (violence['bairro'] if violence['bairro'] != None  else 'Não Informado')
      violence['nome']  = (violence['nome'] if violence['nome'] != None  else 'Não Informado')
      violence['tipo_assalto_id']  = (str(violence['tipo_assalto_id']) if str(violence['tipo_assalto_id']) != None  else 'Não Informado')
      violence['descricao']  = (violence['descricao'] if violence['descricao'] != None  else 'Não Informado')
      violence['sexo']  = (str(violence['sexo']) if str(violence['sexo']) != None  else 'Não Informado')
      violence['endereco']  = (violence['endereco'] if violence['endereco'] != None  else 'Não Informado')
      violence['municipio_id']  = (str(violence['municipio_id']) if str(violence['municipio_id']) != None  else 'Não Informado')
      
      queryStr = "INSERT INTO violence_data(title, latitude, longitude, event_data, bulletin_occurrence,damage_value, neighborhood, county,name,type_violence,description,sex,address,source) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
      try:
        cur.execute(queryStr,(violence['titulo'],str(violence['latitude']),str(violence['longitude']),violence['created_at'], violence['registrou_bo'],violence['valor_prejuizo'],violence['bairro'],violence['municipio_id'],violence['nome'],violence['tipo_assalto_id'],violence['descricao'],str(violence['sexo']),violence['endereco'],'ONDE_FOI_ROUBADO'))
        self.conn.commit()
      except psycopg2.Error as e:
        a = 1;
    cur.close()

  def insertOndeTemTiro(self, json):
    cur = self.conn.cursor()
    for violence in json['rows']:
      descriptionArray = violence[0].split("#")
      strData = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      if descriptionArray[1] != None:
        date = datetime.strptime(descriptionArray[1], '%d/%m/%Y às %H:%M');
        strData = date.strftime('%Y-%m-%d %H:%M:%S')

      queryStr = "INSERT INTO violence_data(title, latitude, longitude, event_data, bulletin_occurrence,damage_value, neighborhood, county,name,type_violence,description,sex,address,source) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
      try:
        cur.execute(queryStr,(descriptionArray[3],str(violence[4]),str(violence[5]),strData, 'Não Informado',0,violence[1].split(',')[1],'Não Informado',violence[2],0,descriptionArray[3],'Não Informado',violence[1],'ONDE_TEM_TIRO'))
        self.conn.commit()
      except psycopg2.Error as e:
        print(e)
    cur.close()
     
      
  def close(self):
    try:
      self.conn.close()
    except:
      print ("I am unable to connect to the database")


