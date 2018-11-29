import urllib2

def suchanfrage(frage):
    l = frage.split(' ')
    s = "https://www.chefkoch.de/rs/s0/"
    s = s + l[0]
    i = 1
    while i < len(l):
        s = s + l[i]
        i = i + 1
    s = s + "+" + "/Rezepte.html"
    quell = urllib2.urlopen(s)
    html = quell.read()
    with open("testquelle.txt", "w") as f:
        f.write(html)
    return None 





