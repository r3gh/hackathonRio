
# -*- coding: utf-8 -*-
from flasgger.utils import swag_from
from flask import Blueprint
from flask import Response
from flask import request
from flask import jsonify
import json
import os
from api.src.postgre import Postgres

violence_blueprint = Blueprint('violence_blueprint', __name__, url_prefix="/violence")


@violence_blueprint.route("/get", methods=['GET'])
@swag_from('get_all.yml')
def list_all():
  postgre = Postgres()
  postgre.open()
  results = postgre.getVeolance(0);
  postgre.close()
  violences = fromResultsToJson(results)
  return Response(json.dumps(violences),
                      status=200, mimetype='application/json')


@violence_blueprint.route("/get/<quantidade>", methods=['GET'])
@swag_from('get_size.yml')
def list(quantidade):
  postgre = Postgres()
  postgre.open()
  results = postgre.getVeolance(quantidade);
  postgre.close()
  violences = fromResultsToJson(results)
  return Response(json.dumps(violences),
                      status=200, mimetype='application/json')


def fromResultsToJson(results):
  violences = []
  for result in results: 
    violence = {
      'title': result[0],
      'latitude': str(result[1]),
      'longitude': str(result[2]),
      'event_data': result[3].strftime('%Y-%m-%d %H:%M:%S'),
      'bulletin_occurrence': result[4],
      'damage_value': str(result[5]),
      'neighborhood': result[6],
      'county': result[7],
      'name': result[8],
      'type': str(result[9]),
      'description': result[10],
      'sex': str(result[11]),
      'address': result[12],
      'source': result[13],
      'day_of_week': result[14],
      'shift': result[15],
      'source': result[16]
    }
    violences.append(violence)
  return violences
  