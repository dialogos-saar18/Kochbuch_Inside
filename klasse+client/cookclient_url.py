# -*- coding: cp1252 -*-
#jython -Dpython.path=ClientInterface-2.0.4.jar cookclient_url.py
from com.clt.dialog.client import Client
from com.clt.script.exp import Value
#from testmodule import *
import java.lang.Object
from rezept_class_url import *

from java.awt import BorderLayout, Color
from javax.swing import JPanel, JFrame, JTextArea, JButton, BoxLayout, Box, JTextField
from javax.swing import JLabel
from javax.swing import ImageIcon
from java.awt import Color
from java.awt import Dimension
from java.lang import Class


def call(category, term, recipe):
    #ruft die Methoden auf, die die Informationen auslesen
    if category == "anleitung":#works but should be expanded
        return(recipe.get_schritt(term)) # term one of {"first","next","repeat","all","previous"}
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
        #pass
        recipe = Recipe('https://www.chefkoch.de/rezepte/785281181805506/Spinat-Cannelloni-al-Forno.html')
        self.recipes=[recipe]
    

    def stateChanged(self, cs):
        print "new state: " + str(cs)

    def sessionStarted(self):
        print "session started"

    def reset(self):
        print "reset"

    #value has type string list (from the Value class)
    #die rezept-referenz ist ein int-Value
    # "URL"
    # "ingredients"
    # "ingredients" rezept
    # "title"
    # "title" rezept
    # "einkaufszettel"
    # "einkaufszettel" rezept
    # "anleitung"/"zutat"/"eigenschaft" suchbegriff
    # "anleitung"/"zutat"/"eigenschaft" suchbegriff rezept
    # "portionen" "wert"
    # "exists_zutat" suchbegriff
    def output(self, value):
        value = list(value)

        #Quelltext für Rezept abfragen
        if str(value[0]).strip('"') == "URL":
            self.gui()
            #recipe = Recipe('https://www.chefkoch.de/rezepte/785281181805506/Spinat-Cannelloni-al-Forno.html')
            #self.recipes=[recipe]
            print("created recipe")            
                    
        elif str(value[0]).strip('"')=="ingredients":
            if len(value)==1:
                self.send(self.recipes[0].ingredients())
            else:
                self.send(self.recipes[int(str(value[-1]))].ingredients())
        elif str(value[0]).strip('"')=="einheiten":
            if len(value)==1:
                self.send(self.recipes[0].einheiten())
            else:
                self.send(self.recipes[int(str(value[-1]))].einheiten())
        elif str(value[0]).strip('"')=="titel":
            if len(value)==1:
                self.send(self.recipes[0].get_title())
            else:
                self.send(self.recipes[int(str(value[-1]))].get_title())

        #kompletten Einkaufszettel schreiben
        elif str(value[0]).strip('"')=="einkaufszettel":
            if len(value)==1:
                self.send(self.recipes[0].einkaufszettel("all"))
            else:
                self.send(self.recipes[int(str(value[-1]))].einkaufszettel())

        #einzelne Zutat auf Einkaufszettel
        elif str(value[0]).strip('"')=="Zettel":
            self.recipes[0].einkaufszettel(str(value[1]).strip('"'))


        elif str(value[0]).strip('"')=="exists_zutat":
            #if len(value)==1:
            
            self.send(self.recipes[0].contains(str(value[1]).strip('"')))
            #else:
             #   self.send(self.recipes[int(str(value[-1]))].einkaufszettel())
        elif str(value[0]).strip('"')=="zutaten":
            self.send(self.recipes[0].get_zutat(str(value[1]).strip('"')))
        elif str(value[0]).strip('"')=="portionen":
            #if len(value)==1:
            if str(value[1]).strip('"')== "wert":
                self.send(str(self.recipes[0].get_portions()))
            #else:
                #self.send(self.recipes[int(str(value[-1]))].einkaufszettel())

        #fürs umrechnen nach Personen
        elif str(value[0]).strip('"')=="Personen":
            self.send(self.recipes[0].umrechnen(str(value[1]).strip('"'),u'Personen'))
        #fürs umrechnen nach Zutaten
        elif str(value[0]).strip('"')=="Zutaten":
            z = str(value[1]).strip('"')
            m = str(value[2]).strip('"')
            e = str(value[3]).strip('"')
            self.send(self.recipes[0].umrechnen([m,e],z))

        elif len(value)==3:
            self.send(call(str(value[0]).strip('"'), str(value[1]).strip('"'), self.recipes[int(str(value[-1]))]))
        else:
            self.send(call(str(value[0]).strip('"'), str(value[1]).strip('"'), self.recipes[0]))
            
        print "output: " + "done"

    def getName(self):
        return "Jython demo client"

    def error(self, throwable):
        print "error"


    def gui(self):#returns URL in unicode
        frame = JFrame('URL eingeben',
                defaultCloseOperation = JFrame.EXIT_ON_CLOSE,
                size = (480,200),
                       )
        frame.setLayout(None)
        
        def testact(event):
            print("hi")
            frame.setVisible(False)
            url = field.getText()
            #recipe = Recipe(url)
            #self.recipes=[recipe]
            self.send("continue")

         
        fieldlabel = JLabel()
        fieldlabel.setText("<html><font size=+1>Geben Sie die Internetadresse des Rezepts ein</font></html>")
        fieldlabel.setBounds(20,20,500,40)
        frame.add(fieldlabel)

        field = JTextField()
        field.setText("https://www.chefkoch.de/rezepte/...")
        field.setBounds(20,60,411,40)
        frame.add(field)
        
        button = JButton("Los!",actionPerformed=testact)
        button.setBounds(155,100,150,30)
        frame.add(button)
        
        frame.setVisible(True)


m = Main()
m.open(8880)


