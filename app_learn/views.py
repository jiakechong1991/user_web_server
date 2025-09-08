from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404

from django.template import loader
from .models import TQuestion
# Create your views here.

def index(request):
    # return HttpResponse("hello world! app learn")
    latest_question_list = TQuestion.objects.order_by("-pub_date")[:5]
    template = loader.get_template("app_learn/index.html")
    context = {"latest_question_list": latest_question_list}
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    # try:
    #     question = TQuestion.objects.get(pk=question_id)
    # except TQuestion.DoesNotExist:
    #     raise Http404("Question does not exist")
    ### 上面的代码是常用操作，所以django提供了快捷方法
    question = get_object_or_404(TQuestion, pk=question_id)
    
    return render(request, "app_learn/detail.html", {"question": question})