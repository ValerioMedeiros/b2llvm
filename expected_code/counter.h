#ifndef _counter_h
#define _counter_h

#include <stdint.h>
#include <stdbool.h>

typedef struct {int32_t value; bool error; }   counter$state$;
typedef counter$state$ * counter$ref$;
extern void counter$init$(counter$ref$ self);
extern void counter$zero(counter$ref$ self);
extern void counter$inc(counter$ref$ self);
extern void counter$get(counter$ref$ self, int32_t* res);
#endif /* _counter_h */
