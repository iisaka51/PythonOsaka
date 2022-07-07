import os
from dataprep.connector import connect, info

auth_token = os.environ.get('FINNHUB_APIKEY', default=None)
dc = connect('finnhub', _auth={"access_token":auth_token})

dc
