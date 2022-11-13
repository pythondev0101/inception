"""
    Functions
"""



def generate_number(prefix, lID):
    generated_number = ""
    
    if 1 <= lID < 9:
        generated_number = prefix +"0000000" + str(lID+1)
    elif 9 <= lID < 99:
        generated_number = prefix + "000000" + str(lID+1)
    elif 999 <= lID < 9999:
        generated_number = prefix + "00000" + str(lID+1)
    elif 9999 <= lID < 99999:
        generated_number = prefix + "0000" + str(lID+1)
    elif 99999 <= lID < 999999:
        generated_number = prefix + "000" + str(lID+1)
    elif 999999 <= lID < 9999999:
        generated_number = prefix + "00" + str(lID+1)
    elif 9999999 <= lID < 99999999:
        generated_number = prefix + "0" + str(lID+1)
    else:
        generated_number = prefix + str(lID+1)

    return generated_number
