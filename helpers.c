/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    if (value < 0)
    return false;
    else
    {
        int start = 0;
    int end = n-1; 
    while (end >= start)
    {
        
        int middle = (start + end) / 2;
        if (values[middle] == value)
        return true;
        else if( values[middle] > value)
        end = middle - 1;
        else 
        start = middle + 1;
        
    }
    }
    
    return false;
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    bool check;
    
    do {
        check = false;
        for (int i = 0; i < n - 1; i++)
        {
            if (values[i] > values[i + 1])
            {
                int counter = values[i];
                values[i] = values[i + 1];
                values[i + 1] = counter;
                
             check = true;
                
            }
            
        }
        
    } while(check);
    return;;
}

