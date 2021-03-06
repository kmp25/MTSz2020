from django.contrib import admin

# Register your models here.
from .models import Artykul,Menu,ArtykulMenu,Uzytkownik, Tpay, NaszeStarty, Terminarz, Osoba, Zawodnik, Czlonek, Rok, SkladkaRoczna, SkladkaRocznaWyslaneTpay
from .models import SkladkaRocznaOplata

class ArtykulAdmin(admin.ModelAdmin):
    #list_display = ('id_tech','id_grpodm','data','wartosc','wartoscpocz','aktywny','usuniety')
    #list_filter = ('grupa','Lp')
    #prepopulated_fields = {'slug': ('title',)}
    #raw_id_fields = ('author',)
    search_fields = ('tytul','wstep','tresc', )
    date_hierarchy = 'utworzony'
    ordering = ['-id']
    

admin.site.register(Artykul,ArtykulAdmin)

class MenuAdmin(admin.ModelAdmin):
    ordering = ['-id']
admin.site.register(Menu,MenuAdmin)


class ArtykulMenuAdmin(admin.ModelAdmin):
    list_filter = ('menu',)
    ordering = ['-id']
admin.site.register(ArtykulMenu,ArtykulMenuAdmin)


class UzytkownikAdmin(admin.ModelAdmin):
    ordering = ['id']
admin.site.register(Uzytkownik,UzytkownikAdmin)

class TpayAdmin(admin.ModelAdmin):
    ordering = ['id']
admin.site.register(Tpay,TpayAdmin)

class NaszeStartyAdmin(admin.ModelAdmin):
    ordering = ['-dataOd']
admin.site.register(NaszeStarty,NaszeStartyAdmin)

class TerminarzAdmin(admin.ModelAdmin):
    ordering = ['-dataOd']
admin.site.register(Terminarz,TerminarzAdmin)

class OsobaAdmin(admin.ModelAdmin):
    ordering = ['nazwisko']
admin.site.register(Osoba,OsobaAdmin)

class ZawodnikAdmin(admin.ModelAdmin):
    ordering = ['-id']
admin.site.register(Zawodnik,ZawodnikAdmin)

class CzlonekAdmin(admin.ModelAdmin):
    ordering = ['-id']
admin.site.register(Czlonek,CzlonekAdmin)

class RokAdmin(admin.ModelAdmin):
    ordering = ['-rok']
admin.site.register(Rok,RokAdmin)

class SkladkaRocznaAdmin(admin.ModelAdmin):
    ordering = ['-id']
admin.site.register(SkladkaRoczna,SkladkaRocznaAdmin)

class SkladkaRocznaWyslaneTpayAdmin(admin.ModelAdmin):
    ordering = ['-id']
admin.site.register(SkladkaRocznaWyslaneTpay,SkladkaRocznaWyslaneTpayAdmin)

class SkladkaRocznaOplataAdmin(admin.ModelAdmin):
    ordering = ['-id']
admin.site.register(SkladkaRocznaOplata,SkladkaRocznaOplataAdmin)


