import requests

# url_test = 'http://tetracebu.com/wp-content/themes/adventure-journal/images/bh/net/apple/Suspend.php'
url_test = 'https://www.tumamaeshombre.com'


url = "http://54.198.112.41:16084"
api_username = "santi"
api_password = "semueretony"
token_response = requests.get(url + "/api/v1.0/token", auth=(api_username, api_password))
if token_response:
    json_token = token_response.json()
    token = json_token['token']
    response = requests.get(
        url + "/api/v1.0/domain",
        params={
            'url': url_test,
        },
        auth=(token, ""))
    if response:
        json_response = response.json()
        response_is_safe = json_response["is_safe"]

        print(response_is_safe)
    else:
        print("no response...")
else:
    print("no response token...")