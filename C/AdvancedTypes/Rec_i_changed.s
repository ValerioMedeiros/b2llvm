; ModuleID = 'Rec_i_changed.c'
target datalayout = "e-p:64:64:64-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:64:64-f32:32:32-f64:64:64-v64:64:64-v128:128:128-a0:0:64-s0:64:64-f80:128:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.9.0"

%struct.R_1 = type { i32, i32, double }
%struct.point = type { i32, i32 }

@.str = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
@Rec__account = internal global %struct.R_1 zeroinitializer, align 8
@.str1 = private unnamed_addr constant [5 x i8] c"%lf\0A\00", align 1
@Rec__INITIALISATION.p = private unnamed_addr constant %struct.point { i32 1, i32 2 }, align 4

define i32 @main() nounwind ssp uwtable {
  call void @Rec__set()
  %1 = load i32* getelementptr inbounds (%struct.R_1* @Rec__account, i32 0, i32 1), align 4
  %2 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([4 x i8]* @.str, i32 0, i32 0), i32 %1)
  call void @Rec__get_and_set()
  %3 = load i32* getelementptr inbounds (%struct.R_1* @Rec__account, i32 0, i32 1), align 4
  %4 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([4 x i8]* @.str, i32 0, i32 0), i32 %3)
  call void @Rec__INITIALISATION()
  %5 = load double* getelementptr inbounds (%struct.R_1* @Rec__account, i32 0, i32 2), align 8
  %6 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([5 x i8]* @.str1, i32 0, i32 0), double %5)
  ret i32 0
}

define void @Rec__set() nounwind ssp uwtable {
  store i32 50, i32* getelementptr inbounds (%struct.R_1* @Rec__account, i32 0, i32 1), align 4
  ret void
}

declare i32 @printf(i8*, ...)

define void @Rec__get_and_set() nounwind ssp uwtable {
  %l = getelementptr inbounds %struct.R_1* @Rec__account, i32 0, i32 1
  %1 = load i32* %l
  %2 = sub nsw i32 %1, 50
  %3 = getelementptr inbounds %struct.R_1* @Rec__account, i32 0, i32 1
  store i32 %2, i32* %3
  ret void
}

define void @Rec__INITIALISATION() nounwind ssp uwtable {
  %p = alloca %struct.point, align 4
  %pi = alloca %struct.point, align 4
  %1 = bitcast %struct.point* %p to i8*
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* %1, i8* bitcast (%struct.point* @Rec__INITIALISATION.p to i8*), i64 8, i32 4, i1 false)
  %2 = getelementptr inbounds %struct.point* %pi, i32 0, i32 1
  store i32 700, i32* %2, align 4
  %3 = getelementptr inbounds %struct.point* %pi, i32 0, i32 0
  store i32 900, i32* %3, align 4
  store i32 0, i32* getelementptr inbounds (%struct.R_1* @Rec__account, i32 0, i32 0), align 4
  store i32 10, i32* getelementptr inbounds (%struct.R_1* @Rec__account, i32 0, i32 1), align 4
  store double 7.000000e+00, double* getelementptr inbounds (%struct.R_1* @Rec__account, i32 0, i32 2), align 8
  ret void
}

declare void @llvm.memcpy.p0i8.p0i8.i64(i8* nocapture, i8* nocapture, i64, i32, i1) nounwind

define void @Rec__positive(i8* %res) nounwind ssp uwtable {
  %1 = alloca i8*, align 8
  store i8* %res, i8** %1, align 8
  %2 = load i32* getelementptr inbounds (%struct.R_1* @Rec__account, i32 0, i32 1), align 4
  %3 = icmp sgt i32 %2, 0
  br i1 %3, label %4, label %6

; <label>:4                                       ; preds = %0
  %5 = load i8** %1, align 8
  store i8 1, i8* %5, align 1
  br label %8

; <label>:6                                       ; preds = %0
  %7 = load i8** %1, align 8
  store i8 0, i8* %7, align 1
  br label %8

; <label>:8                                       ; preds = %6, %4
  ret void
}

define void @Rec__withrdaw(i32 %amt) nounwind ssp uwtable {
  %1 = alloca i32, align 4
  store i32 %amt, i32* %1, align 4
  %2 = load i32* %1, align 4
  %3 = icmp sge i32 %2, 0
  br i1 %3, label %4, label %16

; <label>:4                                       ; preds = %0
  %5 = load i32* %1, align 4
  %6 = icmp sle i32 %5, 2147483647
  br i1 %6, label %7, label %16

; <label>:7                                       ; preds = %4
  %8 = load i32* getelementptr inbounds (%struct.R_1* @Rec__account, i32 0, i32 1), align 4
  %9 = load i32* %1, align 4
  %10 = icmp sge i32 %8, %9
  br i1 %10, label %11, label %16

; <label>:11                                      ; preds = %7
  %12 = load i32* getelementptr inbounds (%struct.R_1* @Rec__account, i32 0, i32 0), align 4
  store i32 %12, i32* getelementptr inbounds (%struct.R_1* @Rec__account, i32 0, i32 0), align 4
  %13 = load i32* getelementptr inbounds (%struct.R_1* @Rec__account, i32 0, i32 1), align 4
  %14 = load i32* %1, align 4
  %15 = sub nsw i32 %13, %14
  store i32 %15, i32* getelementptr inbounds (%struct.R_1* @Rec__account, i32 0, i32 1), align 4
  br label %16

; <label>:16                                      ; preds = %11, %7, %4, %0
  ret void
}

define void @Rec__unsafe_dec() nounwind ssp uwtable {
  %1 = load i32* getelementptr inbounds (%struct.R_1* @Rec__account, i32 0, i32 1), align 4
  %2 = sub nsw i32 %1, 1
  store i32 %2, i32* getelementptr inbounds (%struct.R_1* @Rec__account, i32 0, i32 1), align 4
  ret void
}
