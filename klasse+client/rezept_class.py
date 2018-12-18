# -*- coding:cp1252 -*-
from bs4 import BeautifulSoup as bs
import re

class Recipe:
    
    def __init__(self, _quellcode):
        with open(_quellcode) as f:
            soup = bs(f,features="html.parser")
        self.titel = self.init_titel(soup)
        self.anleitung = self.init_anleitung(soup)
        self.schritt = 0
        self.zutaten = self.init_zutaten(soup)
        self.portionen = self.init_portionen(soup)
        #eigenschaften: dict; available keys:
        #zubereitungszeit ebenfalls evtl. in Gr��e und Einheit unterteilen
            #-> an den jeweiligen Nutzer anpassen
        self.eigenschaften = self.init_properties(soup)

    def get_schritt(self, argument): #returns string
        #if argument == "all":
        if argument == u'next':
            #try:
            self.schritt += 1
            return u'Dein n�chster Schritt lautet: ' + self.anleitung[self.schritt]
            #Index Error -> "Du musst nichts mehr tun."
        elif argument == u'repeat':
            return u'Ich wiederhole: ' + self.anleitung[self.schritt]
        elif argument == u'previous':
            #IndexError
            self.schritt -= 1
            return u'Der letzte Schritt war: ' + self.anleitung[self.schritt]
        elif argument == u'all':
            r = u''
            for i in range(len(self.anleitung)):
                r += str(i+1) + u'. ' + self.anleitung[i]
            return r
        else:
            print (u'Unerwartetes Argument '+str(argument)+u' in get_schritt')
            ###raise Error


    def einkaufszettel(self):
        datei = "Einkaufszettel_" + self.titel + ".txt"
        with open(datei, "w") as f:
            for z in self.zutaten:
                m = self.zutaten[z][u'menge']
                if m == 0:
                    m = u''
                else:
                    m = str(m)
                e = self.zutaten[z][u'einheit']
                s = m + u' ' + e
                f.write(s.encode('utf8'))
                f.write("\t")
                f.write(z.encode('utf8'))
                f.write("\n")


    def get_zutat(self,bezeichnung): #returns string
        if bezeichnung == "all":
            s = u''
            for z in self.zutaten:
                m = self.zutaten[z][u'menge']
                if m == 0:
                    m = u''
                else:
                    m = str(m)
                e = self.zutaten[z][u'einheit']
                s = s + u' ' + m + u' ' + e + u' ' + z + u' '
            return s
            
        try:
            me = self.zutaten[bezeichnung][u'menge']
            if me == 0:
                me = u''
            else:
                me = str(me)
            ei = self.zutaten[bezeichnung][u'einheit']
            return me + u' ' + ei + u' ' + bezeichnung
        except:
            l = []
            for i in self.zutaten:
                if re.search(bezeichnung, i):
                    me = self.zutaten[i][u'menge']
                    ei = self.zutaten[i][u'einheit']
                    l.append(me)
                    l.append(ei)
                    l.append(i)
            try:
                if l[0] == 0:
                    l0 = u''
                else:
                    l0 = str(l[0])
                s = l0 + u' ' + l[1] + u' ' + l[2]
                i = 3
                while i < len(l):
                    print(i)
                    if i%3 == 0:
                        s = s + u' und'
                    if l[i] == 0:
                        li = u''
                    else:
                        li = str(l[i])
                    s = s + u' ' + li
                    i = i + 1
                return s
                    
            except:
                return u'Zutat wird nicht ben�tigt'

    def get_property(self,key): #returns string
        return self.eigenschaften[key]

    def ingredients(self):
        return self.zutaten.keys()


    # no return value, only changes incredients
    # Einheiten umrechnen?
    # angabe => entweder Personen oder eine Zutat
    def umrechnen(self, anzahl, angabe):
        if angabe == u'Personen':
            factor = anzahl / self.portionen
        else:
            factor = anzahl / self.zutaten[angabe][u'menge']
        for d in self.zutaten:
            d[u'menge'] = d[u'menge'] * factor

    # gibt True zur�ck, wenn die Zutat f�r das Rezept ben�tigt wird
    # Problem: mehrere Sorten der gleichen Zutat
    def contains(self, zutat):
        if zutat in self.zutaten.keys():
            return u'Ja'
        else:
            for i in self.zutaten.keys():
                if re.search(zutat, i):
                    return u'Du brauchst ' + i
            return u'Nein'

    def init_titel(self, beautifuls):
        t = beautifuls.find(u'title')
        t = t.contents[0]
        return t[:-14]

    # returns liste: [u'Die Zwiebeln fein...', u'Das Tomatenmark...',...]
    def init_anleitung(self, beautifuls):
        schritte = []
        zubereitung = beautifuls.find(id=u'rezept-zubereitung')
        for string in zubereitung.stripped_strings:
            schritte.append(string)
        return schritte

    # return dict: {u'Zwiebel(n)': {u'menge': 1, u'einheit': u'm.-gro\xdfe'}, u'Zucker':...}
    def init_zutaten(self, beautifuls):
        zutaten = {}
        incr = beautifuls.find(u'table', {u'class': u'incredients'})
        stripped2 = incr.stripped_strings
        strings = incr.strings
        l = []
        angaben_m = []
        angaben_z = []
        for i in incr.contents:
            if str(type(i)) == "<class 'bs4.element.NavigableString'>":
                pass
            else:
                li = i.findAll(u'td')
                menge = li[0].contents
                mengen_angabe= menge[0]
                mengen_angabe = mengen_angabe.strip()
                mengen_angabe = mengen_angabe.replace(u'\xa0', u' ')
                mengen_angabe = mengen_angabe.strip()
                angaben_m.append(mengen_angabe)
                    
                zutat = li[1].contents
                if len(zutat) == 1:
                    zutat_angabe = zutat[0]
                else:
                    zutat_angabe = zutat[1].contents[0]
                angaben_z.append(zutat_angabe.strip().lower())
        i = 0
        while i < len(angaben_m):
            m = angaben_m[i]
            z = angaben_z[i]
            te = [m]
            d = {}
            if m == u'':
                d[u'menge'] = 0
                d[u'einheit'] = u''
            else:
                spl = m.split()
                zahl = spl[0]
                if len(spl) == 2:
                    einheit = m.split()[1]
                else:
                    einheit = u''
                try:
                    d[u'menge'] = int(zahl)
                    d[u'einheit'] = einheit
                except:
                    d[u'menge'] = 0
                    d[u'einheit'] = zahl
            zutaten[z] = d
            i = i+1
        return zutaten

    # returns int
    def init_portionen(self, beautifuls):
        p = beautifuls.find(u'input', {u'name': u'portionen'})
        p = p[u'value']
        return int(p)

    #returns dict: {u'schwierigkeitsgrad': u'simpel', ...}
    def init_properties(self, beautifuls):
        preparation = {}
        prep = beautifuls.find(id=u'preparation-info')
        l = []
        stripped = prep.stripped_strings
        i = 0
        for s in stripped:
            if i % 2 == 0:
                key = s
            else:
                val = u''
                for n in s:
                    if n == u'/':
                        break
                    else:
                        val = val + n
                val = val.strip()
                if key == u'Arbeitszeit:' or key == u'Ruhezeit:' or key == u'Koch-/Backzeit:':
                    d = {}
                    val = val[4:]
                    lis = val.split(" ")
                    if len(lis) == 4:
                        k = int(lis[0]) * 24 + int(lis[2])
                        v = lis[3]
                    else:
                        k = int(lis[0])
                        v = lis[1]
                    d[u'dauer'] = k
                    d[u'einheit'] = v
                    val = d
                                    
                preparation[key] = val
            i = i + 1
        ges = 0
        einheiten = []
        try:
            aze = preparation[u'Arbeitszeit:'][u'einheit']
            inheiten.append(aze)
        except:
            pass
        try:
            rze = preparation[u'Ruhezeit:'][u'einheit']
            einheiten.append(rze)
        except:
            pass
        try:
            kze = preparation[u'Koch-/Backzeit:'][u'einheit']
            einheiten.append(kze)
        except:
            pass
        umr = False
        for e in einheiten:
            if e != u'Min.':
                umr = True
        if u'Arbeitszeit:' in preparation:
            zeit = preparation[u'Arbeitszeit:'][u'dauer']
            if umr:
                if aze == u'Std.':
                    zeit = zeit * 60
            ges = ges + zeit
        if u'Ruhezeit:' in preparation:
            zeit = preparation[u'Ruhezeit:'][u'dauer']
            if umr:
                if rze == u'Std.':
                    zeit = zeit * 60
            ges = ges + zeit
        if u'Koch-/Backzeit:' in preparation:
            zeit = preparation[u'Koch-/Backzeit:'][u'dauer']
            if umr:
                if kze == u'Std.':
                    zeit = zeit * 60
            ges = ges + zeit  
        di = {}
        e = u'Min.'
        if ges > 300:
            ges = float(ges) / 60
            e = u'Std.'
        di[u'dauer'] = ges
        di[u'einheit'] = e
        preparation[u'Gesamtzeit'] = di
        return preparation

    #def einheiten_ausschreiben(self, einheit):
        
                                             
rezept = Recipe("Bsp_quelltext.txt")
#rezept2 = Recipe("quelltext_stollen.txt")

'''
class Nutzer:
    def __init__(self, name):
        load_user(name)
        self.handicap #wie viel l�nger oder k�rzer braucht der nutzer (in Prozent)
'''