#include <stdio.h>
#include "Rec.h"

/* Clause CONCRETE_CONSTANTS */
/* Basic constants */

/* Array and record constants */
/* Clause CONCRETE_VARIABLES */

static struct R_1 { int32_t number;int32_t balance; double dd; } Rec__account;
void Rec__set(void);
void Rec__unsafe_dec(void);
void Rec__get_and_set(void);
typedef struct point point;
/* Declare the struct with integer members x, y */
struct point {
   int    x;
   int    y;
};

int main (){
    
    Rec__set();
    printf("%d\n",Rec__account.balance);
    Rec__get_and_set();
    printf("%d\n",Rec__account.balance);
    Rec__INITIALISATION();
    printf("%lf\n",Rec__account.dd);
}
/* Clause INITIALISATION */
void Rec__INITIALISATION(void)
{
    point p = {.y = 2, .x = 1};
    point pi;// = {700,900};
    pi.y=700;
    pi.x=900;
    Rec__account.number = 0;
    Rec__account.balance = 10;
    Rec__account.dd=7;

}

/* Clause OPERATIONS */

void Rec__positive(bool *res)
{
    if((Rec__account.balance) > (0))
    {
        (*res) = true;
    }
    else
    {
        (*res) = false;
    }
}

void Rec__withrdaw(int32_t amt)
{
    if((((amt) >= (0)) &&
        ((amt) <= (2147483647))) &&
    (((Rec__account.balance) >= (amt))))
    {
        Rec__account.number = Rec__account.number;
        Rec__account.balance = (Rec__account.balance-amt);
    }
}
void Rec__set(void)
{
    Rec__account.balance = 50;
}
void Rec__get_and_set(void)
{
    Rec__account.balance = Rec__account.balance + 50;
}

void Rec__unsafe_dec(void)
{
    Rec__account.balance = Rec__account.balance-1;
}

