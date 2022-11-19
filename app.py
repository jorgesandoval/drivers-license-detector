from flask import Flask
from flask_restful import Api
from resources.images import ImageREST

app = Flask(__name__)
api = Api(app)

api.add_resource(ImageREST,'/images/<string:file>')

if __name__ == '__main__':
    app.run(debug=True)