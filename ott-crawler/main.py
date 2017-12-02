import urllib3
import json

http = urllib3.PoolManager()
r = http.request('GET', 'http://www.ondefuiroubado.com.br/rio-de-janeiro/RJ');
htmlData = str(r.data.decode('utf8'))
idxStart = htmlData.find('OndeFuiRoubado.Views.CrimesIndexView.initialize')
idxEnd = htmlData.find('OndeFuiRoubado.PoliceStations')
htmlData = htmlData[idxStart:idxEnd]
htmlData = htmlData.replace('OndeFuiRoubado.Views.CrimesIndexView.initialize(','')
htmlData = htmlData.strip()
htmlData = htmlData.replace(');\\n  });\\n\\n  document.addEventListener(\\\'onMainMapLoad\\\', function(data) {\\n','')
htmlData = htmlData.strip()
htmlData = htmlData.replace("document.addEventListener('onMainMapLoad', function(data) {",'')
htmlData = htmlData.replace("\n","")
htmlData = htmlData.replace(");  });","")
jsonDataFrom =json.loads(htmlData)