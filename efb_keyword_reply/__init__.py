import threading
import time
import yaml
import re
from typing import Optional, Union, Dict
from typing import Dict , Any

from ehforwarderbot import Middleware, Message, Status, coordinator, utils, MsgType
from ehforwarderbot.types import ModuleID, MessageID, InstanceID, ChatID
from ehforwarderbot.chat import Chat, SystemChat, GroupChat
from ehforwarderbot.message import MsgType, MessageCommands, MessageCommand, Substitutions
from ehforwarderbot import utils as efb_utils


class KeywordReplyMiddleware(Middleware):

    middleware_id: ModuleID = ModuleID("QQ_War.keyword_reply")
    middleware_name: str = "Keyword Reply Middleware"
    __version__: str = '0.1.0'


    def __init__(self, instance_id: Optional[InstanceID] = None):
        super().__init__(instance_id)
        config_path = efb_utils.get_config_path(self.middleware_id)
        self.config = self.load_config(config_path)
        self.keywords = self.config['keywords'] if 'keywords' in self.config.keys() else {}
        self.keywordsrepeattime = self.config['keywordsrepeattime'] if 'keywordsrepeattime' in self.config.keys() else 1
        self.replylist = dict()
        '''
        { chat_uid1: 
            { keyword1: time1, keyword2: time2,}
          chat_uid2:
            { keyword1: time1, keyword2: time2,}
        }
        '''

    @staticmethod
    def load_config(path : str) -> Dict[str, Any]:
        if not path.exists():
            return
        with path.open() as f:
            d = yaml.full_load(f)
            if not d:
                return
            config: Dict[str, Any] = d
        return config

    @staticmethod
    def sent_by_master(message: Message) -> bool:
        return message.deliver_to != coordinator.master

    def match_list(self, text) -> str:
        """
        关键字的匹配，主要匹配keywords的列表
        """
        for i in self.keywords.keys():
            if re.search(i, str(text)):
                return i
        return "&&"

    def process_message(self, message: Message) -> Optional[Message]:
        keyword = self.match_list(message.text)
    
        if message.type in [MsgType.Unsupported, MsgType.Text] and keyword != "&&" and not self.sent_by_master(message):
            threading.Thread(target=self.keyword_replylist, args=(message,keyword), name=f"keyword_reply thread {message.uid}").start()
            
        return message

    def keyword_replylist(self, message: Message, keyword: str):
        chat_uid = message.chat.uid
        currenttime = time.time()
        if chat_uid in self.replylist.keys():
            if keyword in self.replylist[chat_uid]:
                if currenttime - self.replylist[chat_uid][keyword] > 60*int(self.keywordsrepeattime):
                    self.keyword_reply(message, keyword)
                    self.replylist[chat_uid][keyword] = currenttime
            else:
                self.replylist[chat_uid][keyword] = currenttime
                self.keyword_reply(message, keyword)
        else:
            self.replylist[chat_uid] = { keyword: currenttime }
            self.keyword_reply(message, keyword)


    def keyword_reply(self, message: Message, keyword: str):
        msg = Message(
            uid="{uni_id}".format(uni_id=str(int(time.time()))),
            type=MsgType.Text,
            chat=message.chat,
            text=self.keywords[keyword],
            #author=message.author,
            deliver_to=coordinator.slaves[message.chat.module_id]
        )
        #msg.author = msg.chat.self
        msg.author = msg.chat.make_system_member(name = "keywordreply", uid = ChatID(self.middleware_id))
        msg_to_master = Message(
            uid="{uni_id}".format(uni_id=str(int(time.time()))),
            type=MsgType.Text,
            chat=message.chat,
            text=self.keywords[keyword],
            #author=message.author,
            deliver_to=coordinator.master
        )
        msg_to_master.author =  msg_to_master.chat.make_system_member(name = "keywordreply", uid = ChatID(self.middleware_id))
        coordinator.send_message(msg_to_master)
        coordinator.send_message(msg)
        #coordinator.send_message(msg_to_master)
    
