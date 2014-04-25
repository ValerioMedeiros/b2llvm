#ifndef _counter_h
#define _counter_h

#include <stdint.h>
#include <stdbool.h>
#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */
    
    
    /* Clause SETS */
    
    /* Clause CONCRETE_VARIABLES */
    
    
    /* Clause CONCRETE_CONSTANTS */
    /* Basic constants */
    /* Array and record constants */

   // Passo 2 - Declarando os typedef 
   typedef struct  { int32_t value; bool error; } counter$state$;
   typedef counter$state$ * counter$ref$;



   // Passo 1 - Adicionando a renomeiação das variáveis e usando o parâmetro de contexto.
    extern void counter$INITIALISATION(counter$ref$ self);
   // Passo 3 - Remove as declarações das variáveis antigas no arquivo counter.c 
   // Passo 4 - Atualiza as variáveis no arquivo de teste para usar a referencia a estrutura de estado. Esta mesma sequência de passos segui no arquivo de teste.
   // Passo 5 - Faz a reomeação das funções nos arquivos .c e .h. Exemplo: counter__zero -> counter$zero. Precisa somente counter__-> counter$
   // Passo 6 - Comparar a compatilibilidade entre o arquivo .c baseado no atelierb e o llvm criando com B2llvm
 

    /* Clause OPERATIONS */
    
    extern void counter$zero(counter$ref$ self);
    extern void counter$inc(counter$ref$ self);
    extern void counter$get(counter$ref$ self, int32_t *res);
    
#ifdef __cplusplus
}
#endif /* __cplusplus */


#endif /* _counter_h */
