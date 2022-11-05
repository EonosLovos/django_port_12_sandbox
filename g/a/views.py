from django.shortcuts import render
import os
import pathlib

# Create your views here.
from django.http import HttpResponse
from django.template import loader


def index(req):
    default_file = "/../hamlet.txt";
    file = default_file;
    if req.method =='POST':
        data = req.POST
        post_filepath = data.get("post_filepath")
        if(post_filepath.strip() != ""):
            file = post_filepath
    errorText = ""        
    p = pathlib.Path(file)
    if p.exists():
        file_with_path = p.resolve()
        if os.access(file_with_path, os.R_OK):
            open(file_with_path, "r")#.write(my_data)
        else:
            errorText=f"no access to file {file}!"
    else:
        errorText=f"file {file} not found"
        
        
    dict = []

    view_model = {
	'a_list': dict,
    'file':file,
    'errorText': errorText
    }
    return render(req, 'index.html', view_model)