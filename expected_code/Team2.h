#ifndef _Team2_h
#define _Team2_h

#include <stdint.h>
#include <stdbool.h>

typedef struct {int32_t team_array[11] }   Team2$state$;
typedef Team2$state$ * Team2$ref$;
extern void Team2$init$(Team2$ref$ self);
extern void Team2$substitute(Team2$ref$ self, int32_t pp, int32_t rr);
extern void Team2$in_team(Team2$ref$ self, int32_t pp, bool* aa);
#endif /* _Team2_h */
