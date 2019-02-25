import os, json, math, statistics


class Analysis:
    def __init__(self, path, extendPath=None, dome=''):
        self.__lastData = None
        self.__lastDataExcel = None
        self.__domeCode = None
        self.__path = self.__autoPath(path, extendPath, dome)


    def __autoPath(self, obj, __extend, __dome):
        if type(obj) == str:
            if __dome == '':
                raise Exception('Enter Dome Id Or Insert DomeObject it the ways EZ')
            self.__domeCode = __dome
            return obj
        elif type(obj) == dict:
            if __extend == None:
                raise Exception('Please Enter Extend Path if you use object Caller')
            _dome = obj['reqCode']
            _dome = __extend + 'data_' + _dome + '.json'
            self.__domeCode = obj['reqCode']
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

    def getStatistic(self, bound=None, histogram=False):
        js = self.__loadNameDataFromFile()
        scoreList = []
        scoreListForZero = []
        maxScore = -9999
        minScore = 9999
        maxScoreId = 'na'
        minScoreId = 'na'

        for i in js:
            if 'error' not in js[i]:
                _score = js[i]['summery']['score']
                scoreList.append(_score)
                scoreListForZero.append(_score)
                if _score > maxScore:
                    maxScore = _score
                    maxScoreId = i
                if _score > maxScore < minScore:
                    minScore = _score
                    minScoreId = i

            else:
                scoreListForZero.append(0)

        saveText = ''
        saveText += '-' * 30 + '\n'
        saveText += 'Analysis without None Score\n'
        saveText += '-' * 30 + '\n'
        saveText += self.__showStat(scoreList) + '\n'
        if histogram:
            saveText += '-' * 30 + '\n'
            saveText += self.__histogram(scoreList, bound) + '\n'
        saveText += '-' * 30 + '\n'
        saveText += 'Analysis All Regist\n'
        saveText += '-' * 30 + '\n'
        saveText += self.__showStat(scoreListForZero) + '\n'
        if histogram:
            saveText += '-' * 30 + '\n'
            saveText += self.__histogram(scoreListForZero, bound) + '\n'
        print(saveText)
        self.__lastData = saveText

    def __histogram(self, score, bound=None):
        saveText = ''
        from collections import Counter
        letters_hist = Counter(score)
        # print(letters_hist.most_common())
        k = sorted(letters_hist.items(), key=lambda letters_hist: (letters_hist, ()), reverse=False)
        showBound = ''
        limitBound = -1
        if bound is not None:
            kBound = sorted(letters_hist.items(), key=lambda letters_hist: (letters_hist, ()), reverse=True)
            _sum = 0
            for c in kBound:
                _sum += c[1]
                if _sum >= bound:
                    showBound = str(_sum)
                    limitBound = c[0]
                    break
        for p in k:
            if limitBound == p[0]:
                showBound = '<-----|out|@' + showBound
                text = '{:5} {} {} {}'.format(p[0], '░' * p[1], p[1], showBound)
            else:
                text = '{:5} {} {}'.format(p[0], '░' * p[1], p[1])
            saveText += text + '\n'
        return saveText

    def __showStat(self, score):
        _n = len(score)
        _min = min(score)
        _max = max(score)
        _mean = statistics.mean(score)
        _sd = statistics.stdev(score)
        _med = statistics.median(score)
        _mod = statistics.mode(score)
        text = "n       ={n:10.4f}\nMin     ={min:10.4f}\nMax     ={max:10.4f}\nMean    ={mean:10.4f}" \
               "\nSD      ={sd:10.4f}\nMedian  ={med:10.4f}\nMode    ={mod:10.4f}".format(
            n=_n, min=_min, max=_max, mean=_mean, sd=_sd, med=_med, mod=_mod
        )
        return text

    def getExcel(self):
        js = self.__loadNameDataFromFile()
        scoreList = []
        scoreListForZero = []
        serializeText = 'sid\tname\tnActivity\tScore\n'

        for i in js:
            serializeText += i + '\t'
            if 'error' not in js[i]:
                serializeText += str(js[i]['summery']['name']) + '\t'
                serializeText += str(js[i]['summery']['nActivity']) + '\t'
                serializeText += str(js[i]['summery']['score']) + '\t'
                _score = js[i]['summery']['score']
                scoreList.append(_score)
                scoreListForZero.append(_score)
            else:
                scoreListForZero.append(0)
            serializeText += '\n'
        self.__lastDataExcel = serializeText

    def save(self, dir="./"):
        import os
        if self.__lastData != None:
            if not os.path.exists(dir):
                os.makedirs(dir)
            fileName = self.__domeCode
            fo = open(dir +'log_' + fileName + ".txt", encoding="utf-8", mode="w")

            fo.write(str(self.__lastData))
            fo.close()
        else:
            raise Exception("Cannot Save if never Load")

    def saveExcel(self, dir="./"):
        import os
        if self.__lastDataExcel != None:
            if not os.path.exists(dir):
                os.makedirs(dir)
            fileName = self.__domeCode
            fo = open(dir +'excel_' + fileName + ".txt", encoding="utf-8", mode="w")
            fo.write(str(self.__lastDataExcel))
            fo.close()
            print('-'*30)
            print('Export Tab Forrmat @'+dir +'excel_' + fileName + ".txt")
        else:
            raise Exception("Cannot Save if never Load")

