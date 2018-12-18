# -*- coding: cp1252 -*-
#jython -Dpython.path=ClientInterface-2.0.4.jar cookclient.py
from com.clt.dialog.client import Client
from com.clt.script.exp import Value
#from testmodule import *
import java.lang.Object
from rezept_class import *

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
        testrec = Recipe("Bsp_quelltext.txt")
        self.recipes=[testrec]###

    def stateChanged(self, cs):
        print "new state: " + str(cs)

    def sessionStarted(self):
        print "session started"

    def reset(self):
        print "reset"

    #value has type string list (from the Value class)
    #die rezept-referenz ist ein int-Value
    # "ingredients"
    # "ingredients" rezept
    # "title"
    # "title" rezept
    # "anleitung"/"zutat"/"eigenschaft" suchbegriff
    # "anleitung"/"zutat"/"eigenschaft" suchbegriff rezept
    def output(self, value):
        value = list(value)

        if str(value[0]).strip('"')=="ingredients":
            if len(value)==1:
                self.send(self.recipes[0].ingredients())
            else:
                self.send(self.recipes[int(str(value[-1]))].ingredients())
        #elif len(value)==1:#meaning it's an url
         #   self.recipes.add(Recipe(str(value[0]).strip('"')))
        elif str(value[0]).strip('"')=="title":
            if len(value)==1:
                self.send(self.recipes[0].get_title())
            else:
                self.send(self.recipes[int(str(value[-1]))].get_title)
        elif len (value)==3:
            self.send(call(str(value[0]).strip('"'), str(value[1]).strip('"'), self.recipes[int(str(value[-1]))]))
        else:
            self.send(call(str(value[0]).strip('"'), str(value[1]).strip('"'), self.recipes[0]))
            
        print "output: " + "done"

    def getName(self):
        return "Jython demo client"

    def error(self, throwable):
        print "error"


m = Main()
m.open(8888)


