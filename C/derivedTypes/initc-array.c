#include "bubble.h"
#include <stdio.h>

array$state$ array;

int main(){
	int i=0;
        array.vec1[0]=5;
        for(int i=0;i<100;i++){
        	array.vec1[i]=100-i;
        }

        for(int i=0;i<=10;i++){
            array.vec1[i]=100-i;
            printf(" vec1[%d]= %d\n",i, array.vec1[i]  );
        }
	array$init$(&array);



} 

