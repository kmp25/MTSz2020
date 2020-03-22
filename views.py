from django.shortcuts import render,redirect

from django.http import HttpResponse,HttpRequest  # na potrzeby tpay
from django.utils.html import escape # na potrzeby tpay

# Create your views here.
from .models import Artykul,Menu
from www.forms import skladka01
from www.models import ArtykulMenu, BrakStrony, NaszeStarty, SkladkaRoczna, SkladkaRocznaWyslaneTpay, SkladkaRocznaOplata, Osoba
from tpay import views as tpayViews



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
    
    
#def pokazMenu1(request,pid):
#    return render(request,
#                  'www/index.html',
#                  {**menuGorne(),**artykul('Pelny',pid),**artykul('Skrocony',pid),**artykul('Link',pid),**artykul('NaszeStarty',pid), 'pid': pid if not Menu.objects.get(id=pid).rodzic else Menu.objects.get(id=pid).rodzic.id})


def pokazMenu(request,pid):
    return render(request,
                  'www/index.html',
                  {**menuGorne(), 'ArtykulMenu': ArtykulMenu.objects.filter(menu__id=pid).order_by('kolejnosc','-id'), 'pid': pid if not Menu.objects.get(id=pid).rodzic else Menu.objects.get(id=pid).rodzic.id})


def pokazArtykul(request,pid):
    return render(request,
                  'www/index.html',
                  {**menuGorne(),**{'Pelny': Artykul.objects.filter(id=pid)}})
     
def zaplacSkladke01(request):
    if request.method == 'POST':
        forma = skladka01(request.POST)
        if forma.is_valid():
            skladkaRocznaWyslaneTpay = SkladkaRocznaWyslaneTpay()
            skladkaRocznaWyslaneTpay.idSkladkaRoczna = SkladkaRoczna.objects.get(id=forma.cleaned_data['idSkladkaRoczna'])
            skladkaRocznaWyslaneTpay.kwota = forma.cleaned_data['kwota']
            skladkaRocznaWyslaneTpay.email = forma.cleaned_data['email']
            skladkaRocznaWyslaneTpay.nazwisko = forma.cleaned_data['nazwisko']
            skladkaRocznaWyslaneTpay.save()
            adres = 'http://'+HttpRequest.get_host(request)+'/a/1553'
            return tpayViews.tpay01(request,'SKLADKA',skladkaRocznaWyslaneTpay.id,skladkaRocznaWyslaneTpay.kwota,'Składka roczna ({}) - {} {}'.format(skladkaRocznaWyslaneTpay.idSkladkaRoczna.rokId.rok,skladkaRocznaWyslaneTpay.idSkladkaRoczna.osobaId.imie,skladkaRocznaWyslaneTpay.idSkladkaRoczna.osobaId.nazwisko),skladkaRocznaWyslaneTpay.email,skladkaRocznaWyslaneTpay.nazwisko,adres,adres)
    else:
        sk = request.GET['sk']
        #skladkaRoczna = SkladkaRoczna.objects.all()[0]
        skladkaRoczna = SkladkaRoczna.objects.get(id=sk)
        forma = skladka01(initial={'idSkladkaRoczna' :  skladkaRoczna.id} )
        return render(request,
                    'www/zaplacSkladke.html',
                    {**menuGorne(),'SkladkaRoczna':skladkaRoczna, 'forma':forma}
    )    

def zaplacSkladke02(id_SkladkaRocznaWyslaneTpay,kwota,kanal,idKanal):
    if kanal == 'tpay':
        skladkaRocznaWyslaneTpay = SkladkaRocznaWyslaneTpay.objects.get(id = id_SkladkaRocznaWyslaneTpay)
        skladkaRoczna = skladkaRocznaWyslaneTpay.idSkladkaRoczna
    skladkaRocznaOplata = SkladkaRocznaOplata(idSkladkaRoczna = skladkaRoczna, idSkladkaRocznaWyslaneTpay = skladkaRocznaWyslaneTpay,   kwota = kwota,kanal = kanal, idKanal = idKanal)
    print("skladkaRocznaOplata:",skladkaRocznaOplata)
    skladkaRocznaOplata.save()
    skladkaRoczna = skladkaRocznaOplata.idSkladkaRoczna
    skladkaRoczna.zaplacona += kwota
    skladkaRoczna.save()

def pliki(request,sciezka):
    return redirect('http://test.mtsz.org.pl/static/www/'+sciezka)

def brakStrony(request,sciezka):
    bs = BrakStrony(sciezka=sciezka)
    bs.save()
    return kategoria(request)