from django.db import models
from django.conf import settings

from django.db.models import Q

# Create your models here.

class NaszeStarty(models.Model):
    nazwa = models.TextField()
    link = models.TextField()
    miejscowosc = models.CharField(max_length=255)
    dataOd = models.DateField()
    dataDo = models.DateField()
    zawodnikow = models.IntegerField(null=True,blank=True)
    druzyn = models.IntegerField(null=True,blank=True)
    miejsca = models.TextField()
    def __str__(self):
        return self.nazwa

class Terminarz(models.Model):
    nazwa = models.TextField()
    link = models.TextField()
    dataOd = models.DateField()
    dataDo = models.DateField()
    rund =  models.IntegerField()
    tempo = models.CharField(max_length=50)
    def __str__(self):
        return self.nazwa


class Artykul(models.Model):
    id = models.AutoField(primary_key=True)
    tytul = models.CharField(max_length=255)
    typ = models.CharField(max_length=25,choices=[('Artykuł','Artykuł'),('Starty','Starty'),('Turnieje','Turnieje')],default='Artykuł')
    rok = models.IntegerField(default=0)
    wstep = models.TextField(null=True,blank=True)
    tresc = models.TextField()
    jid = models.IntegerField(default=-1)
    cjid = models.IntegerField(default=-1)
    utworzony = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    zaktualizowany = models.DateTimeField(auto_now=True,null=True,blank=True)
    autor = models.ForeignKey('Uzytkownik',null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.tytul+" (" + str(self.utworzony)[:10]+")"
    def getTytul(self):
        return self.tytul
    def getWstep(self):
        return self.wstep
    def getTresc(self):
        if self.typ == 'Artykuł':
            wynik = self.tresc
        elif self.typ == 'Starty':
            wynik = "<center><table><tr><td>Lp.</td><td>Nazwa turnieju</td><td>Wyniki</td></tr>"
            starty= NaszeStarty.objects.filter(Q(dataOd__year=self.rok) | Q(dataDo__year=self.rok))
            licznik=0
            for s in starty:
                licznik +=1
                wynik += '<tr><td>{licznik}</td><td><a href="{href}" target="_new">{nazwa}</a><BR/>{miejscowosc}, {dataOd}-{dataDo}<BR/>{zaw} {dru}</td><td>{miejsca}</td></tr>'.format(licznik=licznik,href=s.link,nazwa=s.nazwa,miejscowosc=s.miejscowosc,dataOd=s.dataOd.strftime("%d.%m.%Y"),dataDo=s.dataDo.strftime("%d.%m.%Y"),zaw="Startowało {z} zawodników.".format(z=s.zawodnikow) if s.zawodnikow else "",dru="Startowało {dr} drużyn.".format(dr=s.druzyn) if s.druzyn else "",miejsca=s.miejsca)
            wynik += "</table></center>"
        elif self.typ == 'Turnieje':
            wynik = "<center><table><tr><td>Lp.</td><td>Termin</td><td>Nazwa</td><td>Rund</td><td>Termin</td></tr>"
            terminarz= Terminarz.objects.filter(Q(dataOd__year=self.rok) | Q(dataDo__year=self.rok))
            licznik=0
            for t in terminarz:
                licznik +=1
                wynik += '<tr><td>{licznik}</td><td>{dataOd}-{dataDo}</td><td><a href="{href}" target="_new">{nazwa}</a></td><td>{rund}</td><td>{tempo}</td></tr>'.format(licznik=licznik,dataOd=t.dataOd.strftime("%d.%m"),dataDo=t.dataDo.strftime("%d.%m"),href=t.link,nazwa=t.nazwa,rund=t.rund,tempo=t.tempo)
            wynik += "</table></center>"
        return wynik
        

    
class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    kolejnosc = models.IntegerField(default=0)
    nazwa = models.CharField(max_length=50)
    rodzic = models.ForeignKey('Menu',null=True,blank=True,on_delete=models.CASCADE)
    aktywny = models.BooleanField(default=1)
    jid = models.IntegerField(default=-1)
    parent_jid = models.IntegerField(default=-1)
    def __str__(self):
        return (str(self.rodzic)+"\\" if self.rodzic else "") + self.nazwa
    
class ArtykulMenu(models.Model):
    id = models.AutoField(primary_key=True)
    artykul = models.ForeignKey('Artykul',on_delete=models.CASCADE)
    menu = models.ForeignKey('Menu',on_delete=models.CASCADE)
    widok = models.CharField(choices=(('Pelny','Pełny'),('Skrocony','Skrócony'),('Link','Link'),('Starty','Starty')),default='Pelny',max_length=10)
    kolejnosc = models.IntegerField(default=0)
    def __str__(self):
        return (str(self.artykul)+" ___  " + str(self.menu)+' __ '+str(self.widok))
    
class Uzytkownik(models.Model):
    id = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    
class Tpay(models.Model):
    req = models.TextField()

class BrakStrony(models.Model):
    sciezka = models.TextField()    
      