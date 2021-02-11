import json
import time

import requests
import pytest
import urllib

from api.client import RestfulBookerClient
# from api import random
from random import randint
from conftest import pytest_runtest_makereport

url = "http://5.227.126.79:9200/mediadev-elvis-metadata-avm/_search?size=19"
# url1 = "http://5.227.126.79:9200/mediadev-elvis-metadata-avm/_search?data=%7B%22query%22%3A%7B%22match%22%3A%7B%22cf_containerType%22%3A%7B%22query%22%3A%22лента%22%7D%7D%7D%7D"
url1 = "http://elvis2.dev.itass.local/api/asset/search?q=BTF4Qnx54k0By0n_e_orYJ"
url2 = "http://elvis2.dev.itass.local/api/asset/search?q=/Data/Sections&size=30"
url22 = "http://elvis2.dev.itass.local/api/asset/search?q=/Reportages&size=5475"
url3 = "http://elvis2.dev.itass.local/services/apilogin?username=cvtTest2&password=cvtTest2"
# ?assetIds=BTF4Qnx54k0By0n_e_orYJ

Token = ""


def benchmark(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(end - start)
        assert end - start <= 0.5
        return result

    return wrapper()


# вызывает список лент по способу бекендеров тасс медиа
class TestAPITASS:
    def test_token(self):
        response = requests.post(url3)
        json_data = json.loads(response.text)
        print(json_data)
        Token = json_data["authToken"]
        print(Token)
        print('--------------------------')
        return Token

    def test_n1_spisok_lent(self):
        payload = "{\r\n  \"query\": {\r\n    \"match\": {\r\n      \"cf_containerType\": {\r\n        \"query\": " \
                  "\"лента\"\r\n      }\r\n    }\r\n  }\r\n} "
        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"cf_containerType": {"query": "лента"}}}  # ,
                        # { "match": { "folderPath": "/Data/Sections" } }
                    ]
                }
            }
        }  # Если по одному ключу находится несколько словарей, формируем список словарей
        # answer = requests.request("POST", url, data=json.dumps(data), headers=headers)
        # print(answer)
        # response_x = answer.json()
        # print(json.dumps(response_x, indent=4, ensure_ascii=False))

        # response = requests.request("GET", url, headers=headers, data=payload.encode('utf8'))
        response = requests.request("GET", url, headers=headers, data=json.dumps(data))
        json_data = json.loads(response.text)
        print(json_data)
        p = json.dumps(json_data, indent=4, ensure_ascii=False)
        print(p)
        path = json_data["hits"]
        print(path)
        path2 = json_data["hits"]["hits"]  # ["_source"]["assetType"]
        print(path2)
        path1 = path2[1]['_source']['cf_headlineRu']
        print(json.dumps(path1, indent=4, ensure_ascii=False))
        for i in range(1, 18):
            path1 = path2[i]['_source']['cf_headlineRu']
            print(json.dumps(path1, indent=4, ensure_ascii=False))

    # запросить репортажи по конкретмым полям
    def test_n1_1_spisok_lent(self):
        start = time.time()
        payload = "{\r\n  \"query\": {\r\n    \"match\": {\r\n      \"cf_containerType\": {\r\n        \"query\": " \
                  "\"лента\"\r\n      }\r\n    }\r\n  }\r\n} "
        headers = {
            'Content-Type': 'application/json'
        }

        data = {
          "query": { "match": { "_id": "0dqUtibZKYT9lLkwZp46s1" } }
        }

        # data = {
        #     "query": {
        #         "bool": {
        #             "must": [
        #                 {"match": {"cf_containerType": {"query": "репортаж"}}}  # ,
        #                 # { "match": { "cf_wireSections": "MILITARY" } }
        #             ]
        #         }
        #     }
        # }  # Если по одному ключу находится несколько словарей, формируем список словарей
        # answer = requests.request("POST", url, data=json.dumps(data), headers=headers)
        # print(answer)
        # response_x = answer.json()
        # print(json.dumps(response_x, indent=4, ensure_ascii=False))

        # response = requests.request("GET", url, headers=headers, data=payload.encode('utf8'))
        urll1 = 'http://5.227.126.79:9200/mediadev-elvis-metadata-avm/_search?size=199'
        response = requests.request("GET", url, headers=headers, data=json.dumps(data))
        json_data = json.loads(response.text)
        # print(json_data)
        p = json.dumps(json_data, indent=4, ensure_ascii=False)
        # print(p)
        path = json_data["hits"]
        # print(path)
        path2 = json_data["hits"]["hits"][0]['_source']  # ["_source"]["assetType"]
        # print(json.dumps(path2, indent=4, ensure_ascii=False))
        # path1 = path2[0]['_source']['cf_headlineRu']
        # print(json.dumps(path1, indent=4, ensure_ascii=False))
        print()
        print('-------------------------------------------------------------------------------------------------')
        print()
        pab = ['cf_objectId', 'iptcCreated', 'copyright', 'cf_headlineRu', 'cf_descriptionFirst', 'cf_stockIdList']
        pab2 = ['ID DAM: ', 'Дата съемки: ', 'Авторское право: ', 'Заголовок: ', 'Описание: ', 'Библиотека: ']
        for i in range(0, 6):
            if pab[i] in path2 and pab[i] != 'cf_stockIdList' and pab[i] != 'iptcCreated':
                path1 = path2[pab[i]]
                print(pab2[i], json.dumps(path1, indent=4, ensure_ascii=False))
            else:
                if pab[i] != 'cf_stockIdList' and pab[i] != 'iptcCreated':
                    print(pab2[i])
                if pab[i] in path2 and pab[i] == 'cf_stockIdList':
                    path1s = path2[pab[i]]
                    d = len(path1s)
                    # print(len(path1s))
                    print(pab2[i])
                    for j in range(0, d):
                        path1 = path2[pab[i]][j]
                        # print(path1)
                        headers = {'Content-Type': 'application/json'}
                        data = {"query": {"match": {"_id": path1}}}
                        response = requests.request("GET", url, headers=headers, data=json.dumps(data))
                        json_data = json.loads(response.text)
                        ps2 = json_data["hits"]["hits"][0]['_source']['cf_headlineRu']
                        print('           ', json.dumps(ps2, indent=4, ensure_ascii=False))

                if pab[i] in path2 and pab[i] == 'iptcCreated':
                    path1 = path2[pab[i]]['formatted']
                    print(pab2[i], path1)
            # старый код
            # if 'cf_objectId' in path2[i]['_source']:
            #     path1 = path2[i]['_source']['cf_objectId']
            #     print(json.dumps(path1, indent=4, ensure_ascii=False))
            # if 'iptcCreated' in path2[i]['_source']:
            #     path1 = path2[i]['_source']['iptcCreated']['formatted']
            #     print(json.dumps(path1, indent=4, ensure_ascii=False))
            # if 'copyright' in path2[i]['_source']:
            #     path1 = path2[i]['_source']['copyright']
            #     print(json.dumps(path1, indent=4, ensure_ascii=False))
            # if 'cf_headlineRu' in path2[i]['_source']:
            #     path1 = path2[i]['_source']['cf_headlineRu']
            #     print(json.dumps(path1, indent=4, ensure_ascii=False))
            # if 'cf_descriptionRu' in path2[i]['_source']:
            #     path1 = path2[i]['_source']['cf_descriptionRu']
            #     print(json.dumps(path1, indent=4, ensure_ascii=False))
            # if 'cf_stockIdList' in path2[i]['_source']:
            #     path1 = path2[i]['_source']['cf_stockIdList']
            #     print(json.dumps(path1, indent=4, ensure_ascii=False))
        end = time.time()
        print(end - start)

    # составляет блок с репортажами
    def test_n2_create_bloc_reportazhi(self):
        response = requests.post(url3)
        json_data = json.loads(response.text)
        print(json_data)
        Token = json_data["authToken"]
        print(Token)
        print('--------------------------')

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + Token}

        response = requests.request("GET", url22, headers=headers)
        json_data = json.loads(response.text)

        # print(json_data)
        # print(json.dumps(json_data, indent=4, ensure_ascii=False))

        rep = json.dumps(json_data, indent=4, ensure_ascii=False)
        f = open('rep.json', 'w')  # открытие в режиме записи
        # f.write(str(rep))
        f.close()
        f1 = open('rep1.json', 'w')
        for i in range(0, 414):
            path1 = json_data['hits'][i]['metadata']
            if 'cf_containerType' in path1:
                repor = json_data['hits'][i]['metadata']['cf_containerType']
                if repor == 'репортаж' and 'cf_wireSections' in path1:
                    if 'cf_headlineRu' in path1:
                        path2 = json_data['hits'][i]['metadata']['cf_headlineRu']  # ['cf_headlineRu'] name
                        f1.write('Название: ' + str(path2) + '\n')
                        # print(json.dumps(path2, indent=4, ensure_ascii=False))
                    # else:
                    #     print(i)
                    if 'cf_wireSections' in path1:
                        path2 = json_data['hits'][i]['metadata']['cf_wireSections']  # ['cf_headlineRu'] name
                        f1.write('Ленты:    ' + str(path2) + '\n')
                        # print(json.dumps(path2, indent=4, ensure_ascii=False))
                    # else:
                    #     print(i)
                    if 'status' in path1:
                        path2 = json_data['hits'][i]['metadata']['status']  # ['cf_headlineRu'] name
                        id_report = json_data['hits'][i]['id']
                        f1.write('Статус:   ' + str(path2) + ',  id - ')
                        f1.write(str(id_report) + '\n')
                        f1.write('\n')
                        f1.write('---------------------------' + '\n')
                        # print(json.dumps(path2, indent=4, ensure_ascii=False), ' - ', i, ' id - ', json.dumps(id_report, indent=4, ensure_ascii=False))
                        # print(' id - ', json.dumps(id_report, indent=4, ensure_ascii=False))
                        print()
                    # else:
                    #     print(i)
        f.close()

    # выводит в консоли репортаж
    @pytest.mark.parametrize("id1",
                             ('2W2mGul-4tV8aT3iNz7xPQ', 'BTF4Qnx54k0By0n_e_orYJ')
                             )
    def test_n3_console_reportezhi(self, id1):
        start = time.time()
        Token = self.test_token()
        url_rep = "http://elvis2.dev.itass.local/"  # 2W2mGul-4tV8aT3iNz7xPQ   api/asset/search?q=BTF4Qnx54k0By0n_e_orYJ
        api = 'api/asset/search'
        url_rep += api
        params = dict(q=id1)
        url_rep += '?' + urllib.parse.urlencode(params)
        print(url_rep)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + Token}

        response = requests.request("GET", url_rep, headers=headers)
        json_data = json.loads(response.text)

        # print(json_data)
        # print(json.dumps(json_data, indent=4, ensure_ascii=False))
        rep = json.dumps(json_data, indent=4, ensure_ascii=False)
        f = open('rep.json', 'w')  # открытие в режиме записи
        f.write(rep)
        f.close()
        path2 = json_data['hits'][0]['metadata']
        print()
        print('-------------------------------------------------------------------------------------------------')
        print()
        pab = ['cf_objectId', 'iptcCreated', 'copyright', 'cf_headlineRu', 'cf_descriptionFirst', 'cf_stockIdList']
        pab2 = ['ID DAM: ', 'Дата съемки: ', 'Авторское право: ', 'Заголовок: ', 'Описание: ', 'Библиотека: ']
        for i in range(0, 6):
            if pab[i] in path2 and pab[i] != 'cf_stockIdList' and pab[i] != 'iptcCreated':
                path1 = path2[pab[i]]
                print(pab2[i], json.dumps(path1, indent=4, ensure_ascii=False))
            else:
                if pab[i] != 'cf_stockIdList' and pab[i] != 'iptcCreated':
                    print(pab2[i])
                if pab[i] in path2 and pab[i] == 'cf_stockIdList':
                    path1s = path2[pab[i]]
                    d = len(path1s)
                    # print(len(path1s))
                    print(pab2[i])
                    for j in range(0, d):
                        path1 = path2[pab[i]][j]
                        # print(path1)
                        headers = {'Content-Type': 'application/json'}
                        data = {"query": {"match": {"_id": path1}}}
                        response = requests.request("GET", url, headers=headers, data=json.dumps(data))
                        json_data = json.loads(response.text)
                        ps2 = json_data["hits"]["hits"][0]['_source']['cf_headlineRu']
                        print('           ', json.dumps(ps2, indent=4, ensure_ascii=False))

                if pab[i] in path2 and pab[i] == 'iptcCreated':
                    path1 = path2[pab[i]]['formatted']
                    print(pab2[i], path1)
        # старый код
        # if 'cf_containerType' in path1:
        #     repor = json_data['hits'][0]['metadata']['cf_containerType']
        #     if repor == 'репортаж' or repor == 'коллекция':
        #         if 'cf_headlineRu' in path1:
        #             path2 = json_data['hits'][0]['metadata']['cf_headlineRu']  # ['cf_headlineRu'] name
        #             print(json.dumps(path2, indent=4, ensure_ascii=False))
        #
        #         if 'cf_wireSections' in path1:
        #             path2 = json_data['hits'][0]['metadata']['cf_wireSections']  # ['cf_headlineRu'] name
        #             print(json.dumps(path2, indent=4, ensure_ascii=False))
        #
        #         if 'status' in path1:
        #             path3 = json_data['hits'][0]['metadata']['status']  # ['cf_headlineRu'] name
        #             id_report = json_data['hits'][0]['id']
        #             print(json.dumps(path3, indent=4, ensure_ascii=False), ' id - ',
        #                   json.dumps(id_report, indent=4, ensure_ascii=False))
        #             print()
        #             print('------------------------------------------------')
        #             print()
        #
        #         if 'cf_objectId' in path1:
        #             path4 = json_data['hits'][0]['metadata']['cf_objectId']
        #             path4 = (json.dumps(path4, indent=4, ensure_ascii=False))
        #         else:
        #             path4 = ' '
        #         print('ID DAM:  ', path4)
        #         if 'iptcCreated' in path1:
        #             path4 = json_data['hits'][0]['metadata']['iptcCreated']['formatted']
        #             path4 = (json.dumps(path4, indent=4, ensure_ascii=False))
        #         else:
        #             path4 = ' '
        #         print('Дата создания:  ', path4)
        #         if 'copyright' in path1:
        #             path4 = json_data['hits'][0]['metadata']['copyright']
        #             path4 = (json.dumps(path4, indent=4, ensure_ascii=False))
        #         else:
        #             path4 = ' '
        #         print('Авторское право:  ', path4)
        #         if 'cf_headlineRu' in path1:
        #             path4 = json_data['hits'][0]['metadata']['cf_headlineRu']
        #             path4 = (json.dumps(path4, indent=4, ensure_ascii=False))
        #         else:
        #             path4 = ' '
        #         print('Заголовок:  ', path4)
        #         if 'cf_descriptionRu' in path1:
        #             path4 = json_data['hits'][0]['metadata']['cf_descriptionRu']
        #             path4 = (json.dumps(path4, indent=4, ensure_ascii=False))
        #         else:
        #             path4 = ' '
        #         print('Описание:  ', path4)
        #         if 'cf_stockIdList' in path1:
        #             path4 = json_data['hits'][0]['metadata']['cf_stockIdList']
        #             path4 = (json.dumps(path4, indent=4, ensure_ascii=False))
        #         else:
        #             path4 = ' '
        #         print('Библиотека:  ', path4)
        end = time.time()
        print(end - start)

    # выводит список лент по API документации DAM
    def test_n4_spisok_lent(self):
        path333 = 0
        Token = self.test_token()

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + Token}

        response = requests.request("GET", url2, headers=headers)
        json_data = json.loads(response.text)

        print(json_data)
        # print(json.dumps(json_data, indent=4, ensure_ascii=False))

        rep = json.dumps(json_data, indent=4, ensure_ascii=False)
        f = open('rep.json', 'w')  # открытие в режиме записи
        f.write(rep)
        f.close()
        for i in range(1, 28):
            path1 = json_data['hits'][i]['metadata']
            if 'cf_headlineRu' in path1:
                path2 = json_data['hits'][i]['metadata']['cf_headlineRu']  # ['cf_headlineRu'] name
                print(json.dumps(path2, indent=4, ensure_ascii=False))
            # else:
            #     print(i)
            if 'status' in path1:
                path3 = json_data['hits'][i]['metadata']['status']  # ['cf_headlineRu'] name
                print(json.dumps(path3, indent=4, ensure_ascii=False))
                path33 = json.dumps(path3, indent=4, ensure_ascii=False)
                if path33 == '"выпущено на сайт"':
                    path333 += 1
                    print("--------------------------------------------")
                print()
            # else:
            #     print(i)
        print(path333)

    # создает json док с репортажами
    def test_n5_create_json_reportazhi(self):
        Token = self.test_token()

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + Token}

        response = requests.request("GET", url22, headers=headers)
        json_data = json.loads(response.text)

        # print(json_data)
        # print(json.dumps(json_data, indent=4, ensure_ascii=False))

        rep = json.dumps(json_data, indent=4, ensure_ascii=False)
        # f = open('rep.json', 'w')  # открытие в режиме записи
        # f.write(str(rep))
        # f.close()
        cn = 0
        f1 = open('rep2.json', 'w')
        f1.write('{' + '\n')
        f1.write('  "Репортажи": [' + '\n')
        for i in range(0, 5 + -475):
            path1 = json_data['hits'][i]['metadata']
            path0 = json_data['hits'][i]
            if 'cf_containerType' in path1:
                repor = json_data['hits'][i]['metadata']['cf_containerType']
                if repor == 'репортаж' and 'cf_wireSections' in path1 and 'id' in path0:
                    f1.write('   {' + '\n')
                    if 'cf_headlineRu' in path1:
                        path2 = json_data['hits'][i]['metadata']['cf_headlineRu']  # ['cf_headlineRu'] name
                        path2 = str(path2).replace('"', "'")
                        # print(path2)
                        f1.write('      "Название": ' + '"' + str(path2) + '",' + '\n')
                        # print(json.dumps(path2, indent=4, ensure_ascii=False))
                    # else:
                    #     print(i)
                    if 'cf_wireSections' in path1:
                        path2 = json_data['hits'][i]['metadata']['cf_wireSections']  # ['cf_headlineRu'] name
                        path2 = str(path2)
                        path2 = path2[1: -1]
                        f1.write('      "Ленты": ' + '"' + str(path2) + '",' + '\n')
                        # print(json.dumps(path2, indent=4, ensure_ascii=False))
                    # else:
                    #     print(i)
                    if 'cf_plannedPubDate' in path1:
                        path2 = json_data['hits'][i]['metadata']['cf_plannedPubDate'][
                            'formatted']  # ['cf_headlineRu'] name
                        path2 = str(path2)
                        path2 = path2[1: -1]
                        f1.write('      "Дата будликации": ' + '"' + str(path2) + '",' + '\n')
                        # print(json.dumps(path2, indent=4, ensure_ascii=False))
                    # else:
                    #     print(i)
                    if 'status' in path1:
                        path2 = json_data['hits'][i]['metadata']['status']  # ['cf_headlineRu'] name
                        id_report = json_data['hits'][i]['id']
                        f1.write('      "Статус": ' + '"' + str(path2) + '",' + '\n')
                        f1.write('      "ID": ' + '"' + str(id_report) + '"' + '\n')
                        f1.write('\n')
                        # f1.write('---------------------------' + '\n')
                        # print(json.dumps(path2, indent=4, ensure_ascii=False), ' - ', i, ' id - ', json.dumps(id_report, indent=4, ensure_ascii=False))
                        # print(' id - ', json.dumps(id_report, indent=4, ensure_ascii=False))
                        # print()
                    cn = cn + 1
                    f1.write('   },' + '\n')
                    # else:
                    #     print(i)
        f1.write(' {}  ]' + '\n')
        f1.write('}' + '\n')
        # f.close()
        print(cn)

    # парсит json док с репортажами из test_n5
    def test_n6_pars_json_reportazhi(self):
        with open('rep2.json', 'r') as fh:  # открываем файл на чтение
            data = json.load(fh)  # загружаем из файла данные в словарь data
        print(data)
        for i in range(0, 121):
            path2 = data['Репортажи'][i]['Ленты']
            if path2 == "'ART'":
                path3 = data['Репортажи'][i]['Название']
                print(json.dumps(path3, indent=4, ensure_ascii=False))
                print(json.dumps(path2, indent=4, ensure_ascii=False))
                print(i)
                print('--------------------------------')
                print(' ')
        # print("1")
        # with open('rep2.json') as f:
        #     d = json.load(f)
        #     print(d)
        # print("2")
        # with open('rep2.json', 'r') as f:
        #     nums = f.read()
        # print(nums)
        # print("3")
        # json_data = json.loads(nums)
        # print(json_data)
        # print("4")

    # выводит сравнивает пришедший json с тем который хранится в файле как правильный
    def test_n7_console_reportezhi_srawnyt(self):
        self.test_n3_console_reportezhi()
        Token = self.test_token()

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + Token}

        response = requests.request("GET", url1, headers=headers)
        json_data = json.loads(response.text)

        # print(json_data)
        print(json.dumps(json_data, indent=4, ensure_ascii=False))
        response1 = json.dumps(json_data, indent=4, ensure_ascii=False)
        with open('rep.json', 'r') as fh:  # открываем файл на чтение
            data = json.load(fh)  # загружаем из файла данные в словарь data
        print(data)
        assert json_data == data

        data1 = json.dumps(data, indent=4, ensure_ascii=False)
        assert response1 == data1

    # создание сущности в DAM через API
    # def test_n8_create_reportezh(self):
    #     Token = self.test_token()
    #
    #     headers = {
    #         'Content-Type': 'application/json',
    #         'Authorization': 'Bearer ' + Token}
    #     urll = 'http://elvis2.dev.itass.local/services/create?folderPath=/Reportages&assetType=collection&name=TASS%20New%20TASS'
    #
    #     response = requests.request("POST", urll, headers=headers, )
    #     json_data = json.loads(response.text)
    #
    #     print(json_data)
    #     print(json.dumps(json_data, indent=4, ensure_ascii=False))
