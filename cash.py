# Returns the number of coins used to provide change
from cs50 import get_float

given_amount = 0
cent_amount = 0
quarter_count = 0
dime_count = 0
nickel_count = 0
leftover = 0
coin_count = 0

# Prompts user for amount of change owed
while True:
    given_amount = get_float("Change owed: ")
    
    if given_amount >= 0:
        break
    
# Calculates number of coins needed to provide change     
cent_amount = round(given_amount*100, 1)
 
quarter_count = cent_amount // 25
leftover = cent_amount % 25
 
dime_count = leftover // 10 
leftover = leftover % 10
 
nickel_count = leftover // 5
leftover = leftover % 5
 
coin_count = quarter_count + dime_count + nickel_count + leftover;
 
print(coin_count)

    