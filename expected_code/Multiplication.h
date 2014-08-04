#ifndef _Multiplication_h
#define _Multiplication_h

#include <stdint.h>
#include <stdbool.h>

typedef struct {int32_t loopnn }   Body$state$;
typedef Body$state$ * Body$ref$;
typedef struct {Body$ref$ }   Multiplication$state$;
typedef Multiplication$state$ * Multiplication$ref$;
extern void Multiplication$init$(Multiplication$ref$ self, Body$ref$ self);
extern void Multiplication$mult(Multiplication$ref$ self, int32_t mm);
#endif /* _Multiplication_h */
