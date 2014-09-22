#include <stdio.h>
struct database {
  int id_number;
  int age;
  float salary;
};


int nn[10],n[ 10 ]; /* n is an array of 10 integers */

void test0(){
  struct database employee;  /* There is now an employee variable that has
                               modifiable variables inside it.*/
  struct database newEmployee;

  employee.age = 22;
  employee.id_number = 1;
  employee.salary = 12000.21;

  newEmployee = employee;
  newEmployee.age = 5;
  printf("employee.age:%d , id_number:%d, salary:%f \n", 
	employee.age, employee.id_number, employee.salary );
  printf("newemployee.age:%d , id_number:%d, salary:%f \n", 
	newEmployee.age, newEmployee.id_number, newEmployee.salary );

}


void test1(){
	
   int i,j;
   /* initialize elements of array n to 0 */         
   for ( i = 0; i < 10; i++ )
   {
      n[ i ] = i + 100; /* set element at location i to i + 100 */
      nn[i] = 2 + i;
   }   
  
 	
}
void test2(){
   int i,j;
   /* output each array element's value */
   for (j = 0; j < 10; j++ )
   {

      printf("Element n:[%d] = %d\n", j, n[j] );

      printf("Element nn:[%d] = %d\n", j, nn[j] );
   }
 

}
int main()
{

   test0();
   test1();
   test2();
}


