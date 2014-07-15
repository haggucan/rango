from django.template import RequestContext
from django.shortcuts import render_to_response



def test_index(request):

	context = RequestContext(request)
	template_context = {
	"ps_message":"This is my test rango page to test showing static file!!"

	}

	return render_to_response("test.html",template_context,context)
