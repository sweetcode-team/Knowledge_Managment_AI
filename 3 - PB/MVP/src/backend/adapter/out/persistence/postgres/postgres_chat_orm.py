from datetime import datetime
from typing import List
from adapter.out.persistence.postgres.chat_models import Chat, MessageStore, MessageRelevantDocuments

from adapter.out.persistence.postgres.database import db_session

from adapter.out.persistence.postgres.postgres_chat_operation_response import PostgresChatOperationResponse
from adapter.out.persistence.postgres.postgres_message import PostgresMessage, PostgresMessageSenderType
from adapter.out.persistence.postgres.postgres_chat_preview import PostgresChatPreview
from adapter.out.persistence.postgres.postgres_chat import PostgresChat

from datetime import datetime

class PostgresChatORM:
    def __init__(self) -> None:
        pass
    
    def persistChat(self, messages: List[PostgresMessage], chatId: int = None) -> PostgresChatOperationResponse:
        if len(messages) == 0:
            return PostgresChatOperationResponse(False, "Nessun messaggio da salvare.", None)
        
        if chatId is None:
            newChatResponse = self.createChat()
            if not newChatResponse.status:
                return newChatResponse
            return self.saveMessages(messages, newChatResponse.chatId)
        else:
            return self.saveMessages(messages, chatId)
    
    def createChat(self) -> PostgresChatOperationResponse:
        try:
            newChat = Chat(f"Nuova chat {datetime.now().isoformat()}")
            db_session.add(newChat)
            db_session.commit()
            newChatId = newChat.id
            return PostgresChatOperationResponse(True, "Chat creata correttamente.", newChatId)
        except Exception as e:
            return PostgresChatOperationResponse(False, f"Errore nella creazione della chat: {str(e)}", None)
    
    def saveMessages(self, messages: List[PostgresMessage], chatId: int) -> PostgresChatOperationResponse:
        try:
            newMessages = [MessageStore(chatId, {"data": {"type": message.sender.name, "content": message.content, "timestamp": message.timestamp.isoformat()}}) for message in messages]
            db_session.add_all(newMessages)
            db_session.commit()
            newMessageIds = [newMessage.id for newMessage in newMessages]
            
            messageRelevantDocuments = []
            for i, message in enumerate(messages):
                if message.relevantDocuments is not None:
                    for document in message.relevantDocuments:
                        messageRelevantDocuments.append(MessageRelevantDocuments(id=newMessageIds[i], documentId=document))
            db_session.add_all(messageRelevantDocuments)
            return PostgresChatOperationResponse(True, "Messaggi salvati correttamente.", chatId)
        except Exception as e:
            return PostgresChatOperationResponse(False, f"Errore nel salvataggio dei messaggi: {str(e)}", None)
    
    def deleteChats(self, chatIds: List[int]) -> List[PostgresChatOperationResponse]:
        try:
            db_session.query(Chat).filter(Chat.id.in_(chatIds)).delete(synchronize_session=False)
            db_session.commit()
            #TODO: eliminare anche i messaggi e i documenti associati
            #TODO: vedere se è stata eliminata effettivamente la chat
            return [PostgresChatOperationResponse(True, "Chat eliminata correttamente.", chatId) for chatId in chatIds]
        except Exception as e:
            return [PostgresChatOperationResponse(False, f"Errore nella eliminazione della chat: {str(e)}", chatId) for chatId in chatIds]
    
    def renameChat(self, chatId: int, newName: str) -> PostgresChatOperationResponse:
        try:
            db_session.query(Chat).filter(Chat.id == chatId).update({"title": newName})
            db_session.commit()
            return PostgresChatOperationResponse(True, "Chat rinominata correttamente.", chatId)
        except Exception as e:
            return PostgresChatOperationResponse(False, f"Errore nella rinomina della chat: {str(e)}", chatId)
    
    def getChats(self, chatFilter:str) -> List[PostgresChatPreview]:
        try:
            chats = db_session.query(Chat).filter(Chat.title.like(f"%{chatFilter}%")).all()
            chatPreviews = []
            for chat in chats:
                lastMessage = db_session.query(MessageStore).filter(MessageStore.sessionId == chat.id).order_by(MessageStore.id.desc()).first()
                if lastMessage is not None:
                    chatPreviews.append(PostgresChatPreview(chat.id, chat.title, PostgresMessage(
                        lastMessage.message["data"]["content"],
                        datetime.fromisoformat(lastMessage.message["data"]["timestamp"]),
                        [document.documentId for document in db_session.query(MessageRelevantDocuments).filter(MessageRelevantDocuments.id == lastMessage.id).all()],
                        PostgresMessageSenderType[lastMessage.message["data"]["type"]]))
                    )
                else:
                    chatPreviews.append(PostgresChatPreview(chat.id, chat.title, None))
            return chatPreviews
        except Exception as e:
            return []
    
    def getChatMessages(self, chatId: int) -> PostgresChat:
        try:
            chat = db_session.query(Chat).filter(Chat.id == chatId).first()
            messages = db_session.query(MessageStore).filter(MessageStore.sessionId == chatId).all()
            postgresMessages = [PostgresMessage(
                message.message["data"]["content"],
                datetime.fromisoformat(message.message["data"]["timestamp"]),
                [document.documentId for document in db_session.query(MessageRelevantDocuments).filter(MessageRelevantDocuments.id == message.id).all()],
                PostgresMessageSenderType[message.message["data"]["type"]]) for message in messages]
            
            return PostgresChat(chat.id, chat.title, postgresMessages)
        except Exception as e:
            return None
