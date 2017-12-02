
# -*- coding: utf-8 -*-
from flasgger.utils import swag_from
from flask import Blueprint
from flask import Response
from flask import request
from flask import jsonify
import json
import os

color_blueprint = Blueprint('color_blueprint', __name__, url_prefix="/color")


@color_blueprint.route("/list/<palette>", methods=['GET'])
@swag_from('index.yml')
def list(palette):
  all_colors = {
    'cmyk': ['cian', 'magenta', 'yellow', 'black'],
    'rgb': ['red', 'green', 'blue']
  }
  if palette == 'all':
    result = all_colors
  else:
    result = {palette: all_colors.get(palette)}

  return jsonify(result)
