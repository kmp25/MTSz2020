from django.db import models
from django.conf import settings

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
    
class Artykul(models.Model):
    id = models.AutoField(primary_key=True)
    tytul = models.CharField(max_length=255)
    wstep = models.TextField(null=True,blank=True)
    tresc = models.TextField()
    jid = models.IntegerField(default=-1)
    cjid = models.IntegerField(default=-1)
    utworzony = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    zaktualizowany = models.DateTimeField(auto_now=True,null=True,blank=True)
    autor = models.ForeignKey('Uzytkownik',null=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.tytul+" (" + str(self.utworzony)[:10]+")"
    
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
      