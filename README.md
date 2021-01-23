A script to retrieve the names, titles and email addresses of all LinkedIn connections. Saves the data to a CSV file.
This uses the LinkedIn APIs directly, so no Selenium required.

# Usage
```
./get_connections.py <access token> <csrf token>
```

To get these values, sign in to LinkedIn and grab the `li_at` cookie for the access token, and `JSESSIONID` for the CSRF token.


Disclaimer: this may break as the APIs change over time. Working as of Jan 2020.