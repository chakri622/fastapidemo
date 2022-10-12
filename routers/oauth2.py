
from fastapi import Form, Depends
from typings import Optional

class OAuth2PasswordRequestForm:

    def __init__(
            self,
            grant_type: str = Form(None, regex="password"),
            username: str = Form(...),
            password: str = Form(...),
            scope: str = Form(""),
            client_id: Optional[str] = Form(None),
            client_secret: Optional[str] = Form(None)
                 ):
        self.grant_type = grant_type
        self.username = username
        self.password = password
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret
