#include "stdio.h"
#include "Array.h"

/* Clause CONCRETE_CONSTANTS */
/* Basic constants */

/* Array and record constants */
/* Clause CONCRETE_VARIABLES */

static int32_t Array2[10][20][30];
static int32_t Array__arr[100];
static int32_t Array__arr_n[100][100];
static int32_t Array__tmp[100];

void Array__setZero(void);
void Array__setZero2(void);
void Array__setZeroSimp(void);
void Array__setArray(void);

int main(void){
   Array__setZero();
   Array__setZero2();
   printf("%d\n", Array2[2][3][4]);
  return 0;
}

/* Clause INITIALISATION */
void Array__INITIALISATION(void)
{
    Array__arr[1] = 100;
    Array__arr_n[0][0] = 10;
    memmove(Array__tmp,Array__arr,100 * sizeof(int32_t));
    Array__setZero();

}

/* Clause OPERATIONS */
void Array__setZero(void)
{   int32_t x=2; int32_t y=3 ; int32_t z=4 ;
    Array2[x][y][z]=7;
}

void Array__setZero2(void)
{
    int x =4;
    x= x-2;
    Array2[x][3][4]=7;
}
void Array__setArray(void)
{
    int32_t cprogram[3][2][4]={
        {{0, 022, 03, 43}, {23, 47, -9, 2}},
        {{0, 36, 45, 4}, {12, 24, 022, -1}},
        {{8, 32, 342, 01}, {21, 32, 43, -20}}
    };
    int32_t Array3[1][2][1]= {{{4},{5}}};
    /*{ { {1}, {2} , {3}},
        
              { {4}, {5} , {6}},
              { {7}, {8} , {9}}
             } ;*/
}
void Array__setZeroSuggestedByDavid(void)
{  /* David gives a similar sugestion wit intermediate steps */   

	Array__arr_n[2][5]=4;
    	printf("%d\n",Array__arr_n[2][5]);     
	int * mid = Array__arr_n[2];
	printf("%d\n",mid[5]);
}




void Array__set(int32_t ix, int32_t tt)
{
    if(((((ix) >= (0)) &&
            ((ix) <= (99))) &&
        ((tt) >= (0))) &&
    ((tt) <= (1000)))
    {
        Array__arr[ix] = tt;
    }
}

void Array__read(int32_t ix, int32_t *tt)
{
    if(((ix) >= (0)) &&
    ((ix) <= (99)))
    {
        (*tt) = Array__arr[ix];
    }
    else
    {
        (*tt) = 0;
    }
}

void Array__swap(int32_t ix, int32_t jx)
{
    if(((((ix) >= (0)) &&
            ((ix) <= (99))) &&
        ((jx) >= (0))) &&
    ((jx) <= (99)))
    {
        {
            int32_t temp;
            
            temp = Array__arr[jx];
            Array__arr[jx] = Array__arr[ix];
            Array__arr[ix] = temp;
        }
    }
}

