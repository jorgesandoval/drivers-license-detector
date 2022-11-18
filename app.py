from flask import Flask, jsonify
from flask_restful import Api
from resources.images import Image

app = Flask(__name__)

# Adding path to config
app.config['INITIAL_FILE_UPLOADS'] = 'static/uploads'
app.config['EXISTNG_FILE'] = 'static/original'
app.config['GENERATED_FILE'] = 'static/generated'

api = Api(app)

api.add_resource(Image,'/')

if __name__ == '__main__':
    app.run(debug=True)