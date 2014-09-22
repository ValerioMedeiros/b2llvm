#ifndef _array_h
#define _array_h

#include <stdint.h>
#include <stdbool.h>

typedef struct {int32_t arr[100]; int32_t arr2d[100][100]; int32_t arr_n[100][100]; int32_t tmp[100]; int32_t short_array[3]; int32_t a3d[2][2][4]; }   array$state$;
typedef array$state$ * array$ref$;
extern void array$init$(array$ref$ self);
#endif /* _array_h */
