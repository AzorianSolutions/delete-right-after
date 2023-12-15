from azure.identity.aio import ClientSecretCredential
from msgraph import GraphServiceClient
from app.lib.azure.models import ApiConfig


class MicrosoftGraphApiWrapper:
    """A wrapper for the Microsoft Graph API"""

    _client: GraphServiceClient
    """The GraphServiceClient used to make requests to the Microsoft Graph API"""

    _credential: ClientSecretCredential
    """The ClientSecretCredential used to authenticate to the Microsoft Graph API"""

    _scopes: list[str] = ["https://graph.microsoft.com/.default"]
    """The scopes used to authenticate to the Microsoft Graph API"""

    @property
    def client(self) -> GraphServiceClient:
        """Get the GraphServiceClient"""
        return self._client

    @property
    def credential(self) -> ClientSecretCredential:
        """Get the credential"""
        return self._credential

    @property
    def scopes(self) -> list[str]:
        """Get the scopes"""
        return self._scopes

    def __init__(self, config: ApiConfig):
        """Initialize the MicrosoftGraphApiWrapper"""

        self._credential = ClientSecretCredential(
            tenant_id=config.tenant_id,
            client_id=config.client_id,
            client_secret=config.client_secret,
        )

        self._client = GraphServiceClient(credentials=self._credential, scopes=self._scopes)

    def __str__(self):
        return f"<MicrosoftGraphApiWrapper client={self._client} credential={self._credential} scopes={self._scopes}>"

    def __repr__(self):
        return self.__str__()
