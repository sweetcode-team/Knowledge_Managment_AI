from flask import Blueprint, jsonify
import json

from adapter._in.web.get_configuration_controller import GetConfigurationController
from application.service.get_configuration_service import GetConfigurationService

from adapter.out.get_configuration.get_configuration_postgres import GetConfigurationPostgres
from adapter.out.persistence.postgres.postgres_configuration_orm import PostgresConfigurationORM

getConfigurationBlueprint = Blueprint("getConfiguration", __name__)

@getConfigurationBlueprint.route('/getConfiguration', methods=['GET'])
def getConfiguration():
    
    controller = GetConfigurationController(
        GetConfigurationService(
            GetConfigurationPostgres(PostgresConfigurationORM())
        )
    )
    
    configuration = controller.getConfiguration()
    
    if configuration is None:
        return jsonify({}), 404

    return jsonify({
        "vectorStore": {
            "name": configuration.vectorStore.name.name,
            "organization": configuration.vectorStore.organization,
            "description": configuration.vectorStore.description,
            "type": configuration.vectorStore.type,
            "costIndicator": configuration.vectorStore.costIndicator},
        "documentStore": {
            "name": configuration.documentStore.name.name,
            "organization": configuration.documentStore.organization,
            "description": configuration.documentStore.description,
            "type": configuration.documentStore.type,
            "costIndicator": configuration.documentStore.costIndicator},
        "embeddingModel": {
            "name": configuration.embeddingModel.name.name,
            "organization": configuration.embeddingModel.organization,
            "description": configuration.embeddingModel.description,
            "type": configuration.embeddingModel.type,
            "costIndicator": configuration.embeddingModel.costIndicator},
        "LLMModel": {
            "name": configuration.LLMModel.name.name,
            "organization": configuration.LLMModel.organization,
            "description": configuration.LLMModel.description,
            "type": configuration.LLMModel.type,
            "costIndicator": configuration.LLMModel.costIndicator
        }
    })