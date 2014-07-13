#include "bubble.h"
#include <stdio.h>

bubble$state$ bubble;

int main(){
	int i=0;
        bubble.vec1[0]=5;
        for(int i=0;i<100;i++){
        	bubble.vec1[i]=100-i; 
        }

        for(int i=0;i<=10;i++){
            bubble.vec1[i]=100-i;
            printf(" vec1[%d]= %d\n",i, bubble.vec1[i]  );
        }
	bubble$init$(&bubble);

	for(int i=0;i<=10;i++)
	{
        printf(" vec1[%d]= %d\n",i, bubble.vec1[i]  );
	}

	bubble$op_sort(&bubble);
        printf("Ordenado\n");
        for(int i=0;i<100;i++)
        {
	         printf(" vec1[%d]= %d\n",i, bubble.vec1[i]  );
        }

} 

