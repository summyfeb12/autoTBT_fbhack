# Create your views here.
from django.http import HttpResponse
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
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt



def index(request):
    return render_to_response('index.html')

@csrf_exempt
def login(request):
    print request
    magicalFn(request)
    return HttpResponse("success")


ID = 'me'
SAFE_CHARS = '-_() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def save(res, name='data'):
    """Save data to a file"""
    with open('%s.lst' % name, 'w') as f:
        pickle.dump(res, f)
    
def read(name='data'):
    """Read data from a file"""
    with open('%s.lst' % name, 'r') as f:
        res = pickle.load(f)
    return res

def fetch(limit=1000, depth=10, last=None, id=ID, token=""):
    """Fetch the data using Facebook's Graph API"""
    lst = []
    print token
    graph = facebook.GraphAPI(token)
    print graph
    url = '%s/photos/uploaded' % id
    
    if not last:
        args = {'fields': ['source','name'], 'limit': limit}
        res = graph.request('%s/photos/uploaded' % id, args)
        process(lst, res['data'])
    else:
        res = {'paging': {'next': last}}
    
    # continue fetching till all photos are found
    for _ in xrange(depth):
        if 'paging' not in res:
            break
        try:
            url = res['paging']['next']
            res = json.loads(urllib.urlopen(url).read())
            process(lst, res['data'])
        except:
            break
    
    save(url, 'last_url')
    print lst
    return lst

def process(res, dat):
    """Extract required data from a row"""
    err = []
    for d in dat:
        if 'source' not in d:
            err.append(d)
            continue
        src = d['source']
        if 'name' in d:
            name = ''.join(c for c in d['name'][:99] if c in SAFE_CHARS) + src[-4:]
        else:
            name = src[src.rfind('/')+1:]
        res.append({'name': name, 'src': src})
    if err:
        print '%d errors.' % len(err)
        print err
    #print '%d photos found.' % len(dat)

def download(res):
    """Download the list of files"""
    start = time.clock()
    if not os.path.isdir(ID):
        os.mkdir(ID)
    os.chdir(ID)
    print "HERE"
    print res
    print len(res)
    p = random.choice(res)
    # try to get a higher resolution of the photo
    p['src'] = p['src'].replace('_s', '_n')
    k,message = urllib.urlretrieve(p['src'], p['name'])
    return k
    
def post(k, a_token):
    graph = facebook.GraphAPI(a_token)
    photo = open(""+str(k))
    graph.put_photo(photo, message="#AutoTBT")
    photo.close()

def magicalFn(request):
    # download 500 photos, fetch details about 100 at a time
    print request.body
    a_token = request.body.split("=")[1]
    print "a_token is "
    lst = fetch(token=a_token,limit=100, depth=5)
    save(lst, 'photos')
    post(download(lst), a_token)

# @csrf_exempt
# def login(request):
# 	magicalFn()
# 	return HttpResponse("success")
