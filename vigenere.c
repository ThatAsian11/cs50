// Enciphers text using Vigenere's Cipher
// Usage: ./vigenere k

#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int main(int argc,string argv[])
{
    // Making sure a key is given
    if (argc == 2)
    {  
        string k = argv[1];
    
      // Checking if keyword is valid 
    for (int i = 0; i < strlen(k); i++)
      {
          if (!isalpha(k[i]))
          {
              printf("Error, invalid keyword\n");
              exit(1);
          }
      }
     
        string t = get_string("plaintext: ");
        printf("ciphertext: ");
       
      // Ciphering and outputing text  
    for (int i = 0, j = 0; i < strlen(t); i++)
     {
            
               // Checking whether value is an alphabet
                if (isalpha(t[i]))     
                {    
                    // Checking whether alphabet is uppercase
                    if (isupper(t[i])) 
                    {
                        printf("%c", ((t[i] - 65) + (toupper(k[j]) - 65)) % 26 + 65);
                    } 
                    // Checking whether alphabet is lowercase
                    else if (islower(t[i]))
                    { 
                        printf("%c", ((t[i] - 97) + (toupper(k[j]) - 65)) % 26 + 97);
                    }
                     
                    j = (j + 1) % strlen(k);
                }    
                else
                {
                    printf("%c",t[i]);
                }
     }
    }
    else 
    {
     printf("Error, please enter a keyword\n");
     return 1;
    }
    printf("\n");
}