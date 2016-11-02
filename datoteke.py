import re
import orodja
import os

def zajemi_rezultate():
    osnova = 'http://classic.autosport.com/results.php'
    parametri = 's=80'
    for leto in range(1949, 2017):
        naslov = '{}?{}&y={}&c=1'.format(osnova, parametri, leto)
        ime_datoteke = 'skupni_rezultati/{}.html'.format(leto)
        orodja.shrani(naslov, ime_datoteke)
        for dirka in range(1, 19):
            naslov2 = '{}?{}&y={}&r={}80{:02}&c=2'.format(osnova, parametri, leto, leto, dirka)
            ime = 'rezultati/{}-{:02}.html'.format(leto, dirka)
            orodja.shrani(naslov2, ime)


def izbrisi_neobstojece():
    for datoteka in orodja.datoteke('rezultati/'):
        if 'Results for this race are not available' in orodja.vsebina_datoteke(datoteka):
            os.remove(datoteka)


