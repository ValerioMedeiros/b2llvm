#ifndef _MOD_SizeCounter_h
#define _MOD_SizeCounter_h

#include <stdint.h>
#include <stdbool.h>

typedef struct {int32_t sze }   MOD_SizeCounter$state$;
typedef MOD_SizeCounter$state$ * MOD_SizeCounter$ref$;
extern void MOD_SizeCounter$init$(MOD_SizeCounter$ref$ self);
extern void MOD_SizeCounter$szeinc(MOD_SizeCounter$ref$ self);
extern void MOD_SizeCounter$szedec(MOD_SizeCounter$ref$ self);
extern void MOD_SizeCounter$szeget(MOD_SizeCounter$ref$ self, int32_t* ss);
#endif /* _MOD_SizeCounter_h */
