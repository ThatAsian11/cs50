#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int main(int argc,string argv[])
{
    //making sure a key is given
    if (argc == 2)
{    
        int k = atoi(argv[1]);
        printf("plaintext:");
        string t = get_string();
        printf("ciphertext:");
        
        for ( int i = 0; i < strlen(t); i++)
        {
            //checking whether value is an alphabet
        if (isalpha(t[i]))    
        {    
            //checking whether alphabet is uppercase
            if (isupper(t[i])) 
            {
                printf("%c",(char) ((t[i] - 65) + k) % 26 + 65);
            } 
            //checking whether alphabet is lowercase
             else if (islower(t[i]))
            { 
                printf("%c",(char) ((t[i] - 97) + k) % 26 + 97);
            }
        }    
            else
            {
            printf("%c",t[i]);
            }
           
        }
    
}
    
    else 
    {
        printf("Error, please enter a key\n");
        return 1;  
    }
             printf("\n");
}