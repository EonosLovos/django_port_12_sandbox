from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader


def index(req):
    the_list=[
	{
	'name': 'aname',
	'id': 111
	},
	{
	'name': 'bname',
	'id': 222
	}
    ]
    templ = loader.get_template('index.html')
    view_model = {
	'a_list': the_list
    }
    return HttpResponse(templ.render(view_model, req))