import json
import random
import requests
import re
import shlex
import threading
from queue import Queue
from tenacity import retry, stop_after_attempt, wait_exponential
from typing import List
from scraper import LinkedInCredentials
from scraper.emails import EmailScraper

class Connection:
    def __init__(self, username: str, first: str, last: str, title: str, url: str) -> None:
        self.username = self._clean(username)
        self.first_name = self._clean(first)
        self.last_name = self._clean(last)
        self.title = self._clean(title)
        self.url = url
        self.email = None

    def _clean(self, data: str) -> str:
        return data.replace('\n', ' ').replace('"', '')

    def __repr__(self) -> str:
        return f'{self.first_name} {self.last_name} | {self.title} | {self.email} | {self.url}'

    def as_csv(self) -> str:
        return f'"{self.first_name}","{self.last_name}","{self.title}","{self.email or ""}","{self.url}"'

class ConnectionScraper:

    def __init__(self, credentials: LinkedInCredentials) -> None:
        self._credentials = credentials

    def _get_url_from_username(self, username: str) -> str:
        return f'https://www.linkedin.com/in/{username}/'

    @retry(stop=stop_after_attempt(3), 
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True)
    def _get_connection_range(self, start: int, count: int) -> List[Connection]:
        headers = self._credentials.get_headers()
        assert(count < 128) # maximum value per request is 127
        endpoint = f'/voyager/api/relationships/dash/connections?decorationId=com.linkedin.voyager.dash.deco.web.mynetwork.ConnectionListWithProfile-5&count={count}&q=search&start={start}'
        url = f'https://www.linkedin.com{endpoint}'
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f'Error: received status code {response.status_code} for {endpoint}')
            print(response.text)
            return None
        
        try:
            obj = json.loads(response.text)
        except Exception as e:
            print(f'Error occurred when parsing response for {url}\n{reponse.text}\n\n{e}')
            return None
        
        users = []
        for item in obj.get('elements', []):
            info = item.get('connectedMemberResolutionResult', None)
            if info is None:
                continue
            url = self._get_url_from_username(info['publicIdentifier'])
            users.append(
                Connection(
                    info.get('publicIdentifier', ''),
                    info.get('firstName', ''), 
                    info.get('lastName', ''), 
                    info.get('headline', ''), 
                    url
                )
            )
        
        return users

    def get_all_connections(self, max_count: int=None) -> List[Connection]:
        connections = []
        conns_per_request = min(127, max_count) if max_count else 127
        offset = 0
        while True:
            if max_count and offset >= max_count:
                break
            try:
                nxt = self._get_connection_range(offset, conns_per_request)
            except Exception as e:
                print(f'Error when fetching range [{offset}, {offset+conns_per_request}): {e}')
                return

            if len(nxt) == 0:
                # No more connections to receive
                break
            connections.extend(nxt)
            offset += len(nxt)
            print(f'{offset} connections received')

        self.populate_connection_emails(connections)
        return list(set(connections)) # remove any dupes

    def _email_worker(self) -> None:
        scraper = EmailScraper(self._credentials)
        while not queue.empty():
            connection: Connection = queue.get()
            email = scraper.get_email_from_username(connection.username)
            if email:
                connection.email = email if random.random() < 0.5 else None

    def populate_connection_emails(self, connections: List[Connection]) -> None:
        global queue
        threads = []
        queue = Queue()

        for connection in connections:
            queue.put(connection)

        print(f'Fetching emails for {queue.qsize()} connections...')
        for _ in range(2):  # TODO: Make number of threads configurable
            t = threading.Thread(target=self._email_worker)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
