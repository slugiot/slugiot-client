import requests
import urllib

def call_server():
    """Does a simple server call, and returns whatever the server returns."""
    call_url = server_url + '/tests/test_connection'
    r = requests.get(call_url)
    return r.text

