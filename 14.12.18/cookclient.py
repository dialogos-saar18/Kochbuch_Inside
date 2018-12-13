# -*- coding: cp1252 -*-
from com.clt.dialog.client import Client
from com.clt.script.exp import Value
#from testmodule import *
import java.lang.Object
from classmodule import *

testrec= Recipe("Testrezept",
                ["tu dies zuerst", "tu das als zweites", "tu jenes zum schluss"],
                {'zucker': {'menge': 200, 'einheit': "g"},
                 'milch':{'menge': 125, 'einheit': "ml"}},
                {'zubereitungszeit': '30 min', 'schwierigkeit': 'einfach'})

def call(category, term, recipe):
    #ruft die Methoden auf, die die Informationen auslesen
    if category == "anleitung":#works but should be expanded
        return(recipe.get_schritt(term)) # term one of {"next","repeat","all","previous"}
    elif category == "zutaten":#works
        return(recipe.get_zutat(term)) 
    elif category == "eigenschaft":#works
        return(recipe.get_property(term))
    else:#works
        print("Fehler in call; Kategorie " + category + " ist ungültig")
        return ("ungültig")
        ##raise Error! 


class Main(Client):
    def __init__(self):
        self.recipes=[testrec]###

    def stateChanged(self, cs):
        print "new state: " + str(cs)

    def sessionStarted(self):
        print "session started"

    def reset(self):
        print "reset"

    #value has type string list; it can have two or three elements which are the args of get_info
        #or one or two elements which then "ingredients" and optionally the recipe number
        #we can also tell the Client to get a recipe; elements of value is an url
    def output(self, value):
        value = list(value)
        if str(value[0]).strip('"')=="ingredients":
            if len(value)==1:
                self.send(self.recipes[0].ingredients())
            else:
                self.send(self.recipes[int(str(value[-1]))])
        #elif len(value)==1:#meaning it's an url
         #   self.recipes.add(Recipe(str(value[0]).strip('"')))
        elif len (value)==3:#works
            self.send(call(str(value[0]).strip('"'), str(value[1]).strip('"'), self.recipes[int(str(value[-1]))]))
        else:#works
            self.send(call(str(value[0]).strip('"'), str(value[1]).strip('"'), self.recipes[0]))
        print "output: " + "done"

    def getName(self):
        return "Jython demo client"

    def error(self, throwable):
        print "error"


m = Main()
m.open(8888)


