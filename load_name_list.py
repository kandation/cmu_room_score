# This api can be run in 2019-02-25
import requests
from bs4 import BeautifulSoup


class LoadNameList:
    def __init__(self, _domeList):
        self.__domeList = _domeList
        self.__lastNameList = None

    def __domeListTranslate(self):
        code = []
        for l in self.__domeList:
            for d in l["dome"]:
                nameGender = self.__domeListTranslate_gender(l["gender-id"])
                nameRoom = self.__domeListTranslate_room(d)
                _code = str(l["gender-id"]) + str(d)
                _adeptive_code = self.__domeListTranslate_gender_code(l["gender-id"]) + str(nameRoom)
                _textShow = "[{id}] for {gender} {dome}".format(id=_code, gender=nameGender, dome=nameRoom)
                code.append({
                    "code": _code,
                    "reqCode": _adeptive_code,
                    "text": nameGender + " " + nameRoom,
                    "show": _textShow
                })
        return code

    def __domeListTranslate_room(self, rNum):
        return "0" + str(rNum) if int(rNum) < 10 else str(rNum)

    def __domeListTranslate_gender(self, gid):
        return "female" if gid == 0 else "male"

    def __domeListTranslate_gender_code(self, gid):
        return "w" if gid == 0 else "m"

    def __loadPage(self, domeCode):
        url = "https://www3.reg.cmu.ac.th/roombooking/senior/liststudy.php?dorm="
        url += str(domeCode)
        re = requests.get(url)
        re.encoding = 'utf-8'
        return re.text

    def __loadName(self, page):
        bs = BeautifulSoup(page, "html.parser")
        bs = bs.find_all("tr")
        return self.__nameClean(bs[1:])

    def __nameClean(self, bsTrs):
        regList = []
        for trs in bsTrs:
            tds = trs.find_all("td")
            _tagName = ["id", "sid", "name", "faculty", "dome", "date"]
            _js = {}
            for tdi, td in enumerate(tds):
                _tdText = str(td.text).strip()
                _js[_tagName[tdi]] = _tdText
            regList.append(_js)
        return regList

    def getNameList(self, domeListCode):
        regCode = domeListCode["reqCode"]
        nameList = self.__loadName(self.__loadPage(regCode))
        self.__lastNameList = {"info": domeListCode, "list": nameList}
        return self.__lastNameList

    def ask(self):
        domeListJS = self.__domeListTranslate()
        found = None
        while found == None:
            print("-" * 30)
            print("Select Dome for Calculate")
            print("-"*30)
            for dome in domeListJS:
                print(dome["show"])
            print("And Enter 0 to Exit")
            inp = str(input(">>"))
            for dome in domeListJS:
                if inp == dome["code"]:
                    found = dome
                if inp == "0":
                    exit(0)
            if found == None:
                print("Not Found Try agine")
        print("-"*30)
        return found

    def save(self, dir="./"):
        import os
        if self.__lastNameList != None:
            if not os.path.exists(dir):
                os.makedirs(dir)
            fileName = self.__lastNameList["info"]["reqCode"]
            fo = open(dir + "list_"+fileName+".json", encoding="utf-8", mode="w")
            import json
            fo.write(str(json.dumps( self.__lastNameList)))
            fo.close()
        else:
            raise Exception("Cannot Save if never Load")





