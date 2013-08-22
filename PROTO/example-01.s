;; -*- asm-mode -*-

%counter_i$state$ = type { i32, i1 }
@counter_i$self$ = common global %counter_i$state$ zeroinitializer

define void @counter_i$init$(%counter_i$state$ * %self$) {
entry:
  %0 = getelementptr %counter_i$state$ * @counter_i$self$, i32 0, i32 0
  store i32 0, i32 * %0
  %1 = getelementptr %counter_i$state$ * @counter_i$self$, i32 0, i32 1
  store i1 0, i1 * %1
  br label %exit
exit:
  ret void
}

define void @counter_i$zero(%counter_i$state$ * %self$) {
entry:
  %0 = getelementptr %counter_i$state$ * %self$, i32 0, i32 0
  store i32 0, i32 * %0
  %1 = getelementptr %counter_i$state$ * %self$, i32 0, i32 1
  store i1 0, i1 * %1
  br label %exit
exit:
  ret void
}

define void @counter_i$inc(%counter_i$state$ * %self$) {
entry:
  %0 = getelementptr %counter_i$state$ * %self$, i32 0, i32 0
  %1 = load i32* %0
  %2 = icmp slt i32 %1, 2147483647
  br i1 %2, label %lbl3, label %lbl4
lbl3:
  %3 = getelementptr %counter_i$state$ * %self$, i32 0, i32 0
  %4 = load i32* %3
  %5 = add i32 %4, 1
  %6 = getelementptr %counter_i$state$ * %self$, i32 0, i32 0
  store i32 %5, i32* %6
  br label %exit
lbl4:
  %7 = getelementptr %counter_i$state$ * %self$, i32 0, i32 1
  store i1 1, i1* %7
  br label %exit
exit:
  ret void
}

@.str = private constant [12 x i8] c"value = %i\0A\00", align 1 ; <[12 x i8]*> [#uses=1]
@.str1 = private constant [12 x i8] c"error = %i\0A\00", align 1 ; <[12 x i8]*> [#uses=1]
@.str2 = private constant [36 x i8] c"Type 'z': zero, 'i': inc, 'q': quit\00", align 1 ; <[36 x i8]*> [#uses=1]
@.str3 = private constant [16 x i8] c"Initializing...\00", align 1 ; <[16 x i8]*> [#uses=1]

define void @print_state() nounwind ssp {
entry:
  %0 = load i32* getelementptr inbounds (%counter_i$state$* @counter_i$self$, i64 0, i32 0), align 4 ; <i32> [#uses=1]
  %1 = tail call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([12 x i8]* @.str, i64 0, i64 0), i32 %0) nounwind ; <i32> [#uses=0]
  %2 = load i1* getelementptr inbounds (%counter_i$state$* @counter_i$self$, i64 0, i32 1), align 4 ; <i32> [#uses=1]
  %3 = tail call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([12 x i8]* @.str, i64 0, i64 0), i1 %2) nounwind ; <i32> [#uses=0]
  ret void
}

declare i32 @printf(i8* nocapture, ...) nounwind

define i32 @main() nounwind ssp {
entry:
  %retval = alloca i32                            ; <i32*> [#uses=2]
  %0 = alloca i32                                 ; <i32*> [#uses=2]
  %c = alloca i8                                  ; <i8*> [#uses=2]
  %"alloca point" = bitcast i32 0 to i32          ; <i32> [#uses=0]
  %1 = call i32 @puts(i8* getelementptr inbounds ([16 x i8]* @.str3, i64 0, i64 0)) nounwind ; <i32> [#uses=0]
  call void @counter_i$init$(%counter_i$state$* @counter_i$self$) nounwind ssp
  call void @print_state() nounwind ssp
  br label %bb

bb:                                               ; preds = %bb3, %entry
  %2 = call i32 @puts(i8* getelementptr inbounds ([36 x i8]* @.str2, i64 0, i64 0)) nounwind ; <i32> [#uses=0]
  %3 = call i32 @getchar() nounwind               ; <i32> [#uses=1]
  %4 = trunc i32 %3 to i8                         ; <i8> [#uses=1]
  store i8 %4, i8* %c, align 1
  %5 = load i8* %c, align 1                       ; <i8> [#uses=1]
  %6 = sext i8 %5 to i32                          ; <i32> [#uses=1]
  switch i32 %6, label %bb4 [
    i32 121, label %bb1
    i32 105, label %bb2
    i32 113, label %bb3
  ]

bb1:                                              ; preds = %bb
  call void @counter_i$zero(%counter_i$state$* @counter_i$self$) nounwind ssp
  br label %bb4

bb2:                                              ; preds = %bb
  call void @counter_i$inc(%counter_i$state$* @counter_i$self$) nounwind ssp
  br label %bb4

bb3:                                              ; preds = %bb
  store i32 0, i32* %0, align 4
  %7 = load i32* %0, align 4                      ; <i32> [#uses=1]
  store i32 %7, i32* %retval, align 4
  br label %return

bb4:                                              ; preds = %bb1, %bb
  call void @print_state() nounwind ssp
  br label %bb

return:                                           ; preds = %bb2
  %retval4 = load i32* %retval                    ; <i32> [#uses=1]
  ret i32 %retval4
}

declare i32 @puts(i8*)

declare i32 @getchar()
