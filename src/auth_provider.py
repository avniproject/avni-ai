from fastmcp.server.auth import AccessToken, TokenVerifier


class SimpleTokenVerifier(TokenVerifier):
    def __init__(self, valid_token_prefix: str = ""):
        super().__init__()
        self.valid_token_prefix = valid_token_prefix

    async def verify_token(self, token: str) -> AccessToken | None:
        # Simple validation - check if token starts with expected prefix
        if token and (
            not self.valid_token_prefix or token.startswith(self.valid_token_prefix)
        ):
            return AccessToken(
                token=token,
                client_id="avni_client",
                scopes=[],
                claims={"auth_token": token, "sub": "avni_user"},
            )
        return None
