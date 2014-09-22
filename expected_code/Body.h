#ifndef _Body_h
#define _Body_h

#include <stdint.h>
#include <stdbool.h>

typedef struct {int32_t loopnn }   Body$state$;
typedef Body$state$ * Body$ref$;
extern void Body$init$(Body$ref$ self);
extern void Body$body(Body$ref$ self, int32_t ii, int32_t cc, int32_t* dd);
extern void Body$value(Body$ref$ self, int32_t* vv);
#endif /* _Body_h */
