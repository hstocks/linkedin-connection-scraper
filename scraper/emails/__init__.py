import json
import requests
import re
import threading
from queue import Queue
from typing import List
from scraper import LinkedInCredentials

class EmailScraper:
    def __init__(self, credentials: LinkedInCredentials) -> None:
        self._credentials = credentials
    
    def _extract_username_from_url(self, url: str) -> str:
        """Assumes format of url is https://www.linkedin.com/in/someusernamehere."""
        match = re.match('https://www.linkedin.com/in/(.*)', url)
        if match is None:
            return None
        username = match.group(1)

        # Remove trailing slash
        username = username.rstrip('/')
        return username

    def get_email_from_username(self, username: str) -> str:
        headers = self._credentials.get_headers()
        endpoint = f'/voyager/api/identity/profiles/{username}/profileContactInfo'
        url = f'https://www.linkedin.com{endpoint}'
        try:
            response = requests.get(url, headers=headers)
        except Exception as e:
            print(f'Error fetching email for {username}: {e}')
            return ''
    
        if response.status_code != 200:
            print(f'Error: received status code {response.status_code} for {url}')
            print(response.text)
            return None
        
        try:
            obj = json.loads(response.text)
        except Exception as e:
            print(f'Error occurred when parsing response for {url}\n{reponse.text}\n\n{e}')
            return None
        
        return obj.get('emailAddress', None)

    def get_email_from_profile_url(self, url: str) -> str:
        username = self._extract_username_from_url(url)
        return self.get_email_from_username(username)
