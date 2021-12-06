import json
import flask
from flask_restful import Resource, Api
from Constants import Constants
from exception.IllegalArgumentException import IllegalArgumentException
from service.GetCoordinatesService import GetCoordinates
from flask import request

app = flask.Flask(__name__)
api = Api(app)

class GeoAPI(Resource):
    def get(self):
        return getCoordinates.getCoordinates(Constants.ADDRESS_FOR_TASK_FILE_PATH)

    def post(self):
        data = json.loads(flask.request.data.decode('utf-8'))
        if(data == None or data['address'] == None or data['address'] == ''):
            raise IllegalArgumentException('Please enter a valid address and try again.')
        return getCoordinates.getCoordinatesForAddressString(data['address'])

api.add_resource(GeoAPI, '/')

if __name__ == '__main__':
    getCoordinates = GetCoordinates()
    app.run(port='8080', debug=True)
