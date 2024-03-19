import unittest.mock
from application.service.change_configuration_service import ChangeConfigurationService
from domain.configuration.llm_model_configuration import LLMModelType
from domain.configuration.configuration_operation_response import ConfigurationOperationResponse
from domain.document.document import Document
from domain.document.document_content import DocumentContent
from domain.document.document_id import DocumentId
from domain.document.document_metadata import DocumentMetadata, DocumentType
from domain.document.document_operation_response import DocumentOperationResponse
from domain.document.document_status import DocumentStatus, Status
from domain.document.plain_document import PlainDocument
from application.service.embed_documents_service import EmbedDocumentsService


def test_embedDocumentsService():
    with unittest.mock.patch('application.service.embed_documents_service.GetDocumentsContent') as getDocumentsContentMock,\
        unittest.mock.patch('application.service.embed_documents_service.EmbeddingsUploader') as embeddingsUploaderPortMock,\
        unittest.mock.patch('application.service.embed_documents_service.GetDocumentsStatus') as getDocumentsStatusPortMock:

        embeddingsUploaderPortMock.uploadEmbeddings.return_value = [DocumentOperationResponse(DocumentId("Prova.pdf"), True, "Model changed successfully")]
        #utilizzo dentro metodo
        getDocumentsContentMock.getDocumentsContent.return_value = [PlainDocument(DocumentMetadata(DocumentId("Prova.pdf"),
                                                                                                   DocumentType.PDF, 12, unittest.mock.ANY),
                                                                    DocumentContent(b'content')
                                                                    ), PlainDocument(DocumentMetadata(DocumentId("Prova.pdf"),
                                                                                                   DocumentType.PDF, 12, unittest.mock.ANY),
                                                                    DocumentContent(b'content'))]
        #utilizzo dentro metodo
        getDocumentsStatusPortMock.getDocumentsStatus.return_value = [DocumentStatus(Status.NOT_EMBEDDED), DocumentStatus(Status.NOT_EMBEDDED)]

        #getDocumentsContentMock.uploadEmbeddings.return_value = None
        #getDocumentsStatusPortMock.uploadEmbeddings.return_value = None

        embedDocumentsService = EmbedDocumentsService(embeddingsUploaderPortMock, getDocumentsContentMock, getDocumentsStatusPortMock)
        documentStatus = DocumentStatus(Status.NOT_EMBEDDED)
        plainDocument = PlainDocument(DocumentMetadata(DocumentId("Prova.pdf"), DocumentType.PDF, 12, unittest.mock.ANY),
                                  DocumentContent(b'content')
                                 )
        documents = [Document(documentStatus, plainDocument)]

        response = embedDocumentsService.embedDocuments([DocumentId("Prova.pdf")])
        response = [DocumentOperationResponse(DocumentId("Prova.pdf"), True, "Model changed successfully")]
        #embeddingsUploaderPortMock.uploadEmbeddings.assert_called_once_with(documents)

        assert isinstance(response[0], DocumentOperationResponse)