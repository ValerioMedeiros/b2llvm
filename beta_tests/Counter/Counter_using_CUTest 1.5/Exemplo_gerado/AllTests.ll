; ModuleID = 'AllTests.c'
target datalayout = "e-p:64:64:64-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:64:64-f32:32:32-f64:64:64-v64:64:64-v128:128:128-a0:0:64-s0:64:64-f80:128:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.9.0"

%"struct.counter$state$" = type { i32, i8 }
%struct.CuTest = type { i8*, void (%struct.CuTest*)*, i32, i32, i8*, [37 x i32]* }
%struct.CuSuite = type { i32, [1024 x %struct.CuTest*], i32 }
%struct.CuString = type { i32, i32, i8* }

@.str = private unnamed_addr constant [11 x i8] c"AllTests.c\00", align 1
@.str1 = private unnamed_addr constant [69 x i8] c"The invariant '((error = TRUE) => (value = MAXINT))' was unsatisfied\00", align 1
@.str2 = private unnamed_addr constant [43 x i8] c"The invariant '0 <= value' was unsatisfied\00", align 1
@.str3 = private unnamed_addr constant [48 x i8] c"The invariant 'value <= MAXINT' was unsatisfied\00", align 1
@counter = common global %"struct.counter$state$" zeroinitializer, align 4
@.str4 = private unnamed_addr constant [14 x i8] c"assert failed\00", align 1
@.str5 = private unnamed_addr constant [24 x i8] c"counter_inc_test_case_1\00", align 1
@.str6 = private unnamed_addr constant [24 x i8] c"counter_inc_test_case_2\00", align 1
@.str7 = private unnamed_addr constant [4 x i8] c"%s\0A\00", align 1

; Function Attrs: nounwind ssp uwtable
define void @check_invariant(%struct.CuTest* %tc, i64 %counter.coerce) #0 {
  %1 = alloca %struct.CuTest*, align 8
  %counter = alloca %"struct.counter$state$", align 8
  store %struct.CuTest* %tc, %struct.CuTest** %1, align 8
  %2 = bitcast %"struct.counter$state$"* %counter to i64*
  store i64 %counter.coerce, i64* %2, align 1
  %3 = getelementptr inbounds %"struct.counter$state$"* %counter, i32 0, i32 1
  %4 = load i8* %3, align 1
  %5 = trunc i8 %4 to i1
  %6 = zext i1 %5 to i32
  %7 = icmp eq i32 %6, 1
  br i1 %7, label %8, label %14

; <label>:8                                       ; preds = %0
  %9 = getelementptr inbounds %"struct.counter$state$"* %counter, i32 0, i32 0
  %10 = load i32* %9, align 4
  %11 = icmp eq i32 %10, 2147483647
  br i1 %11, label %14, label %12

; <label>:12                                      ; preds = %8
  %13 = load %struct.CuTest** %1, align 8
  call void @CuFail_Line(%struct.CuTest* %13, i8* getelementptr inbounds ([11 x i8]* @.str, i32 0, i32 0), i32 12, i8* null, i8* getelementptr inbounds ([69 x i8]* @.str1, i32 0, i32 0))
  br label %14

; <label>:14                                      ; preds = %12, %8, %0
  %15 = getelementptr inbounds %"struct.counter$state$"* %counter, i32 0, i32 0
  %16 = load i32* %15, align 4
  %17 = icmp sle i32 0, %16
  br i1 %17, label %20, label %18

; <label>:18                                      ; preds = %14
  %19 = load %struct.CuTest** %1, align 8
  call void @CuFail_Line(%struct.CuTest* %19, i8* getelementptr inbounds ([11 x i8]* @.str, i32 0, i32 0), i32 16, i8* null, i8* getelementptr inbounds ([43 x i8]* @.str2, i32 0, i32 0))
  br label %20

; <label>:20                                      ; preds = %18, %14
  %21 = getelementptr inbounds %"struct.counter$state$"* %counter, i32 0, i32 0
  %22 = load i32* %21, align 4
  %23 = icmp sle i32 %22, 2147483647
  br i1 %23, label %26, label %24

; <label>:24                                      ; preds = %20
  %25 = load %struct.CuTest** %1, align 8
  call void @CuFail_Line(%struct.CuTest* %25, i8* getelementptr inbounds ([11 x i8]* @.str, i32 0, i32 0), i32 20, i8* null, i8* getelementptr inbounds ([48 x i8]* @.str3, i32 0, i32 0))
  br label %26

; <label>:26                                      ; preds = %24, %20
  ret void
}

declare void @CuFail_Line(%struct.CuTest*, i8*, i32, i8*, i8*) #1

; Function Attrs: nounwind ssp uwtable
define void @counter_inc_test_case_1(%struct.CuTest* %tc) #0 {
  %1 = alloca %struct.CuTest*, align 8
  %error = alloca i8, align 1
  %value = alloca i32, align 4
  %errorExpected = alloca i8, align 1
  %valueExpected = alloca i32, align 4
  store %struct.CuTest* %tc, %struct.CuTest** %1, align 8
  store i8 0, i8* %error, align 1
  %2 = load i8* %error, align 1
  %3 = trunc i8 %2 to i1
  %4 = zext i1 %3 to i8
  store i8 %4, i8* getelementptr inbounds (%"struct.counter$state$"* @counter, i32 0, i32 1), align 1
  store i32 0, i32* %value, align 4
  %5 = load i32* %value, align 4
  store i32 %5, i32* getelementptr inbounds (%"struct.counter$state$"* @counter, i32 0, i32 0), align 4
  call void @"counter$inc"(%"struct.counter$state$"* @counter)
  %6 = load %struct.CuTest** %1, align 8
  %7 = load i8* getelementptr inbounds (%"struct.counter$state$"* @counter, i32 0, i32 1), align 1
  %8 = trunc i8 %7 to i1
  %9 = zext i1 %8 to i32
  %10 = icmp eq i32 %9, 0
  %11 = zext i1 %10 to i32
  call void @CuAssert_Line(%struct.CuTest* %6, i8* getelementptr inbounds ([11 x i8]* @.str, i32 0, i32 0), i32 44, i8* getelementptr inbounds ([14 x i8]* @.str4, i32 0, i32 0), i32 %11)
  %12 = load %struct.CuTest** %1, align 8
  %13 = load i32* getelementptr inbounds (%"struct.counter$state$"* @counter, i32 0, i32 0), align 4
  %14 = icmp eq i32 %13, 1
  %15 = zext i1 %14 to i32
  call void @CuAssert_Line(%struct.CuTest* %12, i8* getelementptr inbounds ([11 x i8]* @.str, i32 0, i32 0), i32 47, i8* getelementptr inbounds ([14 x i8]* @.str4, i32 0, i32 0), i32 %15)
  %16 = load %struct.CuTest** %1, align 8
  %17 = load i64* bitcast (%"struct.counter$state$"* @counter to i64*), align 1
  call void @check_invariant(%struct.CuTest* %16, i64 %17)
  ret void
}

declare void @"counter$inc"(%"struct.counter$state$"*) #1

declare void @CuAssert_Line(%struct.CuTest*, i8*, i32, i8*, i32) #1

; Function Attrs: nounwind ssp uwtable
define void @counter_inc_test_case_2(%struct.CuTest* %tc) #0 {
  %1 = alloca %struct.CuTest*, align 8
  %error = alloca i8, align 1
  %value = alloca i32, align 4
  %errorExpected = alloca i8, align 1
  %valueExpected = alloca i32, align 4
  store %struct.CuTest* %tc, %struct.CuTest** %1, align 8
  store i8 1, i8* %error, align 1
  %2 = load i8* %error, align 1
  %3 = trunc i8 %2 to i1
  %4 = zext i1 %3 to i8
  store i8 %4, i8* getelementptr inbounds (%"struct.counter$state$"* @counter, i32 0, i32 1), align 1
  store i32 2147483647, i32* %value, align 4
  %5 = load i32* %value, align 4
  store i32 %5, i32* getelementptr inbounds (%"struct.counter$state$"* @counter, i32 0, i32 0), align 4
  call void @"counter$inc"(%"struct.counter$state$"* @counter)
  %6 = load %struct.CuTest** %1, align 8
  %7 = load i8* getelementptr inbounds (%"struct.counter$state$"* @counter, i32 0, i32 1), align 1
  %8 = trunc i8 %7 to i1
  %9 = zext i1 %8 to i32
  %10 = icmp eq i32 %9, 1
  %11 = zext i1 %10 to i32
  call void @CuAssert_Line(%struct.CuTest* %6, i8* getelementptr inbounds ([11 x i8]* @.str, i32 0, i32 0), i32 70, i8* getelementptr inbounds ([14 x i8]* @.str4, i32 0, i32 0), i32 %11)
  %12 = load %struct.CuTest** %1, align 8
  %13 = load i32* getelementptr inbounds (%"struct.counter$state$"* @counter, i32 0, i32 0), align 4
  %14 = icmp eq i32 %13, 2147483647
  %15 = zext i1 %14 to i32
  call void @CuAssert_Line(%struct.CuTest* %12, i8* getelementptr inbounds ([11 x i8]* @.str, i32 0, i32 0), i32 73, i8* getelementptr inbounds ([14 x i8]* @.str4, i32 0, i32 0), i32 %15)
  %16 = load %struct.CuTest** %1, align 8
  %17 = load i64* bitcast (%"struct.counter$state$"* @counter to i64*), align 1
  call void @check_invariant(%struct.CuTest* %16, i64 %17)
  ret void
}

; Function Attrs: nounwind ssp uwtable
define %struct.CuSuite* @counter_inc_test_suite() #0 {
  %suite = alloca %struct.CuSuite*, align 8
  %1 = call %struct.CuSuite* @CuSuiteNew()
  store %struct.CuSuite* %1, %struct.CuSuite** %suite, align 8
  %2 = load %struct.CuSuite** %suite, align 8
  %3 = call %struct.CuTest* @CuTestNew(i8* getelementptr inbounds ([24 x i8]* @.str5, i32 0, i32 0), void (%struct.CuTest*)* @counter_inc_test_case_1)
  call void @CuSuiteAdd(%struct.CuSuite* %2, %struct.CuTest* %3)
  %4 = load %struct.CuSuite** %suite, align 8
  %5 = call %struct.CuTest* @CuTestNew(i8* getelementptr inbounds ([24 x i8]* @.str6, i32 0, i32 0), void (%struct.CuTest*)* @counter_inc_test_case_2)
  call void @CuSuiteAdd(%struct.CuSuite* %4, %struct.CuTest* %5)
  %6 = load %struct.CuSuite** %suite, align 8
  ret %struct.CuSuite* %6
}

declare %struct.CuSuite* @CuSuiteNew() #1

declare void @CuSuiteAdd(%struct.CuSuite*, %struct.CuTest*) #1

declare %struct.CuTest* @CuTestNew(i8*, void (%struct.CuTest*)*) #1

; Function Attrs: nounwind ssp uwtable
define void @RunAllTests() #0 {
  %output = alloca %struct.CuString*, align 8
  %suite = alloca %struct.CuSuite*, align 8
  %1 = call %struct.CuString* @CuStringNew()
  store %struct.CuString* %1, %struct.CuString** %output, align 8
  %2 = call %struct.CuSuite* @CuSuiteNew()
  store %struct.CuSuite* %2, %struct.CuSuite** %suite, align 8
  %3 = load %struct.CuSuite** %suite, align 8
  %4 = call %struct.CuSuite* @counter_inc_test_suite()
  call void @CuSuiteAddSuite(%struct.CuSuite* %3, %struct.CuSuite* %4)
  %5 = load %struct.CuSuite** %suite, align 8
  call void @CuSuiteRun(%struct.CuSuite* %5)
  %6 = load %struct.CuSuite** %suite, align 8
  %7 = load %struct.CuString** %output, align 8
  call void @CuSuiteSummary(%struct.CuSuite* %6, %struct.CuString* %7)
  %8 = load %struct.CuSuite** %suite, align 8
  %9 = load %struct.CuString** %output, align 8
  call void @CuSuiteDetails(%struct.CuSuite* %8, %struct.CuString* %9)
  %10 = load %struct.CuString** %output, align 8
  %11 = getelementptr inbounds %struct.CuString* %10, i32 0, i32 2
  %12 = load i8** %11, align 8
  %13 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([4 x i8]* @.str7, i32 0, i32 0), i8* %12)
  ret void
}

declare %struct.CuString* @CuStringNew() #1

declare void @CuSuiteAddSuite(%struct.CuSuite*, %struct.CuSuite*) #1

declare void @CuSuiteRun(%struct.CuSuite*) #1

declare void @CuSuiteSummary(%struct.CuSuite*, %struct.CuString*) #1

declare void @CuSuiteDetails(%struct.CuSuite*, %struct.CuString*) #1

declare i32 @printf(i8*, ...) #1

; Function Attrs: nounwind ssp uwtable
define i32 @main() #0 {
  call void @RunAllTests()
  ret i32 0
}

attributes #0 = { nounwind ssp uwtable "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.ident = !{!0}

!0 = metadata !{metadata !"Apple LLVM version 5.1 (clang-503.0.40) (based on LLVM 3.4svn)"}
