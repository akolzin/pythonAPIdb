import json
import requests
import pytest

from api.client import RestfulBookerClient
from api import random
from random import randint
from conftest import client

url = "http://5.227.126.79:9200/mediadev-elvis-metadata-avm/_search?size=19"
# url1 = "http://5.227.126.79:9200/mediadev-elvis-metadata-avm/_search?data=%7B%22query%22%3A%7B%22match%22%3A%7B%22cf_containerType%22%3A%7B%22query%22%3A%22лента%22%7D%7D%7D%7D"
url1 = "http://5.227.126.79:9200/mediadev-elvis-metadata-avm/_search?data=%7B%0A%20%20%22query%22%3A%20%7B%0A%20%20%20%20%22match%22%3A%20%7B%0A%20%20%20%20%20%20%22cf_containerType%22%3A%20%7B%0A%20%20%20%20%20%20%20%20%22query%22%3A%20%22%D1%80%D0%B5%D0%BF%D0%BE%D1%80%D1%82%D0%B0%D0%B6%22%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A"
url2 = "http://elvis2.dev.itass.local/api/asset/search?q=/Data/Sections"
url3 = "http://elvis2.dev.itass.local/services/apilogin?username=cvtTest2&password=cvtTest2"
# ?assetIds=BTF4Qnx54k0By0n_e_orYJ

Token = ""

#@pytest.fixture(scope="function")
def test():
    payload = "{\r\n  \"query\": {\r\n    \"match\": {\r\n      \"cf_containerType\": {\r\n        \"query\": " \
              "\"лента\"\r\n      }\r\n    }\r\n  }\r\n} "
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data=payload.encode('utf8'))
    json_data = json.loads(response.text)
    print(json_data)
    p = json.dumps(json_data, indent=4, ensure_ascii=False)
    # print(p)
    path = json_data["hits"]
    print(path)
    path2 = json_data["hits"]["hits"]  # ["_source"]["assetType"]
    print(path2)
    path1 = path2[1]['_source']['cf_headlineRu']
    print(json.dumps(path1, indent=4, ensure_ascii=False))
    for i in range(1, 18):
        path1 = path2[i]['_source']['cf_headlineRu']
        print(json.dumps(path1, indent=4, ensure_ascii=False))


def test2():
    payload = "{\r\n  \"query\": {\r\n    \"match\": {\r\n      \"cf_containerType\": {\r\n        \"query\": " \
              "\"лента\"\r\n      }\r\n    }\r\n  }\r\n} "
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload.encode('utf8'))

    print(response.text.encode('utf8'))


def test3():
    response = requests.get(url1)
    json_data = json.loads(response.text)

    print(json_data)


def test4():
    response = requests.post(url3)
    json_data = json.loads(response.text)
    print(json_data)
    Token = json_data["authToken"]
    print(Token)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + Token}

    response = requests.request("GET", url2, headers=headers)
    json_data = json.loads(response.text)

    print(json_data)
    print(json.dumps(json_data, indent=4, ensure_ascii=False))

    rep = json.dumps(json_data, indent=4, ensure_ascii=False)
    f = open('rep.json', 'w')  # открытие в режиме записи
    f.write(rep)
    f.close()
