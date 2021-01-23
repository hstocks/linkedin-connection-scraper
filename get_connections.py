#!/usr/bin/env python3

import argparse
import sys

from datetime import datetime
from scraper import LinkedInCredentials
from scraper.connections import ConnectionScraper

def run(access_token: str, csrf_token: str, 
        max_conns: int=None, only_with_emails: bool=False) -> None:
    creds = LinkedInCredentials(access_token, csrf_token)
    scraper = ConnectionScraper(creds)

    # Start scraping
    conns = scraper.get_all_connections(max_conns)

    if only_with_emails:
        num_emails = len(list(filter(lambda c: c.email, conns)))
        print(f'{num_emails} emails retrieved from {len(conns)} connections. ' +
                f'{int(num_emails / len(conns) * 100)}% hit rate')
    
    out_file = f'connections_{datetime.now().strftime("%Y_%m_%d-%H_%M")}.txt'
    with open(out_file, 'w') as f:
        for conn in conns:
            if only_with_emails and not conn.email:
                continue
            f.write(conn.as_csv() + '\n')
    print(f'Data written to {out_file}')
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('access_token', help='From li_at cookie')
    parser.add_argument('csrf_token', help='From JSESSIONID cookie')
    parser.add_argument('-e', '--with-emails', action='store_true', 
        help='Only save connections with visible email addresses')
    parser.add_argument('-n', type=int, 
        help='Maximum number of connections to retrieve')
    args = parser.parse_args()
    run(args.access_token, args.csrf_token, args.n, args.with_emails)
