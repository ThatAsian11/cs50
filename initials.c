#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
 
int main(void)

//printing the first initial
{
string s = get_string();
   printf("%c",toupper (s[0]));
   
//printing the next initials after checking for spaces 
  for (int i = 0; i < strlen(s); i++)
  {
      if (s[i] == ' ')
      {
          printf("%c",toupper (s[i+1]));
      }
          
  }
  printf("\n");

}