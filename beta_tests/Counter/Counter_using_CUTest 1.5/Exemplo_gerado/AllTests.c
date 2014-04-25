#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include "CuTest.h"
#include "counter.h"

counter$state$ counter;

void check_invariant(CuTest* tc, counter$state$ counter) {
	
	if(!((!((counter.error == true)) || (counter.value == INT32_MAX)))){
		CuFail(tc, "The invariant '((error = TRUE) => (value = MAXINT))' was unsatisfied");
	}
	
	if(!(0 <= counter.value)){
		CuFail(tc, "The invariant '0 <= value' was unsatisfied");
	}
	
	if(!(counter.value <= INT32_MAX)){
		CuFail(tc, "The invariant 'value <= MAXINT' was unsatisfied");
	}
	
}
		 

/**
* Test Case 1
* Formula: value <= MAXINT & 0 <= value & value < MAXINT & error : BOOL & value : INT & ((error = TRUE) => (value = MAXINT))
*/
void counter_inc_test_case_1(CuTest* tc)
{
	//counter$INITIALISATION(&counter);
	
	bool error = false; 
	counter.error = error; 
	int32_t value = 0; 
	counter.value = value; 
	
	
	counter$inc(&counter);
	
	 
	bool errorExpected; // Add expected value here.
	CuAssertTrue(tc, counter.error == false);
	
	int32_t valueExpected; // Add expected value here.
	CuAssertTrue(tc, counter.value == 1);
	 
	check_invariant(tc, counter);
}
		 
/**
* Test Case 2
* Formula: value <= MAXINT & 0 <= value & not(value < MAXINT) & error : BOOL & value : INT & ((error = TRUE) => (value = MAXINT))
*/
void counter_inc_test_case_2(CuTest* tc)
{
	//counter$INITIALISATION(&counter);
	
	bool error = true; 
	counter.error = error; 
	int32_t value = INT32_MAX; 
	counter.value = value; 
	
	
	counter$inc(&counter);
	
	 
	bool errorExpected; // Add expected value here.
	CuAssertTrue(tc, counter.error == true);
	
	int32_t valueExpected; // Add expected value here.
	CuAssertTrue(tc, counter.value == INT32_MAX);
	 
	check_invariant(tc, counter);
}
		 
/**
* Test Suite
* Machine: counter
* Operation: inc
*
* Partition Strategy: Equivalence Classes
* Combination Strategy: All-Combinations
* Oracle Strategy: Exception, State Variables, Return Values, State Invariant
*/
CuSuite* counter_inc_test_suite(void)
{
	CuSuite* suite = CuSuiteNew();
	
	SUITE_ADD_TEST(suite, counter_inc_test_case_1);
	SUITE_ADD_TEST(suite, counter_inc_test_case_2);
	
	return suite;
}

void RunAllTests(void) {
    CuString *output = CuStringNew();
    CuSuite* suite = CuSuiteNew();
    
    CuSuiteAddSuite(suite, counter_inc_test_suite());
    
    CuSuiteRun(suite);
    CuSuiteSummary(suite, output);
    CuSuiteDetails(suite, output);
    printf("%s\n", output->buffer);
}

int main(void) {
    RunAllTests();
}

