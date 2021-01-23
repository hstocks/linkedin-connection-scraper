# LinkedIn Connection Scraper

A script to retrieve the names, titles and email addresses of all of your LinkedIn connections. 

This makes use of the LinkedIn APIs directly, so no Selenium is required. Retrieved data is written to a CSV file.

## Usage
```
$ ./get_connections.py -h
usage: get_connections.py [-h] [-e] [-n N] access_token csrf_token

positional arguments:
  access_token       From li_at cookie
  csrf_token         From JSESSIONID cookie

optional arguments:
  -h, --help         show this help message and exit
  -e, --with-emails  Only save connections with visible email addresses
  -n N               Maximum number of connections to retrieve
```
For the access token and CSRF token values, sign in to LinkedIn and get the value of the `li_at` and `JSESSIONID` cookies.

## Sample Output
```
"John","Archer","Managing Director at Delight Clothing","john.archer@notreal.com","https://www.linkedin.com/in/johnarcher-fake/"
"Rebecca","Wood","Entrepreneur | Inventor","rw2201@notreal.com","https://www.linkedin.com/in/rebeccaaaa-fake/"
```
**Disclaimer:** this may break as the APIs change over time. Works as of publishing.
