from loguru import logger
from app.config import AppSettings


class AzureManager:
    """Manager for Azure-related tasks."""

    _graph_api_endpoint = 'https://graph.microsoft.com/v1.0'
    """The endpoint for the Graph API."""

    _scope = ['email', 'profile', 'https://graph.microsoft.com/Mail.ReadWrite', 'openid']
    """The OAuth scope for the Graph API."""

    _settings: AppSettings
    """The application settings instance."""

    _token: dict | None = None
    """The token data for the Graph API."""

    def __init__(self, settings: AppSettings):
        self._settings = settings
        self._load_token()

    def auth(self):
        """Run the account authorization process."""
        import json
        import webbrowser
        from requests_oauthlib import OAuth2Session

        if self._token is not None:
            confirm_response = input('An existing token was found. Do you want to overwrite it? [y/n]: ')
            if confirm_response.lower() != 'y':
                print()
                print('Authorization aborted.')
                return

        oauth = OAuth2Session(self._settings.azure_client_id, redirect_uri=None, scope=self._scope)

        authorization_url, _ = oauth.authorization_url(self._settings.azure_oauth_authorize_url)

        auth_request_response = input('Launch web browser to perform authorization? [y/n]: ')

        if auth_request_response.lower() == 'y':
            webbrowser.open(authorization_url)
        else:
            print()
            print(f'Please open the following URL in your browser: {authorization_url}')

        print()
        redirect_response = input('Please provide the full redirect URL here: ')

        token = oauth.fetch_token(self._settings.azure_oauth_token_url, authorization_response=redirect_response,
                                  client_id=self._settings.azure_client_id, include_client_id=True)

        with open(self._settings.azure_token_path, 'w') as f:
            f.write(json.dumps(token))
            f.close()

        print()
        print('Authorization completed successfully.')

    def scrub_mail(self, delete: bool = False):
        """Run the mail scrubbing process."""

        if self._token is None:
            logger.error('No token found. Please run the authorization process first.')
            return

        messages = self._load_messages()

        for message in messages:
            message_id: str = message['id']
            subject: str = message["subject"]

            if 'internetMessageId' not in message or '.knowbe4.com' not in message['internetMessageId']:
                if self._settings.debug:
                    logger.debug(f'Skipping message: {subject}')
                continue

            logger.info(f'KnowBe4 Message Found: {subject}')

            if self._settings.debug:
                logger.debug(f'Message ID: {message_id}')

            # Either delete the message or mark it as read and archive it based on the delete flag.
            if delete:
                if not self._delete_message(message_id):
                    logger.error(f'Could not delete message: {subject}')
                    continue
                logger.info(f'Message deleted: {subject}')
            else:
                if not self._archive_message(message_id):
                    logger.error(f'Could not archive message: {subject}')
                    continue

                if not self._move_message(message_id, 'Archive'):
                    logger.error(f'Could not move message: {subject}')
                    continue

                logger.info(f'Message archived: {subject}')

    def _load_token(self):
        """Load the token from the token file."""
        import json
        import os

        if (not os.path.exists(self._settings.azure_token_path)
                or not os.path.isfile(self._settings.azure_token_path)
                or os.path.getsize(self._settings.azure_token_path) == 0
                or not os.access(self._settings.azure_token_path, os.R_OK)):
            return

        with open(self._settings.azure_token_path, 'r') as f:
            self._token = json.loads(f.read())
            f.close()

    def _build_headers(self, is_json: bool = False) -> dict:
        """Build the headers for the API request."""
        headers: dict = {'Authorization': 'Bearer ' + self._token['access_token']}

        if is_json:
            headers['Content-Type'] = 'application/json'

        return headers

    def _load_messages(self) -> list[dict]:
        """Load the messages from the inbox."""
        import requests

        if self._token is None:
            logger.error('No token found. Please run the authorization process first.')
            return []

        headers = self._build_headers()

        inbox_url = f'{self._graph_api_endpoint}/me/mailFolders/inbox/messages'

        response = requests.get(inbox_url, headers=headers)

        if response.status_code != 200:
            logger.error(f'Could not get inbox messages: {response.text}')
            return []

        return response.json()['value']

    def _archive_message(self, message_id: str) -> bool:
        """Archive a message from the inbox."""
        import requests

        if self._token is None:
            logger.error('No token found. Please run the authorization process first.')
            return False

        if self._settings.dry_run:
            return True

        headers = self._build_headers(is_json=True)

        patch_url = f'{self._graph_api_endpoint}/me/mailFolders/inbox/messages/{message_id}'
        patch_data = {
            'isRead': True,
            'categories': ['Archived'],
        }

        response = requests.patch(patch_url, headers=headers, json=patch_data)

        if response.status_code != 200:
            logger.error(f'Could not archive message: {response.text}')
            return False

        logger.debug(f'Message archived: {message_id}')

        return True

    def _move_message(self, message_id: str, destination_folder_id: str) -> bool:
        """Move a message to a different folder."""
        import requests

        if self._token is None:
            logger.error('No token found. Please run the authorization process first.')
            return False

        if self._settings.dry_run:
            return True

        headers = self._build_headers(is_json=True)

        patch_url = f'{self._graph_api_endpoint}/me/mailFolders/inbox/messages/{message_id}/move'
        patch_data = {
            'destinationId': destination_folder_id,
        }

        response = requests.post(patch_url, headers=headers, json=patch_data)

        if response.status_code != 201:
            logger.error(f'Could not move message: {response.text}')
            return False

        logger.debug(f'Message moved: {message_id}')

        return True

    def _delete_message(self, message_id: str) -> bool:
        """Delete a message from the inbox."""
        import requests

        if self._token is None:
            logger.error('No token found. Please run the authorization process first.')
            return False

        if self._settings.dry_run:
            return True

        headers = self._build_headers()

        delete_url = f'{self._graph_api_endpoint}/me/mailFolders/inbox/messages/{message_id}'
        response = requests.delete(delete_url, headers=headers)

        if response.status_code != 204:
            logger.error(f'Could not delete message: {response.text}')
            return False

        logger.debug(f'Message deleted: {message_id}')

        return True
