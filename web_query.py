import requests
import time

xy_headers = {'Content-Type': 'application/json'}

def get_request(token, url, post_json=None):
    xy_headers['X-Auth-token'] = token
    if post_json == None:
        r = requests.get(url, headers=xy_headers)
    else:
        r = requests.get(url, post_json, headers=xy_headers)
    return r

def get_request_not_token(url, post_json=None):
    if post_json == None:
        r = requests.get(url)
    else:
        r = requests.get(url, post_json)
    return r

def post_request(token, url, post_json=None):
    xy_headers['X-Auth-token'] = token
    if post_json == None:
        r = requests.post(url, headers=xy_headers)
    else:
        r = requests.post(url, json=post_json, headers=xy_headers)
    return r

def web_request_retry(token, type, url, post_json=None):
    """timeout발생 시 sleep_seconds쉬고 num_retyrp번 재시도 한다"""
    for n in range(20):
        try:
            if type == 'get':
                return get_request(token, url, post_json)
            else:
                return post_request(token, url, post_json)
        except Exception as err:
            last_err = err
            print(str(n+1) + ' Timeout')
            time.sleep(1)
            continue
    return None

def get_token(url, post_json):
    r = requests.post(url, json=post_json, headers=xy_headers)
    return r