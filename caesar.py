# Enciphers given text using Caesar's cipher
from cs50 import get_string
import sys


while True:
        key = int(sys.argv[1])
        if key > 0:
            break
ptext = get_string("Plaintext: ")
print ("ciphertext: ", end="")
    
for i in ptext:
 
    # Character is uppercase
    if i.isupper():
        print (chr((ord(i) - ord('A') + key) % 26 + ord('A')), end="")

    # Character is lowercase
    elif i.islower():
        print (chr((ord(i) - ord('a') + key) % 26 + ord('a')), end="")
 
    else:
        print(i, end="")
            
print()
    

                
            
    
    
    
    

