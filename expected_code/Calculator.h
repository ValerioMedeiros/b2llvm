#ifndef _Calculator_h
#define _Calculator_h

#include <stdint.h>
#include <stdbool.h>

typedef struct { }   Calculator$state$;
typedef Calculator$state$ * Calculator$ref$;
extern void Calculator$init$(Calculator$ref$ self);
extern void Calculator$add(Calculator$ref$ self, int32_t numberA, int32_t numberB, int32_t* result);
extern void Calculator$mult(Calculator$ref$ self, int32_t numberA, int32_t numberB, int32_t* result);
extern void Calculator$pow(Calculator$ref$ self, int32_t numberA, int32_t numberB, int32_t* result);
extern void Calculator$sub(Calculator$ref$ self, int32_t numberA, int32_t numberB, int32_t* result);
#endif /* _Calculator_h */
