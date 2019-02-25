# This api can be run in 2019-02-25
import unicodedata

import requests
from bs4 import BeautifulSoup
import os, json


class LoadScore:
    def __init__(self, __path, __extendPath=None):
        self.__path = self.__autoPath(__path, __extendPath)
        self.__lastData = None
        self.__domeCode = None

    def __autoPath(self, obj, __extend):
        if type(obj) == str:
            return obj
        elif type(obj) == dict:
            if __extend == None:
                raise Exception('Please Enter Extend Path if you use object Caller')
            _dome = obj['reqCode']
            _dome = __extend + 'list_' + _dome + '.json'
            return _dome
        else:
            raise Exception("I dont know this name ListFile Formmat")

    def __loadNameDataFromFile(self):
        if os.path.exists(self.__path):
            fo = open(self.__path, mode="r", encoding="utf8")
            _js = json.loads(fo.read())
            fo.close()
            return _js
        else:
            raise Exception("File Path Not Found")

    def __getStudentIdList(self, js):
        sList = js["list"]
        studentIdList = {}
        for sd in sList:
            studentIdList[sd['sid']] = {
                "id": sd['id'],
                "name": sd['name'],
                "dome": sd['dome'],
                "faculty": sd['faculty'],
                "date": sd['date']

            }
        return studentIdList

    def __loadData(self, sids):
        scoreData = {}
        count = 0
        print('Now GetData From Internet with ' + str(len(sids)) + " items")
        for i, sid in enumerate(sids):
            scoreData[sid] = self.__loadDataFromWebGet(sid)
            print('.', end='')
            if i % 20 == 0 and i > 0:
                print()
            count += 1
        print('\nFinished {} items'.format(count))
        print('-'*30)

        return scoreData

    def __loadDataFromWebGet(self, sid):
        url = "http://udo.oop.cmu.ac.th/event/include/printsct.php?id=" + str(sid)
        re = requests.post(url)
        re.encoding = 'utf-8'
        bs = BeautifulSoup(re.text, "lxml")
        bs = bs.find_all("table")
        return self.__calTableScore(bs)

    def __calTableScore(self, bstables):
        error = []
        sum = self.__calTableScoreSummery(bstables[0])
        if len(sum) <= 0:
            error.append('summery')

        if len(error) > 0:
            _info = {'error': True}
        else:
            activity = self.__calTableScoreTable(bstables[1:3])
            _info = {
                'summery': sum,
                'activity': activity
            }
        return _info

    def __calTableScoreSummery(self, bstable):
        tds = bstable.find_all("td")
        _info = {}
        if self.__cleanStr(tds[1].text) != '':
            _info['name'] = self.__cleanStr(tds[1].text)
            _info['dome'] = self.__cleanStr(tds[3].text)
            _info['nActivity'] = int(self.__cleanStr(tds[5].text).split(' ')[0])
            _info['score'] = int(self.__cleanStr(tds[7].text).split(' ')[0])
        return _info

    def __calTableScoreTable(self, bstables: list) -> list:
        _activityList = []
        for bstable in bstables:
            trContent = bstable.find_all("tr")[1:-1]
            _order_counter = 0
            for tr in trContent:
                _activity = {}
                td = tr.find_all("td")
                _activity['id'] = _order_counter
                _activity['aName'] = str(self.__cleanStr(td[1].text))
                _activity['owner'] = str(self.__cleanStr(td[2].text))
                _activity['score'] = int(self.__cleanStr(td[3].text))
                _order_counter += 1
                _activityList.append(_activity)
        return _activityList

    def __cleanStr(self, text) -> str:
        return str(unicodedata.normalize("NFKD", text)).strip()

    def getStudentScore(self):
        _js = self.__loadNameDataFromFile()
        self.__domeCode = _js['info']['reqCode']
        _data = self.__loadData(self.__getStudentIdList(_js))
        self.__lastData = _data
        return _data


    def save(self, dir="./"):
        import os
        if self.__lastData != None:
            if not os.path.exists(dir):
                os.makedirs(dir)
            fileName = self.__domeCode
            fo = open(dir + "data_" + fileName + ".json", encoding="utf-8", mode="w")
            import json
            fo.write(str(json.dumps(self.__lastData)))
            fo.close()
        else:
            raise Exception("Cannot Save if never Load")
