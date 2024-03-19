from typing import List
from langchain_core.documents.base import Document as LangchainCoreDocuments
from adapter.out.upload_documents.langchain_embedding_model import LangchainEmbeddingModel

class EmbeddingsCreator:
    def __init__(self, langchainEmbeddingModel: LangchainEmbeddingModel):
        self.langchainEmbeddingModel = langchainEmbeddingModel
        
    def embedDocument(self, documents: List[LangchainCoreDocuments]) -> List[List[float]]:
        return self.langchainEmbeddingModel.embedDocument([document.page_content for document in documents])