import re
import orodja
import os

def zajemi_rezultate():
    '''Zajame podatke iz spletne strani'''
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
    '''Izbriše datoteke neobstoječih dirk'''
    for datoteka in orodja.datoteke('rezultati/'):
        if 'Results for this race are not available' in orodja.vsebina_datoteke(datoteka):
            os.remove(datoteka)


regex_rezultati = re.compile(
    r'<option value="/results.php\?s=80&y=(?P<Leto>\d{4})&c=0" selected>.*?'
    r'<option value="/results.php\?s=80&y=\d{4}&r=\d{8}&c=2" selected>(?P<Dirka>.*?)</option>.*?'
    r'<td align="center">1</td><td align="left"><a target="_blank" href="http://forix.autosport.com/forix.php\?series=80&driver=\d{10}">(?P<Zmagovalec>.*?)</a></td><td align="left">(?P<Mostvo_zmagovalca>.*?)</td>.*?'
    r'<td align="center">2</td><td align="left"><a target="_blank" href="http://forix.autosport.com/forix.php\?series=80&driver=\d{10}">(?P<Drugi>.*?)</a></td><td align="left">(?P<Mostvo_drugega>.*?)</td>.*?'
    r'<td align="center">3</td><td align="left"><a target="_blank" href="http://forix.autosport.com/forix.php\?series=80&driver=\d{10}">(?P<Tretji>.*?)</a></td><td align="left">(?P<Mostvo_tretjega>.*?)</td>.*?',
    flags=re.DOTALL
)


regex_skupno = re.compile(
    r'<option value="/results.php\?s=80&y=(?P<Leto>\d{4})&c=1" selected>.*?'
    r'<td align="center">1</td><td align="left"><a target="_blank" href="http://forix.autosport.com/forix.php\?series=80&driver=\d{10}">(?P<Prvak>.*?)</a></td><td align="right">.*'
    r'<td align="center">2</td><td align="left"><a target="_blank" href="http://forix.autosport.com/forix.php\?series=80&driver=\d{10}">(?P<Podprvak>.*?)</a></td><td align="right">.*'
    r'<tr bgcolor="#FFFFFF"><td align="center">1</td><td align="left">(?P<Prvi_proizvajalec>.*?)</td><td align="right">.*'
    r'<tr bgcolor="#FFFFFF"><td align="center">2</td><td align="left">(?P<Drugi_proizvajalec>.*?)</td><td align="right">.*',
    flags=re.DOTALL
)


def izloci_rezultate(imenik, regex):
    '''Vrne seznam s slovarji podatkov iz imenika'''
    podatki = []
    for datoteka in orodja.datoteke(imenik):
        for podatek in re.finditer(regex, orodja.vsebina_datoteke(datoteka)):
            pod = podatek.groupdict()
            pod['Leto'] = int(pod['Leto'])
            podatki.append(pod)
    return podatki



#zajemi_rezultate()
#izbrisi_neobstojece()

rezultati_dirk = izloci_rezultate('rezultati/', regex_rezultati)
skupni_rezultati = izloci_rezultate('skupni_rezultati/', regex_skupno)

orodja.zapisi_tabelo(rezultati_dirk, ['Leto', 'Dirka', 'Zmagovalec', 'Mostvo_zmagovalca', 'Drugi', 'Mostvo_drugega', 'Tretji', 'Mostvo_tretjega'], 'csv-datoteke/rezultati_dirk.csv')
orodja.zapisi_tabelo(skupni_rezultati, ['Leto', 'Prvak', 'Podprvak', 'Prvi_proizvajalec', 'Drugi_proizvajalec'], 'csv-datoteke/skupni_rezultati.csv')
