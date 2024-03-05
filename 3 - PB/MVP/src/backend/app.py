from flask import Flask
from flask_cors import CORS

from blueprints.upload_documents import uploadDocumentsBlueprint
from blueprints.delete_documents import deleteDocumentsBlueprint

app = Flask(__name__)
CORS(app)

app.register_blueprint(uploadDocumentsBlueprint)
app.register_blueprint(deleteDocumentsBlueprint)