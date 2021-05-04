from random import randint

def get_image_path(name):
    fileName = ''
    chars = 'xcvbnmQWERTYUI1290qwertyuiopasdfghjklzOPASDFGH345678JKLZXCVBNM'
    for c in name:
        if c not in chars:
            fileName += chars[randint(0, 8)]
        else:
            fileName += c
        fileName += chars[randint(0, 8)]
    return fileName