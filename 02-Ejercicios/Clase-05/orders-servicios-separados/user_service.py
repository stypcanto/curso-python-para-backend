from data import USERS


class UserService:
    def get_user(self, user_id: int):
        return USERS[user_id]
