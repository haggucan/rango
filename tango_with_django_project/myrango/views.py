#from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from myrango.models import Category,Page

def index(request):

	context = RequestContext(request)

	categories = Category.objects.order_by("-likes")[:5]

	 for category in categories:
        category.url = category.name.replace(' ', '_')
	context_variables = {"boldmessage":"HERE WILL BE BOLD",
						"categories":categories}
	return render_to_response("myrango/index.html",context_variables,context)





def category(request,category_name_url):
	context = RequestContext(request)
	category_name = category_name_url.replace("_"," ")
	context_variables = {"category_name":category_name}

	try:
		cat = Category.objects.get(name=category_name)
		pages = Pages.objects.filter(category = cat)
		context_variables["category"] = cat
		context_variables["pages"]=pages

	except:
		pass


	return render_to_response("myrango/category.html",context_variables,context)
