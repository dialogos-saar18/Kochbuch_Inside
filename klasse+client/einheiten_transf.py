# -*- coding: cp1252 -*-
def e_umrechnen(einheit_alt, einheit_neu, menge):
    if einheit_alt == einheit_neu:
        m = menge
    elif einheit_alt == u'g' and einheit_neu == u'kg':
        m = menge/1000.0
    elif einheit_alt == u'g' and einheit_neu == u'mg':
        m = menge * 1000.0
    elif einheit_alt == u'kg' and einheit_neu == u'g':
        m = menge * 1000.0
    elif einheit_alt == u'kg' and einheit_neu == u'mg':
        m = menge * 1000.0 * 1000.0
    elif einheit_alt == u'mg' and einheit_neu == u'g':
        m = menge / 1000.0
    elif einheit_alt == u'mg' and einheit_neu == u'kg':
        m = menge / 1000.0 / 1000.0
    elif einheit_alt == u'Liter' and einheit_neu == u'ml':
        m = menge * 1000.0
    elif einheit_alt == u'Liter' and einheit_neu == u'cl':
        m = menge * 100.0
    elif einheit_alt == u'Liter' and einheit_neu == u'dl':
        m = menge * 10.0
    elif einheit_alt == u'ml' and einheit_neu == u'Liter':
        m = menge / 1000.0
    elif einheit_alt == u'ml' and einheit_neu == u'cl':
        m = menge / 10.0
    elif einheit_alt == u'ml' and einheit_neu == u'dl':
        m = menge / 100.0
    elif einheit_alt == u'cl' and einheit_neu == u'Liter':
        m = menge / 100.0
    elif einheit_alt == u'cl' and einheit_neu == u'dl':
        m = menge / 10.0
    elif einheit_alt == u'cl' and einheit_neu == u'ml':
        m = menge * 10.0
    elif einheit_alt == u'dl' and einheit_neu == u'Liter':
        m = menge / 10.0
    elif einheit_alt == u'dl' and einheit_neu == u'cl':
        m = menge * 10.0
    elif einheit_alt == u'dl' and einheit_neu == u'ml':
        m = menge * 100.0
    else:
        print("Nicht umrechenbar")
    return m    

def e_ausschreiben(einheit):
    if einheit == u'EL, gestr.':
        e = u'EL, gestrichen'
    #elif einheit == u'EL, gehäuft':
        #pass
    elif einheit == u'TL, gestr.':
        e = u'TL, gestrichen'
    elif einheit == u'gr. Dose/n':
        e = u'große Dose/n'
    elif einheit == u'gr. Flasche(n)':
        e = u'große Flasche(n)'
    elif einheit == u'gr. Gläser':
        e = u'große Gläser'
    elif einheit == u'gr. Glas':
        e = u'großes Glas'
    elif einheit == u'gr. Kopf':
        e = u'großer Kopf'
    elif einheit == u'gr. Scheiben':
        e = u'große Scheiben'
    elif einheit == u'm.-große':
        e = u'mittelgroße'
    elif einheit == u'm.-großer':
        e = u'mittelgroßer'
    elif einheit == u'm.-großes':
        e = u'mittelgroßes'
    elif einheit == u'Msp.':
        e = u'Messerspitze'
    elif einheit == u'n. B.':
        e = u'nach Belieben'
    elif einheit == u'Pck.':
        e = u'Päckchen'
    elif einheit == u'Pkt.':
        e = u'Päckchen'
    else:
        e = einheit
    return e
    
