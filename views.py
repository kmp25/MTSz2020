from django.shortcuts import render,redirect

from django.http import HttpResponse # na potrzeby tpay
from django.utils.html import escape # na potrzeby tpay

# Create your views here.

from .models import Artykul,Menu
from www.models import ArtykulMenu, Tpay, BrakStrony, NaszeStarty


def menuGorne():
    return {'Menu1': Menu.objects.filter(rodzic__isnull=True, aktywny=True).order_by('kolejnosc'),'Menu2': Menu.objects.filter(rodzic__isnull=False,aktywny=True).order_by('kolejnosc')}

def artykul(widok,pid):
    if widok=='NaszeStarty':
        if ArtykulMenu.objects.filter(menu__id=pid,widok = 'Starty'):
            return naszeStarty()
        else:
            return {'NaszeStarty':None}
    else:
        return {widok: Artykul.objects.filter(artykulmenu__menu__id=pid,artykulmenu__widok=widok).order_by('artykulmenu__kolejnosc','-artykulmenu__id')}

def naszeStarty():
        return {'NaszeStarty':NaszeStarty.objects.filter(dataOd__range=["2020-01-01", "2020-12-31"]).order_by('dataOd')}

def artykul1(widok,pid):
    return {widok: Artykul.objects.filter(artykulmenu__menu__id=pid,artykulmenu__widok=widok).order_by('artykulmenu__kolejnosc','-artykulmenu__id')}

# Create your views here.
def kategoria(request):
    #return render(request,
                  #'www/index.html',
                  #{**menuGorne(),**{'Artykuly': Artykul.objects.filter(artykulmenu__menu__id=1)}})
    pid=Menu.objects.filter(jid=121)[0].id
    return pokazMenu(request,pid)
    
    
def pokazMenu(request,pid):
    return render(request,
                  'www/index.html',
                  {**menuGorne(),**artykul('Pelny',pid),**artykul('Skrocony',pid),**artykul('Link',pid),**artykul('NaszeStarty',pid)})
    
def pokazArtykul(request,pid):
    return render(request,
                  'www/index.html',
                  {**menuGorne(),**{'Pelny': Artykul.objects.filter(id=pid)}})
     


def tpay(request):
    if request.method == 'GET':
      qd = request.GET
    elif request.method == 'POST':
     qd = request.POST
     
    #return HttpResponse(escape(repr(qd)))
    
    req1 = Tpay(req = str(dict(qd)))
    req1.save()
    
    return HttpResponse(str(dict(qd)))
#def pokazMenu(request,pid):
#    return render(request,
#                  'www/index.html',
#                  {'Menu1': Menu.objects.filter(rodzic__isnull=True).order_by('kolejnosc'),'Menu2': Menu.objects.filter(rodzic__isnull=False).order_by('kolejnosc')})
    

def pliki(request,sciezka):
    return redirect('http://test.mtsz.org.pl/static/www/'+sciezka)


def brakStrony(request,sciezka):
    bs = BrakStrony(sciezka=sciezka)
    bs.save()
    return kategoria(request)