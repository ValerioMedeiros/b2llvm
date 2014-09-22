#ifndef _bubble_h
#define _bubble_h

#include <stdint.h>
#include <stdbool.h>

typedef struct {int32_t vec1[100]; int32_t sort1; }   bubble$state$;
typedef bubble$state$ * bubble$ref$;
extern void bubble$init$(bubble$ref$ self);
#endif /* _bubble_h */
