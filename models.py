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
    typ = models.CharField(max_length=25,choices=[('Artykuł','Artykuł'),('Starty','Starty'),('Turnieje','Turnieje'),('Składki','Składki')],default='Artykuł')
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
        elif self.typ == 'Składki':
            wynik = "<center><table><tr><td>Lp.</td><td>Imię, nazwisko</td><td>Kwota zapłacona</td><td>&nbsp;</td></tr>"
            skladki= SkladkaRoczna.objects.filter(rokId__rok=self.rok)
            licznik=0
            for sk in skladki:
                licznik +=1
                wynik += '<tr><td>{licznik}</td><td>{imieNazwisko}</td><td>{kwotaZaplacona}</td><td>{button}</td></tr>'.format(licznik=licznik,imieNazwisko=sk.osobaId.imie +" "+sk.osobaId.nazwisko,kwotaZaplacona=sk.zaplacona,button='<a href="/zaplacSkladke01">Zapłać</a>')
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


class Osoba(models.Model):
    id = models.AutoField(primary_key=True)
    imie = models.CharField(max_length=50)
    imie2 = models.CharField(max_length=50,null=True,blank=True)
    nazwisko = models.CharField(max_length=100)
    plec = models.CharField(choices=((' ',' '),('K','K'),('M','M')), max_length=1,default=' ')
    dataUrodzenia = models.DateField(null=True,blank=True)
    email1 = models.EmailField(null=True,blank=True)
    email2 = models.EmailField(null=True,blank=True)
    telefon1 = models.CharField(max_length=50,null=True,blank=True)
    telefon2 = models.CharField(max_length=50,null=True,blank=True)
    kodStawki = models.CharField(max_length=10,default='STANDARD')
    def __str__(self):
        return self.imie+' '+self.nazwisko
    
class Zawodnik(models.Model):
    osobaId = models.ForeignKey('Osoba',on_delete=models.CASCADE)
    dataOd = models.DateField(null=True,blank=True)
    dataDo = models.DateField(null=True,blank=True)
    crid = models.IntegerField(default=0)
    fideid = models.IntegerField(default=0)
    nrLicencji = models.CharField(max_length=50,null=True,blank=True)
    elo =  models.IntegerField(default=0)
    klub = models.CharField(max_length=250,null=True,blank=True)
    eloSz =  models.IntegerField(default=0)
    eloBl =  models.IntegerField(default=0)
    def __str__(self):
        return self.osobaId.nazwisko

class Czlonek(models.Model):
    osobaId = models.ForeignKey('Osoba',on_delete=models.CASCADE)
    dataOd = models.DateField(null=True,blank=True)
    dataDo = models.DateField(null=True,blank=True)
    def __str__(self):
        return self.osobaId.nazwisko

    
class Rok(models.Model):
    rok =  models.IntegerField(default=0)
    aktywnySkladki =  models.BooleanField(default=False)
    def __str__(self):
        return str(self.rok)
    
class SkladkaRoczna(models.Model):
    osobaId = models.ForeignKey('Osoba',on_delete=models.CASCADE)
    rokId = models.ForeignKey('Rok',on_delete=models.CASCADE)
    kodStawki = models.CharField(max_length=10,default='STANDARD')
    nalezna = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    zaplacona = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    def __str__(self):
        return '({}) {}: {}'.format(self.id,str(self.rokId),str(self.osobaId))

class SkladkaRocznaWyslaneTpay(models.Model):
    idSkladkaRoczna =  models.ForeignKey('SkladkaRoczna',on_delete=models.CASCADE)
    dataGodzina = models.DateTimeField(auto_now_add=True) 
    kwota = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    email = models.EmailField(null=True,blank=True)
    def __str__(self):
        return "({}) {} {}".format(self.id,self.idSkladkaRoczna,self.kwota)

class SkladkaRocznaOplata(models.Model):
    idSkladkaRoczna = models.ForeignKey('SkladkaRoczna',on_delete=models.CASCADE,null=True,blank=True)
    idSkladkaRocznaWyslaneTpay = models.ForeignKey('SkladkaRocznaWyslaneTpay',on_delete=models.CASCADE,null=True,blank=True)
    kwota = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    kanal = models.CharField(default='tpay', max_length=25)
    idKanal = models.IntegerField(null=True,blank=True)
    dataGodzina = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "({}) {} {} {} {} {}".format(self.id, self.idSkladkaRoczna,self.idSkladkaRocznaWyslaneTpay,self.kwota,self.kanal,self.idKanal)
