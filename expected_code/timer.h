#ifndef _timer_h
#define _timer_h

#include <stdint.h>
#include <stdbool.h>

typedef struct {int32_t value; bool error; }   counter$state$;
typedef counter$state$ * counter$ref$;
typedef struct {counter$ref$; counter$ref$; counter$ref$; bool is_running; bool overflow; }   timer$state$;
typedef timer$state$ * timer$ref$;
extern void timer$init$(timer$ref$ self, counter$ref$ self, counter$ref$ self, counter$ref$ self);
extern void timer$tick(timer$ref$ self);
extern void timer$reset(timer$ref$ self);
extern void timer$stop(timer$ref$ self);
extern void timer$start(timer$ref$ self);
extern void timer$elapsed(timer$ref$ self, int32_t* hours, int32_t* minutes, int32_t* seconds);
extern void timer$has_overflown(timer$ref$ self, bool* answer);
#endif /* _timer_h */
