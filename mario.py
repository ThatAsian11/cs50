# Makes a half pyramid like in Mario
from cs50 import get_int

# Prompts user for height of pyramid
while True:
    height = get_int("Height: ")
    if height >= 0 and height <= 23:
            break
    
# Constructs pyramid   
for i in range(height):
    print(" " * (height - 1 - i), end="")
    
    print("#" * ( i + 2), end="")
    
    print()