from django.shortcuts import render
import os, io
import pathlib
import re
from email.message import EmailMessage

import smtplib, ssl
import pandas as pd

# Create your views here.
from django.http import HttpResponse
from django.template import loader

class smtpLibStrDebug(smtplib.SMTP_SSL):
    log = ""
    def print_to_string(self, *args, **kwargs):
        output = io.StringIO()
        print(*args, file=output, **kwargs)
        contents = output.getvalue()
        output.close()
        return contents
    
    def _print_debug(self, *args):
        self.log += self.print_to_string(*args)
        #print("~~~~~~"+self.log+"!!!!!!!!!")
        super()._print_debug(*args)
    


    
def index_howtonamesame(req):
    config={
        "colParticipated": "D",
        "colEventName" : "C",
        "colNameSurname" : "B",
        "regex_FindEventName" : r"/{{\s*[eE]vent\s*[nN]ame}}/",
        # /*TODO: make this work when a person has 3 names. do not think yagni..*/
        "regex_FindNameSurname" : r'\s*(\S+)\s+(\S+)(\s+\S+)?\s*',
        "regex_ReplaceNameSurname" : r'\2.\1@cayonara.id.lv'
    }
    
    inputFileType = 'Xlsx'
    inputFileName = '../../roundcubemail-1.6.0/file example.xlsx'
    templateFileName = '../../template.txt'
    searchNoPunny  = ['Ā', 'ā', 'Č', 'č', 'Ē', 'ē', 'Ģ', 'ģ', 'Ī', 'ī', 'Ķ', 'ķ', 'Ļ', 'ļ', 'Ņ', 'ņ', 'Ō', 'ō', 'Ŗ', 'ŗ', 'Š', 'š', 'Ū', 'ū', 'Ž', 'ž' ]
    replaceNoPunny = ['A', 'a', 'C', 'c', 'E', 'e', 'G', 'g', 'I', 'i', 'K', 'k', 'L', 'l', 'N', 'n', 'O', 'o', 'R', 'r', 'S', 's', 'U', 'u', 'Z', 'z' ]
    
    whomtosend_bcc = "";

    errorText = ""
    
    if req.method =='POST':
        data = req.POST
        post_whomtosend_bcc = data.get("post_whomtosend_bcc")
        if(post_whomtosend_bcc.strip() != ""):
            whomtosend_bcc = post_whomtosend_bcc
            
        ex_path = pathlib.Path(inputFileName)
        templ_path = pathlib.Path(templateFileName)
        print("ac")
        if (ex_path.exists() and templ_path.exists()):
            print("dc")
            ex_where = pd.read_excel(ex_path.resolve(), usecols=[3])
            rnums = [x+1 for x in ex_where[ex_where[ex_where.columns.ravel()[0]] != 1].index]
            ex_result = pd.read_excel(ex_path.resolve(), skiprows=rnums)
            
            
            text_file = open(templ_path.resolve(), "r")
            #read whole file to a string
            template = text_file.read()
            #close file
            text_file.close()
            
            from_address = "noreply@cayonara.id.lv"
            password = "a"
            print("ss")
            context = ssl.create_default_context()
            with smtpLibStrDebug("cayonara.id.lv", 465, context=context) as server:
                server.login(from_address, password)
                
                server.set_debuglevel(1)
                rvl = ex_result.columns.ravel()
                col_a = rvl[0]
                col_b = rvl[1]
                col_c = rvl[2]
                #col_d = rvl[3]
                #col_e = rvl[4]
                for i in ex_result.index:
                    try:
                        email="zanete.darkale@cayonara.id.lv"
                        msg = EmailMessage()
                        msg.set_content(template.replace("{{Event Name}}", ex_result[col_c][i]))
                        #template.format_map({"{Event Name}": "GOGOGOGOO"})
                        msg['Subject'] = 'Hi from ' + ex_result[col_c][i]
                        to = re.sub(config["regex_FindNameSurname"], config["regex_ReplaceNameSurname"],  ex_result[col_b][i])
                        punny_dic = {}
                        for i in range(len(searchNoPunny)):
                            punny_dic[searchNoPunny[i]] = replaceNoPunny[i]
                        for c in punny_dic.keys():
                            to = to.replace(c, punny_dic[c])
                        msg['To'] = to
                        if(whomtosend_bcc!=""):
                            msg['Bcc'] = whomtosend_bcc
                            #"zanete.darkale@gmail.com"
                        msg['From'] = from_address
                        server.send_message(msg)
                
                
                         #   TODO PASS OBJECT TO TEMPLATE SO THAT IT CAN FORMAT IT AS TEMPLATES DO>..
                        errorText += "\n\n"+"Sending to "+email+"\n"  
                        errorText += server.log
                        #from email.message import EmailMessage
                    except Exception as e:
                        errorText += "\n\n"+"error Sending to "+email+"\n"  
                        errorText += server.log + "\n"
                        errorText += str(e)
                
                
                server.quit()
            

    view_model = {
    'post_whomtosend_bcc':whomtosend_bcc,
    'errorText': errorText
    }
    return render(req, 'index_howtonamesame.html', view_model)