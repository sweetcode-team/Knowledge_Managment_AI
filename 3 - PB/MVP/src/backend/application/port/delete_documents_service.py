from application.port._in.delete_documents_use_case import DeleteDocumentsUseCase
from domain.document_id import DocumentId
from typing import List
from domain.document_operation_response import DocumentOperationResponse
from application.port.delete_documents import DeleteDocuments
from application.port.delete_documents_embeddings import DeleteDocumentsEmbeddings


class DeleteDocumentsService(DeleteDocumentsUseCase):
    def __init__(self, deleteDocuments: DeleteDocuments, deleteDocumentsEmbeddings: DeleteDocumentsEmbeddings):
        self.documentsDeleter = deleteDocuments
        self.deleteDocumentsEmbeddings = deleteDocumentsEmbeddings
        
    def deleteDocuments(self, documentsIds: List[DocumentId]) -> List[DocumentOperationResponse]:
        documentOperationResponses = self.deleteDocumentsEmbeddings.deleteDocumentsEmbeddings(documentsIds)
        
        finalOperationResponses = []

        for documentId, documentOperationResponse in zip(documentsIds, documentOperationResponses):
            if documentOperationResponse.ok():
                deleteDocumentOperationResponse = self.documentsDeleter.deleteDocuments([documentId])
                finalOperationResponses=finalOperationResponses+deleteDocumentOperationResponse

        return finalOperationResponses