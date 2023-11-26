class MsgStore:
    def __init__(self):
        self.msgs = {}

    def add(self, chat_id: int, user_msg_id: int, bot_msg_id: int):
        if chat_id not in self.msgs:
            self.msgs[chat_id] = {}
        self.msgs[chat_id][user_msg_id] = bot_msg_id

    def get(self, chat_id: int, user_msg_id: int):
        if chat_id in self.msgs:
            if user_msg_id in self.msgs[chat_id]:
                return self.msgs[chat_id][user_msg_id]
        return None

    def delete(self, chat_id: int, user_msg_id: int):
        if chat_id in self.msgs:
            if user_msg_id in self.msgs[chat_id]:
                del self.msgs[chat_id][user_msg_id]
                if not self.msgs[chat_id]:
                    del self.msgs[chat_id]
