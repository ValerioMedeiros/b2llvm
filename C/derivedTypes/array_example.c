#include <stdio.h> 
	//int arr[99];
        struct tstruct { int arr[99];int arr3[2][2][4] ; int anyVar1; int anyVar2;  } ref;
	const int start_arr =1  ;
	int array[3][3][4] = {[0 ... 2][0 ... 2][0 ... 3] = 5};
void set();
void get();	

int main (){
	set();

	printf("%d",ref.arr[4]);
}

void set(){
	int ind = 7;
	int tmp = 4 - start_arr;
	ref.arr[tmp]=5;

	// initialising 
//	ref.arr={[0 ... 98] = 5};
//	ref.arr = array;

}

void get(){
	int a= ref.arr[4];
}
