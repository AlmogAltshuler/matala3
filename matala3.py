# -*- coding: utf-8 -*-
"""
Created on Thu May  6 10:23:12 2021

@author: almog
"""
  
import json

#Whatsapp text
WhatsApp_Path="C:/Users/almog/Desktop/PythonMatalot/matala3/files/whatsapp.txt"
WhatsApp_text = open(WhatsApp_Path,"r",encoding= "utf-8")

#Creat the message dictionary
def messages_dict(chats_line,i,people): 
    text=chats_line[15:].split(":")
    in_list="Null"
    try:
        line = dict()
        line["datetime"]=chats_line[:15]
        if text[0] in people:
            line["id"]=people.index(text[0])+1
        else:
            in_list=text[0]
            line["id"]=i
        
        line["text"]=text[1]
    except:
        line=False
    result=[line,in_list]    
    return result

#Creat the metadata dictionary
def metadata_dict(line,WhatsApp_text): 
    meta = dict()
    meta["chat_name"]=line.split('"')[1]
    meta["creation_date"]=line[:15]
    meta["num_of_participants"]=0
    creator_phone=line.find("נוצרה על ידי")+len("נוצרה על ידי")
    meta["creator"]=line[creator_phone:]
    return meta

messages_metadata_dict=dict()
messages = []
contacts = []
index=1
last_datetime=" "#checking for lines that has no date in them whitch mean its from the person in the row before
for line in WhatsApp_text: 
    this_line=messages_dict(line,index,contacts)
    if this_line[0]!=False: #normal message
        messages.append(this_line[0])
        last_datetime= this_line[0]["datetime"]
        if this_line[1]!="Null":
            index+=1
            contacts.append(this_line[1])
    if "נוצרה על ידי" in line: #group creation message
        metadata=metadata_dict(line,WhatsApp_text)
    if last_datetime[:5] not in line: #if we have a line with no date so add the text to the row before
        messages[len(messages)-1]["text"]=messages[len(messages)-1]["text"]+" "+line
        
#create the full dictionary
metadata["num_of_participants"]=len(contacts)
messages_metadata_dict["messages"]= messages 
messages_metadata_dict["metadata"]= metadata      
print(messages_metadata_dict)

#Create a file with the data
file_name=messages_metadata_dict["metadata"]["chat_name"]+".txt"
f = open(file_name,"w",encoding="utf8")
info = json.dump(messages_metadata_dict,f,ensure_ascii=False,indent=6)
f.close()
f=open(file_name, "r",encoding="utf8")
print(json.load(f))
f.close()