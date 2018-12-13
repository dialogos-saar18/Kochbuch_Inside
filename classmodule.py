
    

class Recipe:
    def __init__(self, _titel, _anleitung, _zutaten, _eigenschaften):
        self.titel = _titel
        self.anleitung=_anleitung
        self.schritt = 0
        self.zutaten= _zutaten
        #eigenschaften: dict; available keys:
        #zubereitungszeit ebenfalls evtl. in Größe und Einheit unterteilen
            #-> an den jeweiligen Nutzer anpassen
        self.eigenschaften=_eigenschaften

    def get_schritt(self, argument): #returns string
        #if argument == "all":
        if argument == "next":
            #try:
            self.schritt += 1
            return "Dein nächster Schritt lautet: " + self.anleitung[self.schritt]
            #Index Error -> "Du musst nichts mehr tun."
        elif argument == "repeat":
            return "Ich wiederhole: " + self.anleitung[self.schritt]
        elif argument == "previous":
            #IndexError
            self.schritt -= 1
            return "Der letzte Schritt war: " + self.anleitung[self.schritt]
        elif argument == "all":
            r=""
            for i in range(len(self.anleitung)):
                r += str(i+1) + ". " + self.anleitung[i]
        else:
            print ("Unerwartetes Argument "+argument+" in get_schritt")
            ###raise Error

    def get_zutat(self,bezeichnung): #returns string
        #if bezeichnung == "all"
        return str(self.zutaten[bezeichnung]['menge']) + self.zutaten[bezeichnung]['einheit']

    def get_property(self,key): #returns string
        return self.eigenschaften[key]

    def umrechnen():
        pass

    def ingredients():
        return self.zutaten.keys()

'''
class Nutzer:
    def __init__(self, name):
        load_user(name)
        self.handicap #wie viel länger oder kürzer braucht der nutzer (in Prozent)
'''
