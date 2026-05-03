import unicodedata

def sanitize(input : str)->str : #virer les accents
    normalized = unicodedata.normalize('NFD', input) #remplace é par e'
    result = "".join(char for char in normalized if unicodedata.category(char) != 'Mn')
    final_list_char = []
    for char in result:
        if char.isalpha() or char.isspace():
            final_list_char.append(char.upper())
    return "".join(final_list_char)

def sanitize_2(input : str)->str :
    normalized = unicodedata.normalize('NFD', input)
    result = "".join(char for char in normalized if unicodedata.category(char) != 'Mn')
    final_list_char = []
    for char in result:
        if char.isalpha() or char.isspace():
            final_list_char.append(char.lower())
    return "".join(final_list_char)

