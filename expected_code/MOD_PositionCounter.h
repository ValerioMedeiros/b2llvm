#ifndef _MOD_PositionCounter_h
#define _MOD_PositionCounter_h

#include <stdint.h>
#include <stdbool.h>

typedef struct {int32_t pos }   MOD_PositionCounter$state$;
typedef MOD_PositionCounter$state$ * MOD_PositionCounter$ref$;
extern void MOD_PositionCounter$init$(MOD_PositionCounter$ref$ self);
extern void MOD_PositionCounter$posinc(MOD_PositionCounter$ref$ self);
extern void MOD_PositionCounter$posget(MOD_PositionCounter$ref$ self, int32_t* pp);
#endif /* _MOD_PositionCounter_h */
