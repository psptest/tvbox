#!/usr/bin/env python
# coding: utf-8
import requests,re,gzip,chardet,json,urllib,hashlib
#from pypinyin import pinyin, Style

def wfile(name,txt):
    w=open(name, "wb+")
    w.write(txt.encode())
    w.close()
def rfile(name):
    w=open(name, 'r+')
    txt=w.read()
    w.close()
    return txt
def takeSecond(elem):
    return pinyin(elem["title"],style=Style.TONE3)
def get2():
    zb_list=[];
    bl={}
    count=0;

    ##http://api.vipmisss.com:81/mf/json.txt
    r1 = requests.get("http://api.vipmisss.com:81/mf/json.txt",timeout=5)
    pingtai=json.loads(r1.content.decode())
    txt=""
    for value in pingtai["pingtai"]:
        if int(value['Number'])>0:
            try:
                r2=requests.get("http://api.vipmisss.com:81/mf/"+value['address'],timeout=5)
                zhubo=json.loads(r2.content.decode())
                txt2=""
               
                for value2 in zhubo["zhubo"]:
                    data={}
                    data["address"]=value2["address"]
                    data["img"]=value2["img"]
                    data["title"]=urllib.parse.unquote(value2["title"], encoding='utf-8', errors='replace')
                    data["res"]=value["title"]
                    md5=hashlib.md5(data["address"].encode(encoding='UTF-8')).hexdigest()
                    
                    if md5 not in bl:
                        zb_list.append(data)
                        bl[md5]=""
                        txt2=txt2+urllib.parse.unquote(value2["title"], encoding='utf-8', errors='replace')+","+value2["address"]+"\r\n"
                count=count+ int(value['Number'])
                if txt2!="":
                     txt=txt+value['title']+",#genre#"+"\r\n"
                     txt=txt+txt2
                print(count);
                ##print(value['title']+"   "+str(count)+"  "+str(len(zb_list)))
            except Exception as e:
                pass
    zb_list.sort(key=takeSecond,reverse=True)
    wfile("data.json",json.dumps(zb_list))

    wfile("data.txt",txt)

    ##print(txt)

get2()
