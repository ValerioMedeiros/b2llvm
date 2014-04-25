#include "CuTest.h"
#include <stdio.h>
#include <string.h>
#include "Counter.h"

    
    CuSuite* StrUtilGetSuite();
    
    counter$state$ counter;


  void Test_oper_inc_testCase1(CuTest *tc) {
	    // setting manually
	counter.value = 0 ;
	counter.error = false;
	    // or setting using the initialization, you can chose one option
	counter$INITIALISATION(&counter);
	    // calling the function
	counter$inc(&counter);
    
	bool condition = !( counter.error == true) || (counter.value == 2147483647);
	CuAssert_Line(tc, __FILE__, __LINE__ , "Invariant invalid", condition);

    }


    void Test_oper_inc_testCase2(CuTest *tc) {
	    // setting manually
	counter.value = 3 ;
	counter.error = true;
    	
	// calling the function
	counter$inc(&counter);
    	
	// Neste caso, o invariante está sendo quebrado então a formula não deveria ser negada ?
	bool condition =  !( counter.error == true) || (counter.value == 2147483647) ;
	CuAssert_Line(tc, __FILE__, __LINE__ , "Invariant invalid", condition);

    }


    void Test_oper_zero_testCase1(CuTest *tc) {
	    // setting manually
	counter.value = 3 ;
	counter.error = true;
    	
	// calling the function
	counter$zero(&counter);
    
	bool condition = !( counter.error == true) || (counter.value == 2147483647);
	CuAssert_Line(tc, __FILE__, __LINE__ , "Invariant invalid", condition);

    }

   
    CuSuite* testsSuite() {
        CuSuite* suite = CuSuiteNew();
	SUITE_ADD_TEST(suite, Test_oper_inc_testCase1);
        SUITE_ADD_TEST(suite, Test_oper_inc_testCase2);
	SUITE_ADD_TEST(suite, Test_oper_zero_testCase1);

        return suite;
    }

    
    void RunAllTests(void) {
        CuString *output = CuStringNew();
        CuSuite* suite = CuSuiteNew();
        
        CuSuiteAddSuite(suite, testsSuite());
    
        CuSuiteRun(suite);
        CuSuiteSummary(suite, output);
        CuSuiteDetails(suite, output);
        printf("%s\n", output->buffer);
    }
    
    int main(void) {
        RunAllTests();
    }
