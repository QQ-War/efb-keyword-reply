import pathlib
import shelve
import atexit
import uuid
import time
import threading
#import re
from collections.abc import Mapping
from threading import Timer
from typing import Optional, Union, Dict
from typing_extensions import overload, Literal

from ruamel.yaml import YAML

from ehforwarderbot import Middleware, Message, Status, coordinator, utils, MsgType
from ehforwarderbot.chat import Chat, SystemChat, GroupChat
from ehforwarderbot.types import ModuleID, MessageID, InstanceID, ChatID
from ehforwarderbot.message import MsgType, MessageCommands, MessageCommand, Substitutions
from ehforwarderbot.status import MessageRemoval, ReactToMessage, MessageReactionsUpdate


class KeywordReplyMiddleware(Middleware):
    """
    """
    middleware_id: ModuleID = ModuleID("QQ_War.keyword_reply")
    middleware_name: str = "Keyword Reply Middleware"
    __version__: str = '0.1.0'

    keywords = ['语音/视频聊天\n  - - - - - - - - - - - - - - - \n不支持的消息类型, 请在微信端查看']
    
    #待处理，通过正则匹配
    #rekeywords = [ '*(unsupported)\n语音/视频聊天*']

    def __init__(self, instance_id: Optional[InstanceID] = None):
        super().__init__(instance_id)
        
    def match_list(self, text) -> bool:
        """
        关键字的匹配，主要匹配keywords的列表
        """
        for i in self.keywords:
            #print(text.find(i))
            if text.find(i) != -1:
                return True
        return False

    def process_message(self, message: Message) -> Optional[Message]:
        #print("message.type&&&&&"+str(message.type))
        #print(message.type)
        #print(self.match_list(message.text))
    
        if message.type == MsgType.Unsupported and \
            self.match_list(message.text):    
            #self.keyword_reply(message)
            threading.Thread(target=self.keyword_reply, args=(message,), name=f"keyword_reply thread {message.uid}").start()
            
        return message

    def keyword_reply(self, message: Message):
        msg = Message(
            uid="{uni_id}".format(uni_id=str(int(time.time()))),
            type=MsgType.Text,
            chat=message.chat,
            text='终端不支持语音通话，请发送信息或拨打****(本条是自动回复）',
            author=message.author,
            #deliver_to=coordinator.slaves,
            deliver_to=coordinator.slaves[message.chat.module_id]
        )
        #msg.chat.uid=message.chat.uid
        #coordinator.slaves['honus.CuteCatiHttp'].send_message(msg)
        coordinator.send_message(msg)
    
