import os
from typing import List

import boto3
from adapter.out.persistence.aws.AWS_document import AWSDocument
from adapter.out.persistence.aws.AWS_document_operation_response import AWSDocumentOperationResponse
from adapter.out.persistence.aws.AWS_document_metadata import AWSDocumentMetadata
from domain.document.document_id import DocumentId
from domain.document.document_metadata import DocumentMetadata, DocumentType

"""
    This class is responsible for managing the AWS S3 bucket.
    Attributes:
        s3 (boto3.client): The boto3 client for S3 operations.
        bucket_name (str): The name of the S3 bucket.
    Methods:
        getDocumentById(documentId: str) -> AWSDocument:
            Get the document from the S3 bucket by its ID.
        uploadDocuments(awsDocuments: List[AWSDocument], forceUpload: bool) -> List[AWSDocumentOperationResponse]:
            Upload the documents to the S3 bucket.
        deleteDocuments(ListOfDocumentId: List[str]) -> List[AWSDocumentOperationResponse]:
            Delete the documents from the S3 bucket.
        getDocumentsMetadata(documentFilter: str) -> List[AWSDocumentMetadata]:
            Get the metadata of the documents from the S3 bucket.
"""
class AWSS3Manager:
    def __init__(self):
        with open('/run/secrets/aws_access_key_id', 'r') as file:
            aws_access_key_id = file.read()
        with open('/run/secrets/aws_secret_access_key', 'r') as file:
            aws_secret_access_key = file.read()
        with open('/run/secrets/aws_bucket_name', 'r') as file:
            awsBucketName = file.read()
        self.awsBucketName = awsBucketName
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name="eu-west-1"
        )

    def getDocumentById(self, documentId):
        try:
            aws = self.s3.get_object(Bucket=self.awsBucketName, Key=documentId)
            id = aws.get('Key')
            content = aws.get('Body').read()
            type = aws.get('ContentType')
            size = aws.get('ContentLength')
            uploadTime = aws.get('LastModified')
        except:
            return None
        return AWSDocument(
            id,
            content,
            type,
            size,
            uploadTime
        )

    def uploadDocuments(self, awsDocuments: List[AWSDocument], forceUpload:bool) -> List[AWSDocumentOperationResponse]:
        AWSDocumentOperationResponseList = []
        for document in awsDocuments:
            if not forceUpload:
                try:
                    self.s3.head_object(Bucket=self.awsBucketName, Key=document.id)
                    AWSDocumentOperationResponseList.append(AWSDocumentOperationResponse(document.id, False, "Il documento è già presente nel sistema."))
                except:
                    try:
                        operationResponse = self.s3.put_object(Bucket=self.awsBucketName, Key=document.id, Body=document.content, ContentType=document.type)
                        if 200 <= operationResponse.get('ResponseMetadata', {}).get('HTTPStatusCode', 0) <= 299:
                            AWSDocumentOperationResponseList.append(AWSDocumentOperationResponse(document.id, True, "Caricamento del documento avvenuto con successo."))
                        else:
                            AWSDocumentOperationResponseList.append(AWSDocumentOperationResponse(document.id, False, "Errore durante il caricamento del documento."))
                    except:
                        AWSDocumentOperationResponseList.append(AWSDocumentOperationResponse(document.id, False, "Errore durante il caricamento del documento."))

        return AWSDocumentOperationResponseList

    def deleteDocuments(self, documentsIds: List[str]) -> List[AWSDocumentOperationResponse]:
        AWSDocumentOperationResponseList = []
        for documentId in documentsIds:
            try:
                self.s3.head_object(Bucket=self.awsBucketName, Key=documentId)
                operationResponse = self.s3.delete_object(Bucket=self.awsBucketName, Key=documentId)
                if 200 <= operationResponse.get('ResponseMetadata', {}).get('HTTPStatusCode', 0) <= 299:
                    AWSDocumentOperationResponseList.append(AWSDocumentOperationResponse(documentId, True, "Eliminazione del documento avvenuta con successo."))
                else:
                    AWSDocumentOperationResponseList.append(AWSDocumentOperationResponse(documentId, False, "Errore durante l'eliminazione del documento."))
            except self.s3.exceptions.NoSuchKey:
                AWSDocumentOperationResponseList.append(AWSDocumentOperationResponse(documentId, False, "Il documento non è presente nel sistema."))
            except:
                AWSDocumentOperationResponseList.append(AWSDocumentOperationResponse(documentId, False, "Errore durante l'eliminazione del documento."))
        return AWSDocumentOperationResponseList

    def getDocumentsMetadata(self, documentFilter: str) -> List[AWSDocumentMetadata]:
        result = []
        awsDocumentMetadata = self.s3.list_objects_v2(Bucket=self.awsBucketName,
                                                      Prefix=documentFilter)
        contents = awsDocumentMetadata.get('Contents')
        for content in contents:
            awsMetadata = AWSDocumentMetadata(content.get('Key'),
                                            content.get('Size'),
                                            content.get('LastModified'))
            result.append(awsMetadata)
        return result

    def getDocumentContent(self, documentId: str) -> AWSDocument:
        documentContentResponse = self.s3.get_object(Bucket=self.awsBucketName, Key=documentId)
        return AWSDocument(documentId,
                            documentContentResponse.get('Body').read(),
                            documentContentResponse.get('ContentType'),
                            documentContentResponse.get('ContentLength'),
                            documentContentResponse.get('LastModified'))
