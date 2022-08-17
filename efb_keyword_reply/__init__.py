import threading
import time
import yaml
from typing import Optional, Union, Dict
from typing import Dict , Any

from ehforwarderbot import Middleware, Message, Status, coordinator, utils, MsgType
from ehforwarderbot.types import ModuleID, MessageID, InstanceID, ChatID
from ehforwarderbot.chat import Chat, SystemChat, GroupChat
from ehforwarderbot.message import MsgType, MessageCommands, MessageCommand, Substitutions
from ehforwarderbot import utils as efb_utils


class KeywordReplyMiddleware(Middleware):
    """
    """
    middleware_id: ModuleID = ModuleID("QQ_War.keyword_reply")
    middleware_name: str = "Keyword Reply Middleware"
    __version__: str = '0.1.0'

    #keywords = {'语音/视频聊天\n  - - - - - - - - - - - - - - - \n不支持的消息类型, 请在微信端查看':'终端不支持语音通话，请发送信息或拨打*****(本条是自动回复）', '在吗？':'信息已收到，请留言（本条是自动回复）', '在？':'信息已收到，请留言（本条是自动回复）',  '在吗':'信息已收到，请留言（本条是自动回复）'}
    
    #待处理，通过正则匹配
    #rekeywords = [ '*(unsupported)\n语音/视频聊天*']

    def __init__(self, instance_id: Optional[InstanceID] = None):
        super().__init__(instance_id)
        config_path = efb_utils.get_config_path(self.middleware_id)
        self.config = self.load_config(config_path)
        self.keywords=self.config['keywords'] if 'keywords' in self.config.keys() else {}
        #self.keywords['语音/视频聊天\n  - - - - - - - - - - - - - - - \n不支持的消息类型, 请在微信端查看']='终端不支持语音通话，请发送信息或拨打*****(本条是自动回复）'

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
            if text.find(i) != -1:
                return i
        return "&&"

    def process_message(self, message: Message) -> Optional[Message]:
        keyword = self.match_list(message.text)
    
        if message.type in [MsgType.Unsupported, MsgType.Text] and keyword != "&&" and not self.sent_by_master(message):
            threading.Thread(target=self.keyword_reply, args=(message,keyword), name=f"keyword_reply thread {message.uid}").start()
            
        return message

    def keyword_reply(self, message: Message, keyword: str):
        msg = Message(
            uid="{uni_id}".format(uni_id=str(int(time.time()))),
            type=MsgType.Text,
            chat=message.chat,
            text=self.keywords[keyword],
            author=message.author,
            deliver_to=coordinator.slaves[message.chat.module_id]
        )
        msg_to_master = Message(
            uid="{uni_id}".format(uni_id=str(int(time.time()))),
            type=MsgType.Text,
            chat=message.chat,
            text=self.keywords[keyword],
            author=message.author,
            deliver_to=coordinator.master
        )
        coordinator.send_message(msg)
        coordinator.send_message(msg_to_master)
    
