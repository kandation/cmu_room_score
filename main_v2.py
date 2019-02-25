from load_name_list import LoadNameList
from load_score import LoadScore
from analysis import Analysis

domeList = [
    {
        "gender-id": 0,
        "dome": [1, 2, 3, 4, 5, 6, 8, 12]
    },
    {
        "gender-id": 1,
        "dome": [3, 4, 5, 6, 7]
    },
]


def showMenu():
    print('-' * 30)
    print('(0) Set toggle HistoGram')
    print('(1) Load ListName')
    print('(2) Load Score')
    print('(3) Show Analysis')
    print('(4) Export Data to Excel')
    print('(5) Do it All')
    print('(6) Back to Menu')
    print('(7) Exit')
    print('-' * 30)


from time import gmtime, strftime

dynamicPath = strftime("%Y-%m-%d", gmtime())
showHistoGram = False
_bound = None
_extendPath = './save/' + dynamicPath + '/'

while True:
    lns = LoadNameList(domeList)
    domeSelect = lns.ask()

    while True:
        showMenu()
        menuInp = input('Select Menu >>')
        if menuInp.isdecimal():
            menu = menuInp
            if menu == '0':
                showHistoGram = not showHistoGram
                print('Now Show Histogram is' + str(showHistoGram))
            elif menu == '9':
                inpb = input('Insert Bounary (int)>>')
                if inpb.isdigit():
                    _bound = int(inpb)
                else:
                    print('Input Wrong try agin')
            elif menu == '1':
                lns.getNameList(domeSelect)
                lns.save(_extendPath)
            elif menu == '2':
                ls = LoadScore(domeSelect, _extendPath)
                ls.getStudentScore()
                ls.save(_extendPath)
            elif menu == '3':
                ana = Analysis(domeSelect, extendPath=_extendPath)
                ana.getStatistic(bound=_bound, histogram=showHistoGram)
                ana.save(_extendPath)
            elif menu == '4':
                ana = Analysis(domeSelect, extendPath=_extendPath)
                ana.getExcel()
                ana.saveExcel(_extendPath)
            elif menu == '5':
                lns.getNameList(domeSelect)
                lns.save(_extendPath)
                ls = LoadScore(domeSelect, _extendPath)
                ls.getStudentScore()
                ls.save(_extendPath)
                ana = Analysis(domeSelect, extendPath=_extendPath)
                ana.getStatistic(bound=_bound, histogram=showHistoGram)
                ana.save(_extendPath)
                ana.getExcel()
                ana.saveExcel(_extendPath)
            elif menu == '6':
                break
            elif menu == '7':
                exit()
