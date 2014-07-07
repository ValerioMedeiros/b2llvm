#ifndef _enumeration_h
#define _enumeration_h

#include <stdint.h>
#include <stdbool.h>

typedef struct {i1 current }   enumeration$state$;
typedef enumeration$state$ * enumeration$ref$;
extern void enumeration$init$(enumeration$ref$ self);
extern void enumeration$tick(enumeration$ref$ self);
extern void enumeration$read(enumeration$ref$ self, i1* res);
#endif /* _enumeration_h */
