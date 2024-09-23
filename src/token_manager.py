# token_manager.py

import json
import os

class TokenManager:
    def __init__(self, token_file='tokens.json'):
        self.token_file = token_file
        self.tokens = self.load_tokens()

    def load_tokens(self):
        if not os.path.exists(self.token_file):
            raise FileNotFoundError(f"Token file {self.token_file} not found.")
        with open(self.token_file, 'r') as f:
            tokens = json.load(f)
        return tokens

    def validate_token(self, provided_token):
        # Reload tokens to get the latest data
        self.tokens = self.load_tokens()
        return provided_token in self.tokens.values()

    def get_user_by_token(self, provided_token):
        for user, token in self.tokens.items():
            if token == provided_token:
                return user
        return None
