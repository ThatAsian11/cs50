#include <stdio.h>
#include <cs50.h>

int main(void)
{
    printf("Minutes: ");
    int n;
    do
      {  
        n = get_int();
    }
    while (n < 0);
    
    printf("Bottles: %i\n", n * 12);
}

