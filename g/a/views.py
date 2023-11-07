from django.shortcuts import render
import os
import pathlib
import re
from collections import Counter
from a.utils import show_wordcloud
import copy
import operator
import glob
# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.utils.encoding import smart_str

def index(req):
    default_file = "../../hamlet.txt"
    default_file = "hamlet.txt"
    file = default_file
    
    errorText = ""
    dict = Counter()
    wordcloud = None
    
    if req.method =='POST':
        data = req.POST
        post_filepath = data.get("post_filepath")
        if(post_filepath.strip() != ""):
            file = post_filepath

        p = pathlib.Path(file)
        if p.exists():
            file_with_path = p.resolve()
            if os.access(file_with_path, os.R_OK):
                with open(file_with_path, "r", encoding="utf-8") as fp:
                    for line in fp:
                        # print(dict)
                        #on what to split? space, comma, ? etc could be split token
                        parts = re.split(r'''\s*[\s,\.?!'-:;'\[\]"']+\s*''', line)
                        cnt = 0
                        #sadly this advances the cursor over what should be deleted.
                        #for i in parts: 
                        while(True):
                            if(len(parts[cnt]) <2 or not re.fullmatch('''[^\s]+''', parts[cnt])):
                                parts.pop(cnt)
                            else:
                                cnt=cnt+1
                            if(cnt==len(parts)):
                                break
                        dict.update(Counter(parts).items())
                #for word, cnt in dict: #immutable!!!!111
                for word in list(dict.keys()):
                    if(len(word)<2): 
                        del dict[word]
                dict = sorted(dict.items(), key=operator.itemgetter(1),reverse=True)
                wordcloud = show_wordcloud(dict)
            else:
                errorText=f"no access to file {file}!"
        else:
            errorText=f"file {file} not found"
    elif req.method =='GET':
        errorText = errorText + "\n files: \n"
        for file in glob.glob('*.txt'):
            errorText = errorText + file+"\n"

        
    
    view_model = {
	'a_list': dict,
    'file':file,
    'errorText': errorText,
    'wordcloud': wordcloud
    }
    return render(req, 'index.html', view_model)

def view_text(r, file_name):
   file_path = 'filez/' + file_name
   #response = HttpResponse(open(file_path, 'rb').read(), content_type='application/force-download')
#   response = HttpResponse(open(file_path, 'rb').read(), content_type='text/plain')
   #response = HttpResponse(open(file_path, 'rb').read(), content_type='text/html; charset=utf-8')
   
#response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
#   return response
   view_model = {
   'fl': open(file_path, 'r', encoding='utf-8').read(),
   }
   return render(r, 't.html', view_model)