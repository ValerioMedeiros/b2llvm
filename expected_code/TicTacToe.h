#ifndef _TicTacToe_h
#define _TicTacToe_h

#include <stdint.h>
#include <stdbool.h>

typedef struct {int32_t board[9]; bool blue_turn; }   TicTacToe$state$;
typedef TicTacToe$state$ * TicTacToe$ref$;
extern void TicTacToe$init$(TicTacToe$ref$ self);
extern void TicTacToe$BlueMove(TicTacToe$ref$ self, int32_t pp);
extern void TicTacToe$RedMove(TicTacToe$ref$ self, int32_t pp);
extern void TicTacToe$GameResult(TicTacToe$ref$ self, int32_t* result);
#endif /* _TicTacToe_h */
