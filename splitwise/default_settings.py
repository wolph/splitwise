import datetime

# Your app key and secret
API_KEY = ''
API_SECRET = ''

# Openexchangerates.org url including app_id, something like this:
# 'https://openexchangerates.org/api/latest.json?app_id=APP_ID'
OPEN_EXCHANGE_RATES_URL = ''

SERVER_PORT = 8080
SERVER_HOST = None
DEBUG = False

# Stay logged in for a year by default
PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=365)

