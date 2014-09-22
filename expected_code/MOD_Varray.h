#ifndef _MOD_Varray_h
#define _MOD_Varray_h

#include <stdint.h>
#include <stdbool.h>

typedef struct {int32_t array[101] }   MOD_Varray$state$;
typedef MOD_Varray$state$ * MOD_Varray$ref$;
extern void MOD_Varray$init$(MOD_Varray$ref$ self);
extern void MOD_Varray$set(MOD_Varray$ref$ self, int32_t ii, int32_t vv);
extern void MOD_Varray$get(MOD_Varray$ref$ self, int32_t ii, int32_t* vv);
#endif /* _MOD_Varray_h */
