from bs4 import BeautifulSoup
from operator import itemgetter
import requests
import json
import math


def get_data():
    try:
        name = open("list",'r').read().split('\n')
    except Exception:
        print("No name list, plz create file \"list\" and insert student id with line by line")
        exit(0)
    counter = 0
    data = []

    while counter < len(name):
        url = "http://udo.oop.cmu.ac.th/event/?page=report"
        re = requests.post(url, data={"stu_id":name[counter]})
        re.encoding = 'utf-8'
        bs = BeautifulSoup(re.text, "html.parser")
        bs = bs.find_all("table")
        if len(bs) >= 1:
            p_sid = name[counter]
            p_name = str(bs[0].find_all("td")[1].text)
            p_num = str(bs[0].find_all("td")[-3].text).split("\xa0")[0]
            p_score = str(bs[0].find_all("td")[-1].text).split("\xa0")[0]
            if p_name == "" or p_num == "" or p_score == "":
                parse = [int(p_sid), str(-1 * counter), 0, 0]
            else:
                parse = [int(p_sid), p_name, int(p_num), int(p_score)]
        data.append(parse)
        counter += 1
        print(parse)
    open("data",mode="w+",encoding="utf-8").write(json.dumps(data))


def get_stat():
    try:
        data = json.loads(open("data", mode="r").read())
    except Exception:
        print("Error connot find data file or Wrong formmat")

    data= sorted(data,key=itemgetter(3))
    sum = 0
    sum2 = 0
    min = data[-1][3]
    c = 0
    index_min = None
    for box in data:
        c += 1
        if box[3] != 0 and box[3] < min:
            min = box[3]
            index_min = c
        sum += box[3]
        sum2 += box[3]**2
    dk = {}
    for bx in data:
        if dk.get(bx[3]) == None:
            dk[bx[3]] = 1
        else:
            dk[bx[3]] += 1
    fo = open("histogram.txt",mode="a+")
    for val in dk:
        r = str(val)+"\t"+str(dk[val])+"\n"
        fo.write(r)
    fo.close()

    print("max:",max(data,key=itemgetter(3))[3],max(data,key=itemgetter(3)))
    print("min:",min, data[index_min])
    print("mean:",sum/len(data),"of",len(data))
    print("sd:",math.sqrt(((len(data)*sum2)-(sum)**2)/(len(data)*(len(data)-1))))


def get_excel():
    data = json.loads(open("data", mode="r").read())
    fo = open("excel_output.txt", mode="a+", encoding="utf-8")
    for box in data:
        for d in box:
            fo.write(str(d))
            fo.write("\t")
        fo.write("\n")
    fo.close()

def main():
    while True:
        print("What do you want")
        print("1: new scan")
        print("2: analysis")
        print("3: excel")
        inp = input(">> ")
        if inp == "1":
            get_data()
        elif inp == "2":
            get_stat()
        elif inp == "3":
            get_excel()
        else:
            print("Something wrong bye bye")
            exit(0)

main()