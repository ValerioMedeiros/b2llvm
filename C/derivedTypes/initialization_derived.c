#include <stdio.h>


void test1(){
 int a= 10;

 printf("%d",a); 

}


int main(){
  struct R_4{ int arr[10] ;} Rstate;

	Rstate.arr[1]=10;
	printf("%d", Rstate.arr[1]);
	
	test1();

}


