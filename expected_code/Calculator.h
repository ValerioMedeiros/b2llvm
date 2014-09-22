#ifndef _Calculator_h
#define _Calculator_h

#include <stdint.h>
#include <stdbool.h>

extern void Calculator$init$();
extern void Calculator$add(int32_t numberA, int32_t numberB, int32_t* result);
extern void Calculator$mult(int32_t numberA, int32_t numberB, int32_t* result);
extern void Calculator$pow(int32_t numberA, int32_t numberB, int32_t* result);
extern void Calculator$sub(int32_t numberA, int32_t numberB, int32_t* result);
#endif /* _Calculator_h */
