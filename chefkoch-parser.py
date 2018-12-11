#https://stackoverflow.com/questions/5041008/how-to-find-elements-by-class
from bs4 import BeautifulSoup as bs

def get_recipe_information(file):
    with open(file) as f:
        soup = bs(f)
        steps = get_steps(soup)
        preparation = get_preparation_info(soup)
        incredients = get_incredients(soup)
        portionen = get_portionen(soup)

        print(steps)
        print(preparation)
        print(incredients)
        print(portionen)



def get_steps(beautifuls):
    schritte = {}
    zubereitung = beautifuls.find(id="rezept-zubereitung")
    i = 1
    for string in zubereitung.stripped_strings:
        schritte[i] = string
        i = i + 1
    return schritte


def get_preparation_info(beautifuls):
    preparation = {}
    prep = beautifuls.find(id="preparation-info")
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
                    n = n.strip()
                    val = val + n
                    
            preparation[key] = val
        i = i + 1
    return preparation
    

def get_incredients(beautifuls):
    zutaten = {}
    incr = beautifuls.find("table", {"class": "incredients"})
    stripped2 = incr.stripped_strings
    strings = incr.strings
    l = []

    angaben_m = []
    angaben_z = []
    for i in incr.contents:
        if str(type(i)) == "<class 'bs4.element.NavigableString'>":
            pass
        else:
            li = i.findAll("td")
            menge = li[0].contents
            mengen_angabe= menge[0]

            mengen_angabe = mengen_angabe.strip()
            angaben_m.append(mengen_angabe)
                
            zutat = li[1].contents
            if len(zutat) == 1:
                zutat_angabe = zutat[0]
            else:
                zutat_angabe = zutat[1].contents[0]
            angaben_z.append(zutat_angabe.strip())

    i = 0
    while i < len(angaben_m):
        m = angaben_m[i]
        z = angaben_z[i]
        if m == u'':
            zutaten[z] = (0,u'')
        else:
            m = m.replace(u'\xa0', u' ')
            spl = m.split()
            zahl = spl[0]
            if len(spl) == 2:
                einheit = m.split()[1]
            else:
                einheit = u''
            zutaten[z] = (zahl, einheit)
        i = i+1
    return zutaten

def get_portionen(beautifuls):
    p = beautifuls.find("input", {"name": "portionen"})
    p = p[u'value']
    return p
    
    

get_recipe_information("Bsp_quelltext.txt")

