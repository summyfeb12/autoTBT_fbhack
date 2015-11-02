# Create your views here.
from django.http import HttpResponse
from core import models
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django import forms
import random
import json
import os
import pickle
import sys
import time
import urllib
import facebook
from django.contrib.staticfiles.templatetags.staticfiles import static
from models import *
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt

def index(request):
	return render_to_response('index.html')

@csrf_exempt
def login(request):
	magicalFn()
	return HttpResponse("success")