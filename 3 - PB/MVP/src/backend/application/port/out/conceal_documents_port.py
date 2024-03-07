from typing import List

from domain.document.document_id import DocumentId
from domain.document.document_operation_response import DocumentOperationResponse


class ConcealDocumentsPort:
    def concealDocuments(self, documentsIds: List[DocumentId]) -> List[DocumentOperationResponse]:
        pass