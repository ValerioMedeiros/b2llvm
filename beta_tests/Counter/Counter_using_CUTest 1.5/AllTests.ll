; ModuleID = 'AllTests.c'
target datalayout = "e-p:64:64:64-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:64:64-f32:32:32-f64:64:64-v64:64:64-v128:128:128-a0:0:64-s0:64:64-f80:128:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.9.0"

%"struct.counter$state$" = type { i32, i8 }
%struct.CuTest = type { i8*, {}*, i32, i32, i8*, [37 x i32]* }
%struct.CuSuite = type { i32, [1024 x %struct.CuTest*], i32 }
%struct.CuString = type { i32, i32, i8* }

@counter = common global %"struct.counter$state$" zeroinitializer, align 4
@.str = private unnamed_addr constant [11 x i8] c"AllTests.c\00", align 1
@.str1 = private unnamed_addr constant [18 x i8] c"Invariant invalid\00", align 1
@.str2 = private unnamed_addr constant [24 x i8] c"Test_oper_inc_testCase1\00", align 1
@.str3 = private unnamed_addr constant [24 x i8] c"Test_oper_inc_testCase2\00", align 1
@.str4 = private unnamed_addr constant [25 x i8] c"Test_oper_zero_testCase1\00", align 1
@.str5 = private unnamed_addr constant [4 x i8] c"%s\0A\00", align 1

; Function Attrs: nounwind ssp uwtable
define void @Test_oper_inc_testCase1(%struct.CuTest* %tc) #0 {
  %1 = alloca %struct.CuTest*, align 8
  %condition = alloca i8, align 1
  store %struct.CuTest* %tc, %struct.CuTest** %1, align 8
  store i32 0, i32* getelementptr inbounds (%"struct.counter$state$"* @counter, i32 0, i32 0), align 4
  store i8 0, i8* getelementptr inbounds (%"struct.counter$state$"* @counter, i32 0, i32 1), align 1
  call void @"counter$INITIALISATION"(%"struct.counter$state$"* @counter)
  call void @"counter$inc"(%"struct.counter$state$"* @counter)
  %2 = load i8* getelementptr inbounds (%"struct.counter$state$"* @counter, i32 0, i32 1), align 1
  %3 = trunc i8 %2 to i1
  %4 = zext i1 %3 to i32
  %5 = icmp eq i32 %4, 1
  br i1 %5, label %6, label %9

; <label>:6                                       ; preds = %0
  %7 = load i32* getelementptr inbounds (%"struct.counter$state$"* @counter, i32 0, i32 0), align 4
  %8 = icmp eq i32 %7, 2147483647
  br label %9

; <label>:9                                       ; preds = %6, %0
  %10 = phi i1 [ true, %0 ], [ %8, %6 ]
  %11 = zext i1 %10 to i8
  store i8 %11, i8* %condition, align 1
  %12 = load %struct.CuTest** %1, align 8
  %13 = load i8* %condition, align 1
  %14 = trunc i8 %13 to i1
  %15 = zext i1 %14 to i32
  call void @CuAssert_Line(%struct.CuTest* %12, i8* getelementptr inbounds ([11 x i8]* @.str, i32 0, i32 0), i32 22, i8* getelementptr inbounds ([18 x i8]* @.str1, i32 0, i32 0), i32 %15)
  ret void
}

declare void @"counter$INITIALISATION"(%"struct.counter$state$"*) #1

declare void @"counter$inc"(%"struct.counter$state$"*) #1

declare void @CuAssert_Line(%struct.CuTest*, i8*, i32, i8*, i32) #1

; Function Attrs: nounwind ssp uwtable
define void @Test_oper_inc_testCase2(%struct.CuTest* %tc) #0 {
  %1 = alloca %struct.CuTest*, align 8
  %condition = alloca i8, align 1
  store %struct.CuTest* %tc, %struct.CuTest** %1, align 8
  store i32 3, i32* getelementptr inbounds (%"struct.counter$state$"* @counter, i32 0, i32 0), align 4
  store i8 1, i8* getelementptr inbounds (%"struct.counter$state$"* @counter, i32 0, i32 1), align 1
  call void @"counter$inc"(%"struct.counter$state$"* @counter)
  %2 = load i8* getelementptr inbounds (%"struct.counter$state$"* @counter, i32 0, i32 1), align 1
  %3 = trunc i8 %2 to i1
  %4 = zext i1 %3 to i32
  %5 = icmp eq i32 %4, 1
  br i1 %5, label %6, label %9

; <label>:6                                       ; preds = %0
  %7 = load i32* getelementptr inbounds (%"struct.counter$state$"* @counter, i32 0, i32 0), align 4
  %8 = icmp eq i32 %7, 2147483647
  br label %9

; <label>:9                                       ; preds = %6, %0
  %10 = phi i1 [ true, %0 ], [ %8, %6 ]
  %11 = zext i1 %10 to i8
  store i8 %11, i8* %condition, align 1
  %12 = load %struct.CuTest** %1, align 8
  %13 = load i8* %condition, align 1
  %14 = trunc i8 %13 to i1
  %15 = zext i1 %14 to i32
  call void @CuAssert_Line(%struct.CuTest* %12, i8* getelementptr inbounds ([11 x i8]* @.str, i32 0, i32 0), i32 37, i8* getelementptr inbounds ([18 x i8]* @.str1, i32 0, i32 0), i32 %15)
  ret void
}

; Function Attrs: nounwind ssp uwtable
define void @Test_oper_zero_testCase1(%struct.CuTest* %tc) #0 {
  %1 = alloca %struct.CuTest*, align 8
  %condition = alloca i8, align 1
  store %struct.CuTest* %tc, %struct.CuTest** %1, align 8
  store i32 3, i32* getelementptr inbounds (%"struct.counter$state$"* @counter, i32 0, i32 0), align 4
  store i8 1, i8* getelementptr inbounds (%"struct.counter$state$"* @counter, i32 0, i32 1), align 1
  call void @"counter$zero"(%"struct.counter$state$"* @counter)
  %2 = load i8* getelementptr inbounds (%"struct.counter$state$"* @counter, i32 0, i32 1), align 1
  %3 = trunc i8 %2 to i1
  %4 = zext i1 %3 to i32
  %5 = icmp eq i32 %4, 1
  br i1 %5, label %6, label %9

; <label>:6                                       ; preds = %0
  %7 = load i32* getelementptr inbounds (%"struct.counter$state$"* @counter, i32 0, i32 0), align 4
  %8 = icmp eq i32 %7, 2147483647
  br label %9

; <label>:9                                       ; preds = %6, %0
  %10 = phi i1 [ true, %0 ], [ %8, %6 ]
  %11 = zext i1 %10 to i8
  store i8 %11, i8* %condition, align 1
  %12 = load %struct.CuTest** %1, align 8
  %13 = load i8* %condition, align 1
  %14 = trunc i8 %13 to i1
  %15 = zext i1 %14 to i32
  call void @CuAssert_Line(%struct.CuTest* %12, i8* getelementptr inbounds ([11 x i8]* @.str, i32 0, i32 0), i32 51, i8* getelementptr inbounds ([18 x i8]* @.str1, i32 0, i32 0), i32 %15)
  ret void
}

declare void @"counter$zero"(%"struct.counter$state$"*) #1

; Function Attrs: nounwind ssp uwtable
define %struct.CuSuite* @testsSuite() #0 {
  %suite = alloca %struct.CuSuite*, align 8
  %1 = call %struct.CuSuite* @CuSuiteNew()
  store %struct.CuSuite* %1, %struct.CuSuite** %suite, align 8
  %2 = load %struct.CuSuite** %suite, align 8
  %3 = call %struct.CuTest* @CuTestNew(i8* getelementptr inbounds ([24 x i8]* @.str2, i32 0, i32 0), void (%struct.CuTest*)* @Test_oper_inc_testCase1)
  call void @CuSuiteAdd(%struct.CuSuite* %2, %struct.CuTest* %3)
  %4 = load %struct.CuSuite** %suite, align 8
  %5 = call %struct.CuTest* @CuTestNew(i8* getelementptr inbounds ([24 x i8]* @.str3, i32 0, i32 0), void (%struct.CuTest*)* @Test_oper_inc_testCase2)
  call void @CuSuiteAdd(%struct.CuSuite* %4, %struct.CuTest* %5)
  %6 = load %struct.CuSuite** %suite, align 8
  %7 = call %struct.CuTest* @CuTestNew(i8* getelementptr inbounds ([25 x i8]* @.str4, i32 0, i32 0), void (%struct.CuTest*)* @Test_oper_zero_testCase1)
  call void @CuSuiteAdd(%struct.CuSuite* %6, %struct.CuTest* %7)
  %8 = load %struct.CuSuite** %suite, align 8
  ret %struct.CuSuite* %8
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
  %4 = call %struct.CuSuite* @testsSuite()
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
  %13 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([4 x i8]* @.str5, i32 0, i32 0), i8* %12)
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
