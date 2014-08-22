; ModuleID = 'ex.c'
target datalayout = "e-p:64:64:64-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:64:64-f32:32:32-f64:64:64-v64:64:64-v128:128:128-a0:0:64-s0:64:64-f80:128:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.9.0"

%struct.anon = type { i32, i32, i32 }

; Function Attrs: nounwind ssp uwtable
define void @norm(%struct.anon* nocapture %P) #0 {
  %g = alloca i32, align 4
  %1 = getelementptr inbounds %struct.anon* %P, i64 0, i32 2
  %2 = load i32* %1, align 4, !tbaa !1
  %3 = icmp eq i32 %2, 0
  br i1 %3, label %13, label %4

; <label>:4                                       ; preds = %0
  %5 = getelementptr inbounds %struct.anon* %P, i64 0, i32 1
  %6 = load i32* %5, align 4, !tbaa !6
  call void @gcd(i32* %g, i32 %6, i32 %2) #2
  %7 = load i32* %g, align 4, !tbaa !7
  %8 = load i32* %5, align 4, !tbaa !6
  %9 = sdiv i32 %8, %7
  store i32 %9, i32* %5, align 4, !tbaa !6
  %10 = load i32* %g, align 4, !tbaa !7
  %11 = load i32* %1, align 4, !tbaa !1
  %12 = sdiv i32 %11, %10
  store i32 %12, i32* %1, align 4, !tbaa !1
  br label %13

; <label>:13                                      ; preds = %0, %4
  ret void
}

declare void @gcd(i32*, i32, i32) #1

attributes #0 = { nounwind ssp uwtable "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { nounwind }

!llvm.ident = !{!0}

!0 = metadata !{metadata !"Apple LLVM version 5.1 (clang-503.0.40) (based on LLVM 3.4svn)"}
!1 = metadata !{metadata !2, metadata !3, i64 8}
!2 = metadata !{metadata !"", metadata !3, i64 0, metadata !3, i64 4, metadata !3, i64 8}
!3 = metadata !{metadata !"int", metadata !4, i64 0}
!4 = metadata !{metadata !"omnipotent char", metadata !5, i64 0}
!5 = metadata !{metadata !"Simple C/C++ TBAA"}
!6 = metadata !{metadata !2, metadata !3, i64 4}
!7 = metadata !{metadata !3, metadata !3, i64 0}
