import json
import requests
import pytest

from api.client import RestfulBookerClient
from api import random
from random import randint
from conftest import pytest_runtest_makereport

url = "http://5.227.126.79:9200/mediadev-elvis-metadata-avm/_search?size=19"
# url1 = "http://5.227.126.79:9200/mediadev-elvis-metadata-avm/_search?data=%7B%22query%22%3A%7B%22match%22%3A%7B%22cf_containerType%22%3A%7B%22query%22%3A%22лента%22%7D%7D%7D%7D"
url1 = "http://elvis2.dev.itass.local/api/asset/search?q=BTF4Qnx54k0By0n_e_orYJ"
url2 = "http://elvis2.dev.itass.local/api/asset/search?q=/Data/Sections&size=25"
url22 = "http://elvis2.dev.itass.local/api/asset/search?q=/Reportages&size=5475"
url3 = "http://elvis2.dev.itass.local/services/apilogin?username=cvtTest2&password=cvtTest2"
# ?assetIds=BTF4Qnx54k0By0n_e_orYJ

Token = ""


# вызывает список лент по способу бекендеров тасс медиа
class TestAPITASS:
    def test_n1_spisok_lent(self):
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
    def test_n3_console_reportezhi(self):
        response = requests.post(url3)
        json_data = json.loads(response.text)
        print(json_data)
        Token = json_data["authToken"]
        print(Token)
        print('--------------------------')

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + Token}

        response = requests.request("GET", url1, headers=headers)
        json_data = json.loads(response.text)

        # print(json_data)
        print(json.dumps(json_data, indent=4, ensure_ascii=False))
        rep = json.dumps(json_data, indent=4, ensure_ascii=False)
        f = open('rep.json', 'w')  # открытие в режиме записи
        f.write(rep)
        f.close()
        path1 = json_data['hits'][0]['metadata']
        if 'cf_containerType' in path1:
            repor = json_data['hits'][0]['metadata']['cf_containerType']
            if repor == 'репортаж':
                if 'cf_headlineRu' in path1:
                    path2 = json_data['hits'][0]['metadata']['cf_headlineRu']  # ['cf_headlineRu'] name
                    print(json.dumps(path2, indent=4, ensure_ascii=False))

                if 'cf_wireSections' in path1:
                    path2 = json_data['hits'][0]['metadata']['cf_wireSections']  # ['cf_headlineRu'] name
                    print(json.dumps(path2, indent=4, ensure_ascii=False))

                if 'status' in path1:
                    path3 = json_data['hits'][0]['metadata']['status']  # ['cf_headlineRu'] name
                    id_report = json_data['hits'][0]['id']
                    print(json.dumps(path3, indent=4, ensure_ascii=False), ' id - ',
                          json.dumps(id_report, indent=4, ensure_ascii=False))
                    print()

    # выводит список лент по API документации DAM
    def test_n4_spisok_lent(self):
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
        # print(json.dumps(json_data, indent=4, ensure_ascii=False))

        rep = json.dumps(json_data, indent=4, ensure_ascii=False)
        f = open('rep.json', 'w')  # открытие в режиме записи
        f.write(rep)
        f.close()
        for i in range(1, 25):
            path1 = json_data['hits'][i]['metadata']
            if 'cf_headlineRu' in path1:
                path2 = json_data['hits'][i]['metadata']['cf_headlineRu']  # ['cf_headlineRu'] name
                print(json.dumps(path2, indent=4, ensure_ascii=False))
            # else:
            #     print(i)
            if 'status' in path1:
                path3 = json_data['hits'][i]['metadata']['status']  # ['cf_headlineRu'] name
                print(json.dumps(path3, indent=4, ensure_ascii=False))
                print()
            # else:
            #     print(i)

    # создает json док с репортажами
    def test_n5_create_json_reportazhi(self):
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
        # f = open('rep.json', 'w')  # открытие в режиме записи
        # f.write(str(rep))
        # f.close()
        cn = 0
        f1 = open('rep2.json', 'w')
        f1.write('{' + '\n')
        f1.write('  "Репортажи": [' + '\n')
        for i in range(0, 5+-475):
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
                        path2 = json_data['hits'][i]['metadata']['cf_plannedPubDate']['formatted'] # ['cf_headlineRu'] name
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

    # выводит в консоли репортаж
    def test_n7_console_reportezhi_srawnyt(self):
        self.test_n3_console_reportezhi()
        response = requests.post(url3)
        json_data = json.loads(response.text)
        print(json_data)
        Token = json_data["authToken"]
        print(Token)
        print('--------------------------')

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

