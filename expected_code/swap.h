#ifndef _swap_h
#define _swap_h

#include <stdint.h>
#include <stdbool.h>

typedef struct {int32_t v1; int32_t v2; }   swap$state$;
typedef swap$state$ * swap$ref$;
extern void swap$init$(swap$ref$ self);
extern void swap$step(swap$ref$ self);
extern void swap$set(swap$ref$ self, int32_t av1, int32_t av2);
extern void swap$get(swap$ref$ self, int32_t* r1, int32_t* r2);
#endif /* _swap_h */
