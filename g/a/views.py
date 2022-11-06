from django.shortcuts import render
import os
import pathlib
import re
from collections import Counter
from a.utils import show_wordcloud
import copy
import operator

# Create your views here.
from django.http import HttpResponse
from django.template import loader


def index(req):
    default_file = "../../hamlet.txt";
    file = default_file;
    
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
                with open(file_with_path, "r") as fp:
                    for line in fp:
                        # print(dict)
                        dict.update(Counter(re.split(r'\s*[\s,\.?!-:;\[\]]\s*', line)).items())
                wordcloud = show_wordcloud(copy.deepcopy(dict))
                dict = sorted(dict.items(), key=operator.itemgetter(1),reverse=True)
            else:
                errorText=f"no access to file {file}!"
        else:
            errorText=f"file {file} not found"
        
    
    view_model = {
	'a_list': dict,
    'file':file,
    'errorText': errorText,
    'wordcloud': wordcloud
    }
    return render(req, 'index.html', view_model)