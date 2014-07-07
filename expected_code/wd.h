#ifndef _wd_h
#define _wd_h

#include <stdint.h>
#include <stdbool.h>

typedef struct {int32_t value; bool error; }   counter$state$;
typedef counter$state$ * counter$ref$;
typedef struct {counter$ref$ }   wd$state$;
typedef wd$state$ * wd$ref$;
extern void wd$init$(wd$ref$ self, counter$ref$ self);
extern void wd$start(wd$ref$ self);
extern void wd$tick(wd$ref$ self);
extern void wd$expired(wd$ref$ self, bool* res);
#endif /* _wd_h */
