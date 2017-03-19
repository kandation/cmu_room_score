from bs4 import BeautifulSoup
from operator import itemgetter
import requests
import json
import math
import os
dome = 7
gender = 1

print("Now system working in : dome",dome," male" if gender == 1 else " female")

def get_data():
    try:
        name = open("list_"+str(dome)+str(gender),'r').read().split('\n')
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
    open("data_"+str(dome)+str(gender),mode="w+",encoding="utf-8").write(json.dumps(data))


def get_stat():
    error = False
    try:
        data = json.loads(open("data_"+str(dome)+str(gender), mode="r").read())
    except Exception:
        print("Error connot find data file or Wrong formmat")
        error = True

    if not error:
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
        if os.path.isfile("histogram_"+str(dome)+str(gender)+".txt"):
            os.remove("histogram_"+str(dome)+str(gender)+".txt")
        fo = open("histogram_"+str(dome)+str(gender)+".txt",mode="a+")
        print("HistoGram")
        print("---------------------------------")
        med_dict = []
        for val in dk:
            r = str(val)+"\t"+str(dk[val])+"\n"
            med_dict.append(int(val))
            print(val,"   \t:","|"*int(dk[val]),dk[val])
            fo.write(r)
        fo.close()
        print("---------------------------------")
        mx = max(data,key=itemgetter(3))[3]
        med_index = len(dk) / 2
        med_up = med_dict[math.floor(med_index)-1]
        med_dn = med_dict[math.ceil(med_index)-1]
        if len(dk)%2 == 0:
            med = med_dict[int(med_index)-1]
        else:
            med = (med_up + med_dn) / 2
        print("max   :",mx ,max(data,key=itemgetter(3)))
        print("min   :",min, data[index_min])
        print("mean  :",sum/len(data),"of",len(data))
        print("Median:",med)
        print("sd:",math.sqrt(((len(data)*sum2)-(sum)**2)/(len(data)*(len(data)-1))))


def get_excel():
    try:
        data = json.loads(open("data_"+str(dome)+str(gender), mode="r").read())
        fo = open("excel_output_"+str(dome)+str(gender)+".txt", mode="a+", encoding="utf-8")
        for box in data:
            for d in box:
                fo.write(str(d))
                fo.write("\t")
            fo.write("\n")
        fo.close()
    except Exception:
        print("Canont find file or file wrong formmat")


def main():
    while True:
        print("\nWhat do you want")
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