from typing import List

from domain.document.document_content import DocumentContent
from langchain_core.documents.base import Document as LangchainCoreDocuments

class TextExtractor:
    def extractText(self, documentContent: DocumentContent) -> List[LangchainCoreDocuments]:
        pass