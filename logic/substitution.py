def subsSimple ( phrase : str , decalage : int ) :
    phrase = phrase.upper()
    chiffrement = " "
    for c in phrase :
        if "A"<= c <= "z":
            position = (ord(c)- 65 + decalage ) % 26 
            chiffrement+= chr(65+position)
        else :
            chiffrement += c
    return chiffrement 
print( subsSimple ( " rendez- vous  pour demain venez pas ,", 24  ))
