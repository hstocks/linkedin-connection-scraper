import random
from typing import Dict

"""
Required things to make an API request:
- CSRF token header, called "csrf-token"
- Two cookies
  - JSESSIONID - this is the same value as in the csrf-token header
  - li_at - presumably LinkedIn Access Token
"""

class LinkedInCredentials:
    def __init__(self, access_token: str, csrf_token: str) -> None:
        self.access_token = access_token
        if not csrf_token.startswith('ajax:'):
            raise RuntimeError('CSRF token should start with ajax:')
        self.csrf_token = csrf_token

    def get_headers(self) -> Dict[str, str]:
        return {
            'csrf-token': f'{self.csrf_token}',
            'Cookie': f'JSESSIONID="{self.csrf_token}"; li_at={self.access_token};',
            'User-Agent': self._get_user_agent(),
        }

    def _get_user_agent(self) -> str:
        return random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
            ])
