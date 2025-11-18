class SessionManager:
    def __init__(self):
        self._current_user = None
        self._authenticated = False

    @property
    def current_user(self):
        return self._current_user

    @property
    def authenticated(self):
        return self._authenticated

    @property
    def user_id(self):
        if self._current_user:
            return self._current_user.id
        return None

    def login(self, user):
        self._current_user = user
        self._authenticated = True

    def logout(self):
        self._current_user = None
        self._authenticated = False

    def clear(self):
        self.logout()
