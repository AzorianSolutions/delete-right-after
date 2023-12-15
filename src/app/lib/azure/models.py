from pydantic import BaseModel
from app.config import AppSettings


class ApiConfig(BaseModel):
    authorize_url: str
    token_url: str
    tenant_id: str
    client_id: str
    client_secret: str

    @staticmethod
    def create_from_settings(settings: AppSettings):
        return ApiConfig(
            authorize_url=settings.azure_oauth_authorize_url,
            token_url=settings.azure_oauth_token_url,
            tenant_id=settings.azure_tenant_id,
            client_id=settings.azure_client_id,
            client_secret=settings.azure_client_secret,
        )
