import requests
from requests import Request
from urllib.parse import urljoin
import json
from app.constants import SECONDARIES_NODES


def test_function(request: Request):
    request_example = {"test": "in"}
    host = request.client.host

    get_test_url = f"http://{host}/test/{id}/"
    get_inp_url = f"http://{host}/test/{id}/inp"

    test_get_response = requests.get(get_test_url)
    inp_post_response = requests.post(get_inp_url, json=request_example)
    if inp_post_response.status_code == 200:
        print(json.loads(test_get_response.content.decode('utf-8')))


# url = urljoin(SECONDARIES_NODES[0].get("host"), SECONDARIES_NODES[0].get("port"))
#
# print(url)
# print(f'{SECONDARIES_NODES[0].get("host")}:{SECONDARIES_NODES[0].get("port")}')
