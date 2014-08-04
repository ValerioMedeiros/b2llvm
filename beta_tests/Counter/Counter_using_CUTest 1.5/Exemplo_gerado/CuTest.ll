; ModuleID = 'CuTest.c'
target datalayout = "e-p:64:64:64-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:64:64-f32:32:32-f64:64:64-v64:64:64-v128:128:128-a0:0:64-s0:64:64-f80:128:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.9.0"

%struct.CuString = type { i32, i32, i8* }
%struct.__va_list_tag = type { i32, i32, i8*, i8* }
%struct.CuTest = type { i8*, void (%struct.CuTest*)*, i32, i32, i8*, [37 x i32]* }
%struct.CuSuite = type { i32, [1024 x %struct.CuTest*], i32 }

@.str = private unnamed_addr constant [5 x i8] c"NULL\00", align 1
@.str1 = private unnamed_addr constant [3 x i8] c": \00", align 1
@.str2 = private unnamed_addr constant [11 x i8] c"expected <\00", align 1
@.str3 = private unnamed_addr constant [12 x i8] c"> but was <\00", align 1
@.str4 = private unnamed_addr constant [2 x i8] c">\00", align 1
@.str5 = private unnamed_addr constant [27 x i8] c"expected <%d> but was <%d>\00", align 1
@.str6 = private unnamed_addr constant [27 x i8] c"expected <%f> but was <%f>\00", align 1
@.str7 = private unnamed_addr constant [39 x i8] c"expected pointer <0x%p> but was <0x%p>\00", align 1
@__func__.CuSuiteAdd = private unnamed_addr constant [11 x i8] c"CuSuiteAdd\00", align 1
@.str8 = private unnamed_addr constant [9 x i8] c"CuTest.c\00", align 1
@.str9 = private unnamed_addr constant [34 x i8] c"testSuite->count < MAX_TEST_CASES\00", align 1
@.str10 = private unnamed_addr constant [2 x i8] c"F\00", align 1
@.str11 = private unnamed_addr constant [2 x i8] c".\00", align 1
@.str12 = private unnamed_addr constant [3 x i8] c"\0A\0A\00", align 1
@.str13 = private unnamed_addr constant [5 x i8] c"test\00", align 1
@.str14 = private unnamed_addr constant [6 x i8] c"tests\00", align 1
@.str15 = private unnamed_addr constant [12 x i8] c"OK (%d %s)\0A\00", align 1
@.str16 = private unnamed_addr constant [22 x i8] c"There was 1 failure:\0A\00", align 1
@.str17 = private unnamed_addr constant [25 x i8] c"There were %d failures:\0A\00", align 1
@.str18 = private unnamed_addr constant [12 x i8] c"%d) %s: %s\0A\00", align 1
@.str19 = private unnamed_addr constant [17 x i8] c"\0A!!!FAILURES!!!\0A\00", align 1
@.str20 = private unnamed_addr constant [10 x i8] c"Runs: %d \00", align 1
@.str21 = private unnamed_addr constant [12 x i8] c"Passes: %d \00", align 1
@.str22 = private unnamed_addr constant [11 x i8] c"Fails: %d\0A\00", align 1
@.str23 = private unnamed_addr constant [8 x i8] c"%s:%d: \00", align 1

; Function Attrs: nounwind ssp uwtable
define i8* @CuStrAlloc(i32 %size) #0 {
  %1 = alloca i32, align 4
  %newStr = alloca i8*, align 8
  store i32 %size, i32* %1, align 4
  %2 = load i32* %1, align 4
  %3 = sext i32 %2 to i64
  %4 = mul i64 1, %3
  %5 = call i8* @malloc(i64 %4)
  store i8* %5, i8** %newStr, align 8
  %6 = load i8** %newStr, align 8
  ret i8* %6
}

declare i8* @malloc(i64) #1

; Function Attrs: nounwind ssp uwtable
define i8* @CuStrCopy(i8* %old) #0 {
  %1 = alloca i8*, align 8
  %len = alloca i32, align 4
  %newStr = alloca i8*, align 8
  store i8* %old, i8** %1, align 8
  %2 = load i8** %1, align 8
  %3 = call i64 @strlen(i8* %2)
  %4 = trunc i64 %3 to i32
  store i32 %4, i32* %len, align 4
  %5 = load i32* %len, align 4
  %6 = add nsw i32 %5, 1
  %7 = call i8* @CuStrAlloc(i32 %6)
  store i8* %7, i8** %newStr, align 8
  %8 = load i8** %newStr, align 8
  %9 = load i8** %1, align 8
  %10 = load i8** %newStr, align 8
  %11 = call i64 @llvm.objectsize.i64.p0i8(i8* %10, i1 false)
  %12 = call i8* @__strcpy_chk(i8* %8, i8* %9, i64 %11) #4
  %13 = load i8** %newStr, align 8
  ret i8* %13
}

declare i64 @strlen(i8*) #1

; Function Attrs: nounwind
declare i8* @__strcpy_chk(i8*, i8*, i64) #2

; Function Attrs: nounwind readnone
declare i64 @llvm.objectsize.i64.p0i8(i8*, i1) #3

; Function Attrs: nounwind ssp uwtable
define void @CuStringInit(%struct.CuString* %str) #0 {
  %1 = alloca %struct.CuString*, align 8
  store %struct.CuString* %str, %struct.CuString** %1, align 8
  %2 = load %struct.CuString** %1, align 8
  %3 = getelementptr inbounds %struct.CuString* %2, i32 0, i32 0
  store i32 0, i32* %3, align 4
  %4 = load %struct.CuString** %1, align 8
  %5 = getelementptr inbounds %struct.CuString* %4, i32 0, i32 1
  store i32 256, i32* %5, align 4
  %6 = load %struct.CuString** %1, align 8
  %7 = getelementptr inbounds %struct.CuString* %6, i32 0, i32 1
  %8 = load i32* %7, align 4
  %9 = sext i32 %8 to i64
  %10 = mul i64 1, %9
  %11 = call i8* @malloc(i64 %10)
  %12 = load %struct.CuString** %1, align 8
  %13 = getelementptr inbounds %struct.CuString* %12, i32 0, i32 2
  store i8* %11, i8** %13, align 8
  %14 = load %struct.CuString** %1, align 8
  %15 = getelementptr inbounds %struct.CuString* %14, i32 0, i32 2
  %16 = load i8** %15, align 8
  %17 = getelementptr inbounds i8* %16, i64 0
  store i8 0, i8* %17, align 1
  ret void
}

; Function Attrs: nounwind ssp uwtable
define %struct.CuString* @CuStringNew() #0 {
  %str = alloca %struct.CuString*, align 8
  %1 = call i8* @malloc(i64 16)
  %2 = bitcast i8* %1 to %struct.CuString*
  store %struct.CuString* %2, %struct.CuString** %str, align 8
  %3 = load %struct.CuString** %str, align 8
  %4 = getelementptr inbounds %struct.CuString* %3, i32 0, i32 0
  store i32 0, i32* %4, align 4
  %5 = load %struct.CuString** %str, align 8
  %6 = getelementptr inbounds %struct.CuString* %5, i32 0, i32 1
  store i32 256, i32* %6, align 4
  %7 = load %struct.CuString** %str, align 8
  %8 = getelementptr inbounds %struct.CuString* %7, i32 0, i32 1
  %9 = load i32* %8, align 4
  %10 = sext i32 %9 to i64
  %11 = mul i64 1, %10
  %12 = call i8* @malloc(i64 %11)
  %13 = load %struct.CuString** %str, align 8
  %14 = getelementptr inbounds %struct.CuString* %13, i32 0, i32 2
  store i8* %12, i8** %14, align 8
  %15 = load %struct.CuString** %str, align 8
  %16 = getelementptr inbounds %struct.CuString* %15, i32 0, i32 2
  %17 = load i8** %16, align 8
  %18 = getelementptr inbounds i8* %17, i64 0
  store i8 0, i8* %18, align 1
  %19 = load %struct.CuString** %str, align 8
  ret %struct.CuString* %19
}

; Function Attrs: nounwind ssp uwtable
define void @CuStringDelete(%struct.CuString* %str) #0 {
  %1 = alloca %struct.CuString*, align 8
  store %struct.CuString* %str, %struct.CuString** %1, align 8
  %2 = load %struct.CuString** %1, align 8
  %3 = icmp ne %struct.CuString* %2, null
  br i1 %3, label %5, label %4

; <label>:4                                       ; preds = %0
  br label %11

; <label>:5                                       ; preds = %0
  %6 = load %struct.CuString** %1, align 8
  %7 = getelementptr inbounds %struct.CuString* %6, i32 0, i32 2
  %8 = load i8** %7, align 8
  call void @free(i8* %8)
  %9 = load %struct.CuString** %1, align 8
  %10 = bitcast %struct.CuString* %9 to i8*
  call void @free(i8* %10)
  br label %11

; <label>:11                                      ; preds = %5, %4
  ret void
}

declare void @free(i8*) #1

; Function Attrs: nounwind ssp uwtable
define void @CuStringResize(%struct.CuString* %str, i32 %newSize) #0 {
  %1 = alloca %struct.CuString*, align 8
  %2 = alloca i32, align 4
  store %struct.CuString* %str, %struct.CuString** %1, align 8
  store i32 %newSize, i32* %2, align 4
  %3 = load %struct.CuString** %1, align 8
  %4 = getelementptr inbounds %struct.CuString* %3, i32 0, i32 2
  %5 = load i8** %4, align 8
  %6 = load i32* %2, align 4
  %7 = sext i32 %6 to i64
  %8 = mul i64 1, %7
  %9 = call i8* @realloc(i8* %5, i64 %8)
  %10 = load %struct.CuString** %1, align 8
  %11 = getelementptr inbounds %struct.CuString* %10, i32 0, i32 2
  store i8* %9, i8** %11, align 8
  %12 = load i32* %2, align 4
  %13 = load %struct.CuString** %1, align 8
  %14 = getelementptr inbounds %struct.CuString* %13, i32 0, i32 1
  store i32 %12, i32* %14, align 4
  ret void
}

declare i8* @realloc(i8*, i64) #1

; Function Attrs: nounwind ssp uwtable
define void @CuStringAppend(%struct.CuString* %str, i8* %text) #0 {
  %1 = alloca %struct.CuString*, align 8
  %2 = alloca i8*, align 8
  %length = alloca i32, align 4
  store %struct.CuString* %str, %struct.CuString** %1, align 8
  store i8* %text, i8** %2, align 8
  %3 = load i8** %2, align 8
  %4 = icmp eq i8* %3, null
  br i1 %4, label %5, label %6

; <label>:5                                       ; preds = %0
  store i8* getelementptr inbounds ([5 x i8]* @.str, i32 0, i32 0), i8** %2, align 8
  br label %6

; <label>:6                                       ; preds = %5, %0
  %7 = load i8** %2, align 8
  %8 = call i64 @strlen(i8* %7)
  %9 = trunc i64 %8 to i32
  store i32 %9, i32* %length, align 4
  %10 = load %struct.CuString** %1, align 8
  %11 = getelementptr inbounds %struct.CuString* %10, i32 0, i32 0
  %12 = load i32* %11, align 4
  %13 = load i32* %length, align 4
  %14 = add nsw i32 %12, %13
  %15 = add nsw i32 %14, 1
  %16 = load %struct.CuString** %1, align 8
  %17 = getelementptr inbounds %struct.CuString* %16, i32 0, i32 1
  %18 = load i32* %17, align 4
  %19 = icmp sge i32 %15, %18
  br i1 %19, label %20, label %29

; <label>:20                                      ; preds = %6
  %21 = load %struct.CuString** %1, align 8
  %22 = load %struct.CuString** %1, align 8
  %23 = getelementptr inbounds %struct.CuString* %22, i32 0, i32 0
  %24 = load i32* %23, align 4
  %25 = load i32* %length, align 4
  %26 = add nsw i32 %24, %25
  %27 = add nsw i32 %26, 1
  %28 = add nsw i32 %27, 256
  call void @CuStringResize(%struct.CuString* %21, i32 %28)
  br label %29

; <label>:29                                      ; preds = %20, %6
  %30 = load i32* %length, align 4
  %31 = load %struct.CuString** %1, align 8
  %32 = getelementptr inbounds %struct.CuString* %31, i32 0, i32 0
  %33 = load i32* %32, align 4
  %34 = add nsw i32 %33, %30
  store i32 %34, i32* %32, align 4
  %35 = load %struct.CuString** %1, align 8
  %36 = getelementptr inbounds %struct.CuString* %35, i32 0, i32 2
  %37 = load i8** %36, align 8
  %38 = load i8** %2, align 8
  %39 = load %struct.CuString** %1, align 8
  %40 = getelementptr inbounds %struct.CuString* %39, i32 0, i32 2
  %41 = load i8** %40, align 8
  %42 = call i64 @llvm.objectsize.i64.p0i8(i8* %41, i1 false)
  %43 = call i8* @__strcat_chk(i8* %37, i8* %38, i64 %42) #4
  ret void
}

; Function Attrs: nounwind
declare i8* @__strcat_chk(i8*, i8*, i64) #2

; Function Attrs: nounwind ssp uwtable
define void @CuStringAppendChar(%struct.CuString* %str, i8 signext %ch) #0 {
  %1 = alloca %struct.CuString*, align 8
  %2 = alloca i8, align 1
  %text = alloca [2 x i8], align 1
  store %struct.CuString* %str, %struct.CuString** %1, align 8
  store i8 %ch, i8* %2, align 1
  %3 = load i8* %2, align 1
  %4 = getelementptr inbounds [2 x i8]* %text, i32 0, i64 0
  store i8 %3, i8* %4, align 1
  %5 = getelementptr inbounds [2 x i8]* %text, i32 0, i64 1
  store i8 0, i8* %5, align 1
  %6 = load %struct.CuString** %1, align 8
  %7 = getelementptr inbounds [2 x i8]* %text, i32 0, i32 0
  call void @CuStringAppend(%struct.CuString* %6, i8* %7)
  ret void
}

; Function Attrs: nounwind ssp uwtable
define void @CuStringAppendFormat(%struct.CuString* %str, i8* %format, ...) #0 {
  %1 = alloca %struct.CuString*, align 8
  %2 = alloca i8*, align 8
  %argp = alloca [1 x %struct.__va_list_tag], align 16
  %buf = alloca [8192 x i8], align 16
  store %struct.CuString* %str, %struct.CuString** %1, align 8
  store i8* %format, i8** %2, align 8
  %3 = getelementptr inbounds [1 x %struct.__va_list_tag]* %argp, i32 0, i32 0
  %4 = bitcast %struct.__va_list_tag* %3 to i8*
  call void @llvm.va_start(i8* %4)
  %5 = getelementptr inbounds [8192 x i8]* %buf, i32 0, i32 0
  %6 = load i8** %2, align 8
  %7 = getelementptr inbounds [1 x %struct.__va_list_tag]* %argp, i32 0, i32 0
  %8 = call i32 @__vsprintf_chk(i8* %5, i32 0, i64 8192, i8* %6, %struct.__va_list_tag* %7)
  %9 = getelementptr inbounds [1 x %struct.__va_list_tag]* %argp, i32 0, i32 0
  %10 = bitcast %struct.__va_list_tag* %9 to i8*
  call void @llvm.va_end(i8* %10)
  %11 = load %struct.CuString** %1, align 8
  %12 = getelementptr inbounds [8192 x i8]* %buf, i32 0, i32 0
  call void @CuStringAppend(%struct.CuString* %11, i8* %12)
  ret void
}

; Function Attrs: nounwind
declare void @llvm.va_start(i8*) #4

declare i32 @__vsprintf_chk(i8*, i32, i64, i8*, %struct.__va_list_tag*) #1

; Function Attrs: nounwind
declare void @llvm.va_end(i8*) #4

; Function Attrs: nounwind ssp uwtable
define void @CuStringInsert(%struct.CuString* %str, i8* %text, i32 %pos) #0 {
  %1 = alloca %struct.CuString*, align 8
  %2 = alloca i8*, align 8
  %3 = alloca i32, align 4
  %length = alloca i32, align 4
  store %struct.CuString* %str, %struct.CuString** %1, align 8
  store i8* %text, i8** %2, align 8
  store i32 %pos, i32* %3, align 4
  %4 = load i8** %2, align 8
  %5 = call i64 @strlen(i8* %4)
  %6 = trunc i64 %5 to i32
  store i32 %6, i32* %length, align 4
  %7 = load i32* %3, align 4
  %8 = load %struct.CuString** %1, align 8
  %9 = getelementptr inbounds %struct.CuString* %8, i32 0, i32 0
  %10 = load i32* %9, align 4
  %11 = icmp sgt i32 %7, %10
  br i1 %11, label %12, label %16

; <label>:12                                      ; preds = %0
  %13 = load %struct.CuString** %1, align 8
  %14 = getelementptr inbounds %struct.CuString* %13, i32 0, i32 0
  %15 = load i32* %14, align 4
  store i32 %15, i32* %3, align 4
  br label %16

; <label>:16                                      ; preds = %12, %0
  %17 = load %struct.CuString** %1, align 8
  %18 = getelementptr inbounds %struct.CuString* %17, i32 0, i32 0
  %19 = load i32* %18, align 4
  %20 = load i32* %length, align 4
  %21 = add nsw i32 %19, %20
  %22 = add nsw i32 %21, 1
  %23 = load %struct.CuString** %1, align 8
  %24 = getelementptr inbounds %struct.CuString* %23, i32 0, i32 1
  %25 = load i32* %24, align 4
  %26 = icmp sge i32 %22, %25
  br i1 %26, label %27, label %36

; <label>:27                                      ; preds = %16
  %28 = load %struct.CuString** %1, align 8
  %29 = load %struct.CuString** %1, align 8
  %30 = getelementptr inbounds %struct.CuString* %29, i32 0, i32 0
  %31 = load i32* %30, align 4
  %32 = load i32* %length, align 4
  %33 = add nsw i32 %31, %32
  %34 = add nsw i32 %33, 1
  %35 = add nsw i32 %34, 256
  call void @CuStringResize(%struct.CuString* %28, i32 %35)
  br label %36

; <label>:36                                      ; preds = %27, %16
  %37 = load %struct.CuString** %1, align 8
  %38 = getelementptr inbounds %struct.CuString* %37, i32 0, i32 2
  %39 = load i8** %38, align 8
  %40 = load i32* %3, align 4
  %41 = sext i32 %40 to i64
  %42 = getelementptr inbounds i8* %39, i64 %41
  %43 = load i32* %length, align 4
  %44 = sext i32 %43 to i64
  %45 = getelementptr inbounds i8* %42, i64 %44
  %46 = load %struct.CuString** %1, align 8
  %47 = getelementptr inbounds %struct.CuString* %46, i32 0, i32 2
  %48 = load i8** %47, align 8
  %49 = load i32* %3, align 4
  %50 = sext i32 %49 to i64
  %51 = getelementptr inbounds i8* %48, i64 %50
  %52 = load %struct.CuString** %1, align 8
  %53 = getelementptr inbounds %struct.CuString* %52, i32 0, i32 0
  %54 = load i32* %53, align 4
  %55 = load i32* %3, align 4
  %56 = sub nsw i32 %54, %55
  %57 = add nsw i32 %56, 1
  %58 = sext i32 %57 to i64
  %59 = load %struct.CuString** %1, align 8
  %60 = getelementptr inbounds %struct.CuString* %59, i32 0, i32 2
  %61 = load i8** %60, align 8
  %62 = load i32* %3, align 4
  %63 = sext i32 %62 to i64
  %64 = getelementptr inbounds i8* %61, i64 %63
  %65 = load i32* %length, align 4
  %66 = sext i32 %65 to i64
  %67 = getelementptr inbounds i8* %64, i64 %66
  %68 = call i64 @llvm.objectsize.i64.p0i8(i8* %67, i1 false)
  %69 = call i8* @__memmove_chk(i8* %45, i8* %51, i64 %58, i64 %68) #4
  %70 = load i32* %length, align 4
  %71 = load %struct.CuString** %1, align 8
  %72 = getelementptr inbounds %struct.CuString* %71, i32 0, i32 0
  %73 = load i32* %72, align 4
  %74 = add nsw i32 %73, %70
  store i32 %74, i32* %72, align 4
  %75 = load %struct.CuString** %1, align 8
  %76 = getelementptr inbounds %struct.CuString* %75, i32 0, i32 2
  %77 = load i8** %76, align 8
  %78 = load i32* %3, align 4
  %79 = sext i32 %78 to i64
  %80 = getelementptr inbounds i8* %77, i64 %79
  %81 = load i8** %2, align 8
  %82 = load i32* %length, align 4
  %83 = sext i32 %82 to i64
  %84 = load %struct.CuString** %1, align 8
  %85 = getelementptr inbounds %struct.CuString* %84, i32 0, i32 2
  %86 = load i8** %85, align 8
  %87 = load i32* %3, align 4
  %88 = sext i32 %87 to i64
  %89 = getelementptr inbounds i8* %86, i64 %88
  %90 = call i64 @llvm.objectsize.i64.p0i8(i8* %89, i1 false)
  %91 = call i8* @__memcpy_chk(i8* %80, i8* %81, i64 %83, i64 %90) #4
  ret void
}

; Function Attrs: nounwind
declare i8* @__memmove_chk(i8*, i8*, i64, i64) #2

; Function Attrs: nounwind
declare i8* @__memcpy_chk(i8*, i8*, i64, i64) #2

; Function Attrs: nounwind ssp uwtable
define void @CuTestInit(%struct.CuTest* %t, i8* %name, void (%struct.CuTest*)* %function) #0 {
  %1 = alloca %struct.CuTest*, align 8
  %2 = alloca i8*, align 8
  %3 = alloca void (%struct.CuTest*)*, align 8
  store %struct.CuTest* %t, %struct.CuTest** %1, align 8
  store i8* %name, i8** %2, align 8
  store void (%struct.CuTest*)* %function, void (%struct.CuTest*)** %3, align 8
  %4 = load i8** %2, align 8
  %5 = call i8* @CuStrCopy(i8* %4)
  %6 = load %struct.CuTest** %1, align 8
  %7 = getelementptr inbounds %struct.CuTest* %6, i32 0, i32 0
  store i8* %5, i8** %7, align 8
  %8 = load %struct.CuTest** %1, align 8
  %9 = getelementptr inbounds %struct.CuTest* %8, i32 0, i32 2
  store i32 0, i32* %9, align 4
  %10 = load %struct.CuTest** %1, align 8
  %11 = getelementptr inbounds %struct.CuTest* %10, i32 0, i32 3
  store i32 0, i32* %11, align 4
  %12 = load %struct.CuTest** %1, align 8
  %13 = getelementptr inbounds %struct.CuTest* %12, i32 0, i32 4
  store i8* null, i8** %13, align 8
  %14 = load void (%struct.CuTest*)** %3, align 8
  %15 = load %struct.CuTest** %1, align 8
  %16 = getelementptr inbounds %struct.CuTest* %15, i32 0, i32 1
  store void (%struct.CuTest*)* %14, void (%struct.CuTest*)** %16, align 8
  %17 = load %struct.CuTest** %1, align 8
  %18 = getelementptr inbounds %struct.CuTest* %17, i32 0, i32 5
  store [37 x i32]* null, [37 x i32]** %18, align 8
  ret void
}

; Function Attrs: nounwind ssp uwtable
define %struct.CuTest* @CuTestNew(i8* %name, void (%struct.CuTest*)* %function) #0 {
  %1 = alloca i8*, align 8
  %2 = alloca void (%struct.CuTest*)*, align 8
  %tc = alloca %struct.CuTest*, align 8
  store i8* %name, i8** %1, align 8
  store void (%struct.CuTest*)* %function, void (%struct.CuTest*)** %2, align 8
  %3 = call i8* @malloc(i64 40)
  %4 = bitcast i8* %3 to %struct.CuTest*
  store %struct.CuTest* %4, %struct.CuTest** %tc, align 8
  %5 = load %struct.CuTest** %tc, align 8
  %6 = load i8** %1, align 8
  %7 = load void (%struct.CuTest*)** %2, align 8
  call void @CuTestInit(%struct.CuTest* %5, i8* %6, void (%struct.CuTest*)* %7)
  %8 = load %struct.CuTest** %tc, align 8
  ret %struct.CuTest* %8
}

; Function Attrs: nounwind ssp uwtable
define void @CuTestDelete(%struct.CuTest* %t) #0 {
  %1 = alloca %struct.CuTest*, align 8
  store %struct.CuTest* %t, %struct.CuTest** %1, align 8
  %2 = load %struct.CuTest** %1, align 8
  %3 = icmp ne %struct.CuTest* %2, null
  br i1 %3, label %5, label %4

; <label>:4                                       ; preds = %0
  br label %11

; <label>:5                                       ; preds = %0
  %6 = load %struct.CuTest** %1, align 8
  %7 = getelementptr inbounds %struct.CuTest* %6, i32 0, i32 0
  %8 = load i8** %7, align 8
  call void @free(i8* %8)
  %9 = load %struct.CuTest** %1, align 8
  %10 = bitcast %struct.CuTest* %9 to i8*
  call void @free(i8* %10)
  br label %11

; <label>:11                                      ; preds = %5, %4
  ret void
}

; Function Attrs: nounwind ssp uwtable
define void @CuTestRun(%struct.CuTest* %tc) #0 {
  %1 = alloca %struct.CuTest*, align 8
  %buf = alloca [37 x i32], align 16
  store %struct.CuTest* %tc, %struct.CuTest** %1, align 8
  %2 = load %struct.CuTest** %1, align 8
  %3 = getelementptr inbounds %struct.CuTest* %2, i32 0, i32 5
  store [37 x i32]* %buf, [37 x i32]** %3, align 8
  %4 = getelementptr inbounds [37 x i32]* %buf, i32 0, i32 0
  %5 = call i32 @setjmp(i32* %4) #8
  %6 = icmp eq i32 %5, 0
  br i1 %6, label %7, label %14

; <label>:7                                       ; preds = %0
  %8 = load %struct.CuTest** %1, align 8
  %9 = getelementptr inbounds %struct.CuTest* %8, i32 0, i32 3
  store i32 1, i32* %9, align 4
  %10 = load %struct.CuTest** %1, align 8
  %11 = getelementptr inbounds %struct.CuTest* %10, i32 0, i32 1
  %12 = load void (%struct.CuTest*)** %11, align 8
  %13 = load %struct.CuTest** %1, align 8
  call void %12(%struct.CuTest* %13)
  br label %14

; <label>:14                                      ; preds = %7, %0
  %15 = load %struct.CuTest** %1, align 8
  %16 = getelementptr inbounds %struct.CuTest* %15, i32 0, i32 5
  store [37 x i32]* null, [37 x i32]** %16, align 8
  ret void
}

; Function Attrs: returns_twice
declare i32 @setjmp(i32*) #5

; Function Attrs: nounwind ssp uwtable
define void @CuFail_Line(%struct.CuTest* %tc, i8* %file, i32 %line, i8* %message2, i8* %message) #0 {
  %1 = alloca %struct.CuTest*, align 8
  %2 = alloca i8*, align 8
  %3 = alloca i32, align 4
  %4 = alloca i8*, align 8
  %5 = alloca i8*, align 8
  %string = alloca %struct.CuString, align 8
  store %struct.CuTest* %tc, %struct.CuTest** %1, align 8
  store i8* %file, i8** %2, align 8
  store i32 %line, i32* %3, align 4
  store i8* %message2, i8** %4, align 8
  store i8* %message, i8** %5, align 8
  call void @CuStringInit(%struct.CuString* %string)
  %6 = load i8** %4, align 8
  %7 = icmp ne i8* %6, null
  br i1 %7, label %8, label %10

; <label>:8                                       ; preds = %0
  %9 = load i8** %4, align 8
  call void @CuStringAppend(%struct.CuString* %string, i8* %9)
  call void @CuStringAppend(%struct.CuString* %string, i8* getelementptr inbounds ([3 x i8]* @.str1, i32 0, i32 0))
  br label %10

; <label>:10                                      ; preds = %8, %0
  %11 = load i8** %5, align 8
  call void @CuStringAppend(%struct.CuString* %string, i8* %11)
  %12 = load %struct.CuTest** %1, align 8
  %13 = load i8** %2, align 8
  %14 = load i32* %3, align 4
  call void @CuFailInternal(%struct.CuTest* %12, i8* %13, i32 %14, %struct.CuString* %string)
  ret void
}

; Function Attrs: nounwind ssp uwtable
define internal void @CuFailInternal(%struct.CuTest* %tc, i8* %file, i32 %line, %struct.CuString* %string) #0 {
  %1 = alloca %struct.CuTest*, align 8
  %2 = alloca i8*, align 8
  %3 = alloca i32, align 4
  %4 = alloca %struct.CuString*, align 8
  %buf = alloca [8192 x i8], align 16
  store %struct.CuTest* %tc, %struct.CuTest** %1, align 8
  store i8* %file, i8** %2, align 8
  store i32 %line, i32* %3, align 4
  store %struct.CuString* %string, %struct.CuString** %4, align 8
  %5 = getelementptr inbounds [8192 x i8]* %buf, i32 0, i32 0
  %6 = load i8** %2, align 8
  %7 = load i32* %3, align 4
  %8 = call i32 (i8*, i32, i64, i8*, ...)* @__sprintf_chk(i8* %5, i32 0, i64 8192, i8* getelementptr inbounds ([8 x i8]* @.str23, i32 0, i32 0), i8* %6, i32 %7)
  %9 = load %struct.CuString** %4, align 8
  %10 = getelementptr inbounds [8192 x i8]* %buf, i32 0, i32 0
  call void @CuStringInsert(%struct.CuString* %9, i8* %10, i32 0)
  %11 = load %struct.CuTest** %1, align 8
  %12 = getelementptr inbounds %struct.CuTest* %11, i32 0, i32 2
  store i32 1, i32* %12, align 4
  %13 = load %struct.CuString** %4, align 8
  %14 = getelementptr inbounds %struct.CuString* %13, i32 0, i32 2
  %15 = load i8** %14, align 8
  %16 = load %struct.CuTest** %1, align 8
  %17 = getelementptr inbounds %struct.CuTest* %16, i32 0, i32 4
  store i8* %15, i8** %17, align 8
  %18 = load %struct.CuTest** %1, align 8
  %19 = getelementptr inbounds %struct.CuTest* %18, i32 0, i32 5
  %20 = load [37 x i32]** %19, align 8
  %21 = icmp ne [37 x i32]* %20, null
  br i1 %21, label %22, label %27

; <label>:22                                      ; preds = %0
  %23 = load %struct.CuTest** %1, align 8
  %24 = getelementptr inbounds %struct.CuTest* %23, i32 0, i32 5
  %25 = load [37 x i32]** %24, align 8
  %26 = getelementptr inbounds [37 x i32]* %25, i32 0, i32 0
  call void @longjmp(i32* %26, i32 0) #9
  unreachable

; <label>:27                                      ; preds = %0
  ret void
}

; Function Attrs: nounwind ssp uwtable
define void @CuAssert_Line(%struct.CuTest* %tc, i8* %file, i32 %line, i8* %message, i32 %condition) #0 {
  %1 = alloca %struct.CuTest*, align 8
  %2 = alloca i8*, align 8
  %3 = alloca i32, align 4
  %4 = alloca i8*, align 8
  %5 = alloca i32, align 4
  store %struct.CuTest* %tc, %struct.CuTest** %1, align 8
  store i8* %file, i8** %2, align 8
  store i32 %line, i32* %3, align 4
  store i8* %message, i8** %4, align 8
  store i32 %condition, i32* %5, align 4
  %6 = load i32* %5, align 4
  %7 = icmp ne i32 %6, 0
  br i1 %7, label %8, label %9

; <label>:8                                       ; preds = %0
  br label %14

; <label>:9                                       ; preds = %0
  %10 = load %struct.CuTest** %1, align 8
  %11 = load i8** %2, align 8
  %12 = load i32* %3, align 4
  %13 = load i8** %4, align 8
  call void @CuFail_Line(%struct.CuTest* %10, i8* %11, i32 %12, i8* null, i8* %13)
  br label %14

; <label>:14                                      ; preds = %9, %8
  ret void
}

; Function Attrs: nounwind ssp uwtable
define void @CuAssertStrEquals_LineMsg(%struct.CuTest* %tc, i8* %file, i32 %line, i8* %message, i8* %expected, i8* %actual) #0 {
  %1 = alloca %struct.CuTest*, align 8
  %2 = alloca i8*, align 8
  %3 = alloca i32, align 4
  %4 = alloca i8*, align 8
  %5 = alloca i8*, align 8
  %6 = alloca i8*, align 8
  %string = alloca %struct.CuString, align 8
  store %struct.CuTest* %tc, %struct.CuTest** %1, align 8
  store i8* %file, i8** %2, align 8
  store i32 %line, i32* %3, align 4
  store i8* %message, i8** %4, align 8
  store i8* %expected, i8** %5, align 8
  store i8* %actual, i8** %6, align 8
  %7 = load i8** %5, align 8
  %8 = icmp eq i8* %7, null
  br i1 %8, label %9, label %12

; <label>:9                                       ; preds = %0
  %10 = load i8** %6, align 8
  %11 = icmp eq i8* %10, null
  br i1 %11, label %23, label %12

; <label>:12                                      ; preds = %9, %0
  %13 = load i8** %5, align 8
  %14 = icmp ne i8* %13, null
  br i1 %14, label %15, label %24

; <label>:15                                      ; preds = %12
  %16 = load i8** %6, align 8
  %17 = icmp ne i8* %16, null
  br i1 %17, label %18, label %24

; <label>:18                                      ; preds = %15
  %19 = load i8** %5, align 8
  %20 = load i8** %6, align 8
  %21 = call i32 @strcmp(i8* %19, i8* %20)
  %22 = icmp eq i32 %21, 0
  br i1 %22, label %23, label %24

; <label>:23                                      ; preds = %18, %9
  br label %35

; <label>:24                                      ; preds = %18, %15, %12
  call void @CuStringInit(%struct.CuString* %string)
  %25 = load i8** %4, align 8
  %26 = icmp ne i8* %25, null
  br i1 %26, label %27, label %29

; <label>:27                                      ; preds = %24
  %28 = load i8** %4, align 8
  call void @CuStringAppend(%struct.CuString* %string, i8* %28)
  call void @CuStringAppend(%struct.CuString* %string, i8* getelementptr inbounds ([3 x i8]* @.str1, i32 0, i32 0))
  br label %29

; <label>:29                                      ; preds = %27, %24
  call void @CuStringAppend(%struct.CuString* %string, i8* getelementptr inbounds ([11 x i8]* @.str2, i32 0, i32 0))
  %30 = load i8** %5, align 8
  call void @CuStringAppend(%struct.CuString* %string, i8* %30)
  call void @CuStringAppend(%struct.CuString* %string, i8* getelementptr inbounds ([12 x i8]* @.str3, i32 0, i32 0))
  %31 = load i8** %6, align 8
  call void @CuStringAppend(%struct.CuString* %string, i8* %31)
  call void @CuStringAppend(%struct.CuString* %string, i8* getelementptr inbounds ([2 x i8]* @.str4, i32 0, i32 0))
  %32 = load %struct.CuTest** %1, align 8
  %33 = load i8** %2, align 8
  %34 = load i32* %3, align 4
  call void @CuFailInternal(%struct.CuTest* %32, i8* %33, i32 %34, %struct.CuString* %string)
  br label %35

; <label>:35                                      ; preds = %29, %23
  ret void
}

declare i32 @strcmp(i8*, i8*) #1

; Function Attrs: nounwind ssp uwtable
define void @CuAssertIntEquals_LineMsg(%struct.CuTest* %tc, i8* %file, i32 %line, i8* %message, i32 %expected, i32 %actual) #0 {
  %1 = alloca %struct.CuTest*, align 8
  %2 = alloca i8*, align 8
  %3 = alloca i32, align 4
  %4 = alloca i8*, align 8
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  %buf = alloca [256 x i8], align 16
  store %struct.CuTest* %tc, %struct.CuTest** %1, align 8
  store i8* %file, i8** %2, align 8
  store i32 %line, i32* %3, align 4
  store i8* %message, i8** %4, align 8
  store i32 %expected, i32* %5, align 4
  store i32 %actual, i32* %6, align 4
  %7 = load i32* %5, align 4
  %8 = load i32* %6, align 4
  %9 = icmp eq i32 %7, %8
  br i1 %9, label %10, label %11

; <label>:10                                      ; preds = %0
  br label %21

; <label>:11                                      ; preds = %0
  %12 = getelementptr inbounds [256 x i8]* %buf, i32 0, i32 0
  %13 = load i32* %5, align 4
  %14 = load i32* %6, align 4
  %15 = call i32 (i8*, i32, i64, i8*, ...)* @__sprintf_chk(i8* %12, i32 0, i64 256, i8* getelementptr inbounds ([27 x i8]* @.str5, i32 0, i32 0), i32 %13, i32 %14)
  %16 = load %struct.CuTest** %1, align 8
  %17 = load i8** %2, align 8
  %18 = load i32* %3, align 4
  %19 = load i8** %4, align 8
  %20 = getelementptr inbounds [256 x i8]* %buf, i32 0, i32 0
  call void @CuFail_Line(%struct.CuTest* %16, i8* %17, i32 %18, i8* %19, i8* %20)
  br label %21

; <label>:21                                      ; preds = %11, %10
  ret void
}

declare i32 @__sprintf_chk(i8*, i32, i64, i8*, ...) #1

; Function Attrs: nounwind ssp uwtable
define void @CuAssertDblEquals_LineMsg(%struct.CuTest* %tc, i8* %file, i32 %line, i8* %message, double %expected, double %actual, double %delta) #0 {
  %1 = alloca %struct.CuTest*, align 8
  %2 = alloca i8*, align 8
  %3 = alloca i32, align 4
  %4 = alloca i8*, align 8
  %5 = alloca double, align 8
  %6 = alloca double, align 8
  %7 = alloca double, align 8
  %buf = alloca [256 x i8], align 16
  store %struct.CuTest* %tc, %struct.CuTest** %1, align 8
  store i8* %file, i8** %2, align 8
  store i32 %line, i32* %3, align 4
  store i8* %message, i8** %4, align 8
  store double %expected, double* %5, align 8
  store double %actual, double* %6, align 8
  store double %delta, double* %7, align 8
  %8 = load double* %5, align 8
  %9 = load double* %6, align 8
  %10 = fsub double %8, %9
  %11 = call double @fabs(double %10) #3
  %12 = load double* %7, align 8
  %13 = fcmp ole double %11, %12
  br i1 %13, label %14, label %15

; <label>:14                                      ; preds = %0
  br label %25

; <label>:15                                      ; preds = %0
  %16 = getelementptr inbounds [256 x i8]* %buf, i32 0, i32 0
  %17 = load double* %5, align 8
  %18 = load double* %6, align 8
  %19 = call i32 (i8*, i32, i64, i8*, ...)* @__sprintf_chk(i8* %16, i32 0, i64 256, i8* getelementptr inbounds ([27 x i8]* @.str6, i32 0, i32 0), double %17, double %18)
  %20 = load %struct.CuTest** %1, align 8
  %21 = load i8** %2, align 8
  %22 = load i32* %3, align 4
  %23 = load i8** %4, align 8
  %24 = getelementptr inbounds [256 x i8]* %buf, i32 0, i32 0
  call void @CuFail_Line(%struct.CuTest* %20, i8* %21, i32 %22, i8* %23, i8* %24)
  br label %25

; <label>:25                                      ; preds = %15, %14
  ret void
}

; Function Attrs: nounwind readnone
declare double @fabs(double) #6

; Function Attrs: nounwind ssp uwtable
define void @CuAssertPtrEquals_LineMsg(%struct.CuTest* %tc, i8* %file, i32 %line, i8* %message, i8* %expected, i8* %actual) #0 {
  %1 = alloca %struct.CuTest*, align 8
  %2 = alloca i8*, align 8
  %3 = alloca i32, align 4
  %4 = alloca i8*, align 8
  %5 = alloca i8*, align 8
  %6 = alloca i8*, align 8
  %buf = alloca [256 x i8], align 16
  store %struct.CuTest* %tc, %struct.CuTest** %1, align 8
  store i8* %file, i8** %2, align 8
  store i32 %line, i32* %3, align 4
  store i8* %message, i8** %4, align 8
  store i8* %expected, i8** %5, align 8
  store i8* %actual, i8** %6, align 8
  %7 = load i8** %5, align 8
  %8 = load i8** %6, align 8
  %9 = icmp eq i8* %7, %8
  br i1 %9, label %10, label %11

; <label>:10                                      ; preds = %0
  br label %21

; <label>:11                                      ; preds = %0
  %12 = getelementptr inbounds [256 x i8]* %buf, i32 0, i32 0
  %13 = load i8** %5, align 8
  %14 = load i8** %6, align 8
  %15 = call i32 (i8*, i32, i64, i8*, ...)* @__sprintf_chk(i8* %12, i32 0, i64 256, i8* getelementptr inbounds ([39 x i8]* @.str7, i32 0, i32 0), i8* %13, i8* %14)
  %16 = load %struct.CuTest** %1, align 8
  %17 = load i8** %2, align 8
  %18 = load i32* %3, align 4
  %19 = load i8** %4, align 8
  %20 = getelementptr inbounds [256 x i8]* %buf, i32 0, i32 0
  call void @CuFail_Line(%struct.CuTest* %16, i8* %17, i32 %18, i8* %19, i8* %20)
  br label %21

; <label>:21                                      ; preds = %11, %10
  ret void
}

; Function Attrs: nounwind ssp uwtable
define void @CuSuiteInit(%struct.CuSuite* %testSuite) #0 {
  %1 = alloca %struct.CuSuite*, align 8
  store %struct.CuSuite* %testSuite, %struct.CuSuite** %1, align 8
  %2 = load %struct.CuSuite** %1, align 8
  %3 = getelementptr inbounds %struct.CuSuite* %2, i32 0, i32 0
  store i32 0, i32* %3, align 4
  %4 = load %struct.CuSuite** %1, align 8
  %5 = getelementptr inbounds %struct.CuSuite* %4, i32 0, i32 2
  store i32 0, i32* %5, align 4
  %6 = load %struct.CuSuite** %1, align 8
  %7 = getelementptr inbounds %struct.CuSuite* %6, i32 0, i32 1
  %8 = getelementptr inbounds [1024 x %struct.CuTest*]* %7, i32 0, i32 0
  %9 = bitcast %struct.CuTest** %8 to i8*
  %10 = load %struct.CuSuite** %1, align 8
  %11 = getelementptr inbounds %struct.CuSuite* %10, i32 0, i32 1
  %12 = getelementptr inbounds [1024 x %struct.CuTest*]* %11, i32 0, i32 0
  %13 = bitcast %struct.CuTest** %12 to i8*
  %14 = call i64 @llvm.objectsize.i64.p0i8(i8* %13, i1 false)
  %15 = call i8* @__memset_chk(i8* %9, i32 0, i64 8192, i64 %14) #4
  ret void
}

; Function Attrs: nounwind
declare i8* @__memset_chk(i8*, i32, i64, i64) #2

; Function Attrs: nounwind ssp uwtable
define %struct.CuSuite* @CuSuiteNew() #0 {
  %testSuite = alloca %struct.CuSuite*, align 8
  %1 = call i8* @malloc(i64 8208)
  %2 = bitcast i8* %1 to %struct.CuSuite*
  store %struct.CuSuite* %2, %struct.CuSuite** %testSuite, align 8
  %3 = load %struct.CuSuite** %testSuite, align 8
  call void @CuSuiteInit(%struct.CuSuite* %3)
  %4 = load %struct.CuSuite** %testSuite, align 8
  ret %struct.CuSuite* %4
}

; Function Attrs: nounwind ssp uwtable
define void @CuSuiteDelete(%struct.CuSuite* %testSuite) #0 {
  %1 = alloca %struct.CuSuite*, align 8
  %n = alloca i32, align 4
  store %struct.CuSuite* %testSuite, %struct.CuSuite** %1, align 8
  store i32 0, i32* %n, align 4
  br label %2

; <label>:2                                       ; preds = %21, %0
  %3 = load i32* %n, align 4
  %4 = icmp ult i32 %3, 1024
  br i1 %4, label %5, label %24

; <label>:5                                       ; preds = %2
  %6 = load i32* %n, align 4
  %7 = zext i32 %6 to i64
  %8 = load %struct.CuSuite** %1, align 8
  %9 = getelementptr inbounds %struct.CuSuite* %8, i32 0, i32 1
  %10 = getelementptr inbounds [1024 x %struct.CuTest*]* %9, i32 0, i64 %7
  %11 = load %struct.CuTest** %10, align 8
  %12 = icmp ne %struct.CuTest* %11, null
  br i1 %12, label %13, label %20

; <label>:13                                      ; preds = %5
  %14 = load i32* %n, align 4
  %15 = zext i32 %14 to i64
  %16 = load %struct.CuSuite** %1, align 8
  %17 = getelementptr inbounds %struct.CuSuite* %16, i32 0, i32 1
  %18 = getelementptr inbounds [1024 x %struct.CuTest*]* %17, i32 0, i64 %15
  %19 = load %struct.CuTest** %18, align 8
  call void @CuTestDelete(%struct.CuTest* %19)
  br label %20

; <label>:20                                      ; preds = %13, %5
  br label %21

; <label>:21                                      ; preds = %20
  %22 = load i32* %n, align 4
  %23 = add i32 %22, 1
  store i32 %23, i32* %n, align 4
  br label %2

; <label>:24                                      ; preds = %2
  %25 = load %struct.CuSuite** %1, align 8
  %26 = bitcast %struct.CuSuite* %25 to i8*
  call void @free(i8* %26)
  ret void
}

; Function Attrs: nounwind ssp uwtable
define void @CuSuiteAdd(%struct.CuSuite* %testSuite, %struct.CuTest* %testCase) #0 {
  %1 = alloca %struct.CuSuite*, align 8
  %2 = alloca %struct.CuTest*, align 8
  store %struct.CuSuite* %testSuite, %struct.CuSuite** %1, align 8
  store %struct.CuTest* %testCase, %struct.CuTest** %2, align 8
  %3 = load %struct.CuSuite** %1, align 8
  %4 = getelementptr inbounds %struct.CuSuite* %3, i32 0, i32 0
  %5 = load i32* %4, align 4
  %6 = icmp slt i32 %5, 1024
  %7 = xor i1 %6, true
  %8 = zext i1 %7 to i32
  %9 = sext i32 %8 to i64
  %10 = call i64 @llvm.expect.i64(i64 %9, i64 0)
  %11 = icmp ne i64 %10, 0
  br i1 %11, label %12, label %14

; <label>:12                                      ; preds = %0
  call void @__assert_rtn(i8* getelementptr inbounds ([11 x i8]* @__func__.CuSuiteAdd, i32 0, i32 0), i8* getelementptr inbounds ([9 x i8]* @.str8, i32 0, i32 0), i32 268, i8* getelementptr inbounds ([34 x i8]* @.str9, i32 0, i32 0)) #9
  unreachable
                                                  ; No predecessors!
  br label %15

; <label>:14                                      ; preds = %0
  br label %15

; <label>:15                                      ; preds = %14, %13
  %16 = load %struct.CuTest** %2, align 8
  %17 = load %struct.CuSuite** %1, align 8
  %18 = getelementptr inbounds %struct.CuSuite* %17, i32 0, i32 0
  %19 = load i32* %18, align 4
  %20 = sext i32 %19 to i64
  %21 = load %struct.CuSuite** %1, align 8
  %22 = getelementptr inbounds %struct.CuSuite* %21, i32 0, i32 1
  %23 = getelementptr inbounds [1024 x %struct.CuTest*]* %22, i32 0, i64 %20
  store %struct.CuTest* %16, %struct.CuTest** %23, align 8
  %24 = load %struct.CuSuite** %1, align 8
  %25 = getelementptr inbounds %struct.CuSuite* %24, i32 0, i32 0
  %26 = load i32* %25, align 4
  %27 = add nsw i32 %26, 1
  store i32 %27, i32* %25, align 4
  ret void
}

; Function Attrs: nounwind readnone
declare i64 @llvm.expect.i64(i64, i64) #3

; Function Attrs: noreturn
declare void @__assert_rtn(i8*, i8*, i32, i8*) #7

; Function Attrs: nounwind ssp uwtable
define void @CuSuiteAddSuite(%struct.CuSuite* %testSuite, %struct.CuSuite* %testSuite2) #0 {
  %1 = alloca %struct.CuSuite*, align 8
  %2 = alloca %struct.CuSuite*, align 8
  %i = alloca i32, align 4
  %testCase = alloca %struct.CuTest*, align 8
  store %struct.CuSuite* %testSuite, %struct.CuSuite** %1, align 8
  store %struct.CuSuite* %testSuite2, %struct.CuSuite** %2, align 8
  store i32 0, i32* %i, align 4
  br label %3

; <label>:3                                       ; preds = %18, %0
  %4 = load i32* %i, align 4
  %5 = load %struct.CuSuite** %2, align 8
  %6 = getelementptr inbounds %struct.CuSuite* %5, i32 0, i32 0
  %7 = load i32* %6, align 4
  %8 = icmp slt i32 %4, %7
  br i1 %8, label %9, label %21

; <label>:9                                       ; preds = %3
  %10 = load i32* %i, align 4
  %11 = sext i32 %10 to i64
  %12 = load %struct.CuSuite** %2, align 8
  %13 = getelementptr inbounds %struct.CuSuite* %12, i32 0, i32 1
  %14 = getelementptr inbounds [1024 x %struct.CuTest*]* %13, i32 0, i64 %11
  %15 = load %struct.CuTest** %14, align 8
  store %struct.CuTest* %15, %struct.CuTest** %testCase, align 8
  %16 = load %struct.CuSuite** %1, align 8
  %17 = load %struct.CuTest** %testCase, align 8
  call void @CuSuiteAdd(%struct.CuSuite* %16, %struct.CuTest* %17)
  br label %18

; <label>:18                                      ; preds = %9
  %19 = load i32* %i, align 4
  %20 = add nsw i32 %19, 1
  store i32 %20, i32* %i, align 4
  br label %3

; <label>:21                                      ; preds = %3
  ret void
}

; Function Attrs: nounwind ssp uwtable
define void @CuSuiteRun(%struct.CuSuite* %testSuite) #0 {
  %1 = alloca %struct.CuSuite*, align 8
  %i = alloca i32, align 4
  %testCase = alloca %struct.CuTest*, align 8
  store %struct.CuSuite* %testSuite, %struct.CuSuite** %1, align 8
  store i32 0, i32* %i, align 4
  br label %2

; <label>:2                                       ; preds = %26, %0
  %3 = load i32* %i, align 4
  %4 = load %struct.CuSuite** %1, align 8
  %5 = getelementptr inbounds %struct.CuSuite* %4, i32 0, i32 0
  %6 = load i32* %5, align 4
  %7 = icmp slt i32 %3, %6
  br i1 %7, label %8, label %29

; <label>:8                                       ; preds = %2
  %9 = load i32* %i, align 4
  %10 = sext i32 %9 to i64
  %11 = load %struct.CuSuite** %1, align 8
  %12 = getelementptr inbounds %struct.CuSuite* %11, i32 0, i32 1
  %13 = getelementptr inbounds [1024 x %struct.CuTest*]* %12, i32 0, i64 %10
  %14 = load %struct.CuTest** %13, align 8
  store %struct.CuTest* %14, %struct.CuTest** %testCase, align 8
  %15 = load %struct.CuTest** %testCase, align 8
  call void @CuTestRun(%struct.CuTest* %15)
  %16 = load %struct.CuTest** %testCase, align 8
  %17 = getelementptr inbounds %struct.CuTest* %16, i32 0, i32 2
  %18 = load i32* %17, align 4
  %19 = icmp ne i32 %18, 0
  br i1 %19, label %20, label %25

; <label>:20                                      ; preds = %8
  %21 = load %struct.CuSuite** %1, align 8
  %22 = getelementptr inbounds %struct.CuSuite* %21, i32 0, i32 2
  %23 = load i32* %22, align 4
  %24 = add nsw i32 %23, 1
  store i32 %24, i32* %22, align 4
  br label %25

; <label>:25                                      ; preds = %20, %8
  br label %26

; <label>:26                                      ; preds = %25
  %27 = load i32* %i, align 4
  %28 = add nsw i32 %27, 1
  store i32 %28, i32* %i, align 4
  br label %2

; <label>:29                                      ; preds = %2
  ret void
}

; Function Attrs: nounwind ssp uwtable
define void @CuSuiteSummary(%struct.CuSuite* %testSuite, %struct.CuString* %summary) #0 {
  %1 = alloca %struct.CuSuite*, align 8
  %2 = alloca %struct.CuString*, align 8
  %i = alloca i32, align 4
  %testCase = alloca %struct.CuTest*, align 8
  store %struct.CuSuite* %testSuite, %struct.CuSuite** %1, align 8
  store %struct.CuString* %summary, %struct.CuString** %2, align 8
  store i32 0, i32* %i, align 4
  br label %3

; <label>:3                                       ; preds = %22, %0
  %4 = load i32* %i, align 4
  %5 = load %struct.CuSuite** %1, align 8
  %6 = getelementptr inbounds %struct.CuSuite* %5, i32 0, i32 0
  %7 = load i32* %6, align 4
  %8 = icmp slt i32 %4, %7
  br i1 %8, label %9, label %25

; <label>:9                                       ; preds = %3
  %10 = load i32* %i, align 4
  %11 = sext i32 %10 to i64
  %12 = load %struct.CuSuite** %1, align 8
  %13 = getelementptr inbounds %struct.CuSuite* %12, i32 0, i32 1
  %14 = getelementptr inbounds [1024 x %struct.CuTest*]* %13, i32 0, i64 %11
  %15 = load %struct.CuTest** %14, align 8
  store %struct.CuTest* %15, %struct.CuTest** %testCase, align 8
  %16 = load %struct.CuString** %2, align 8
  %17 = load %struct.CuTest** %testCase, align 8
  %18 = getelementptr inbounds %struct.CuTest* %17, i32 0, i32 2
  %19 = load i32* %18, align 4
  %20 = icmp ne i32 %19, 0
  %21 = select i1 %20, i8* getelementptr inbounds ([2 x i8]* @.str10, i32 0, i32 0), i8* getelementptr inbounds ([2 x i8]* @.str11, i32 0, i32 0)
  call void @CuStringAppend(%struct.CuString* %16, i8* %21)
  br label %22

; <label>:22                                      ; preds = %9
  %23 = load i32* %i, align 4
  %24 = add nsw i32 %23, 1
  store i32 %24, i32* %i, align 4
  br label %3

; <label>:25                                      ; preds = %3
  %26 = load %struct.CuString** %2, align 8
  call void @CuStringAppend(%struct.CuString* %26, i8* getelementptr inbounds ([3 x i8]* @.str12, i32 0, i32 0))
  ret void
}

; Function Attrs: nounwind ssp uwtable
define void @CuSuiteDetails(%struct.CuSuite* %testSuite, %struct.CuString* %details) #0 {
  %1 = alloca %struct.CuSuite*, align 8
  %2 = alloca %struct.CuString*, align 8
  %i = alloca i32, align 4
  %failCount = alloca i32, align 4
  %passCount = alloca i32, align 4
  %testWord = alloca i8*, align 8
  %testCase = alloca %struct.CuTest*, align 8
  store %struct.CuSuite* %testSuite, %struct.CuSuite** %1, align 8
  store %struct.CuString* %details, %struct.CuString** %2, align 8
  store i32 0, i32* %failCount, align 4
  %3 = load %struct.CuSuite** %1, align 8
  %4 = getelementptr inbounds %struct.CuSuite* %3, i32 0, i32 2
  %5 = load i32* %4, align 4
  %6 = icmp eq i32 %5, 0
  br i1 %6, label %7, label %21

; <label>:7                                       ; preds = %0
  %8 = load %struct.CuSuite** %1, align 8
  %9 = getelementptr inbounds %struct.CuSuite* %8, i32 0, i32 0
  %10 = load i32* %9, align 4
  %11 = load %struct.CuSuite** %1, align 8
  %12 = getelementptr inbounds %struct.CuSuite* %11, i32 0, i32 2
  %13 = load i32* %12, align 4
  %14 = sub nsw i32 %10, %13
  store i32 %14, i32* %passCount, align 4
  %15 = load i32* %passCount, align 4
  %16 = icmp eq i32 %15, 1
  %17 = select i1 %16, i8* getelementptr inbounds ([5 x i8]* @.str13, i32 0, i32 0), i8* getelementptr inbounds ([6 x i8]* @.str14, i32 0, i32 0)
  store i8* %17, i8** %testWord, align 8
  %18 = load %struct.CuString** %2, align 8
  %19 = load i32* %passCount, align 4
  %20 = load i8** %testWord, align 8
  call void (%struct.CuString*, i8*, ...)* @CuStringAppendFormat(%struct.CuString* %18, i8* getelementptr inbounds ([12 x i8]* @.str15, i32 0, i32 0), i32 %19, i8* %20)
  br label %84

; <label>:21                                      ; preds = %0
  %22 = load %struct.CuSuite** %1, align 8
  %23 = getelementptr inbounds %struct.CuSuite* %22, i32 0, i32 2
  %24 = load i32* %23, align 4
  %25 = icmp eq i32 %24, 1
  br i1 %25, label %26, label %28

; <label>:26                                      ; preds = %21
  %27 = load %struct.CuString** %2, align 8
  call void @CuStringAppend(%struct.CuString* %27, i8* getelementptr inbounds ([22 x i8]* @.str16, i32 0, i32 0))
  br label %33

; <label>:28                                      ; preds = %21
  %29 = load %struct.CuString** %2, align 8
  %30 = load %struct.CuSuite** %1, align 8
  %31 = getelementptr inbounds %struct.CuSuite* %30, i32 0, i32 2
  %32 = load i32* %31, align 4
  call void (%struct.CuString*, i8*, ...)* @CuStringAppendFormat(%struct.CuString* %29, i8* getelementptr inbounds ([25 x i8]* @.str17, i32 0, i32 0), i32 %32)
  br label %33

; <label>:33                                      ; preds = %28, %26
  store i32 0, i32* %i, align 4
  br label %34

; <label>:34                                      ; preds = %63, %33
  %35 = load i32* %i, align 4
  %36 = load %struct.CuSuite** %1, align 8
  %37 = getelementptr inbounds %struct.CuSuite* %36, i32 0, i32 0
  %38 = load i32* %37, align 4
  %39 = icmp slt i32 %35, %38
  br i1 %39, label %40, label %66

; <label>:40                                      ; preds = %34
  %41 = load i32* %i, align 4
  %42 = sext i32 %41 to i64
  %43 = load %struct.CuSuite** %1, align 8
  %44 = getelementptr inbounds %struct.CuSuite* %43, i32 0, i32 1
  %45 = getelementptr inbounds [1024 x %struct.CuTest*]* %44, i32 0, i64 %42
  %46 = load %struct.CuTest** %45, align 8
  store %struct.CuTest* %46, %struct.CuTest** %testCase, align 8
  %47 = load %struct.CuTest** %testCase, align 8
  %48 = getelementptr inbounds %struct.CuTest* %47, i32 0, i32 2
  %49 = load i32* %48, align 4
  %50 = icmp ne i32 %49, 0
  br i1 %50, label %51, label %62

; <label>:51                                      ; preds = %40
  %52 = load i32* %failCount, align 4
  %53 = add nsw i32 %52, 1
  store i32 %53, i32* %failCount, align 4
  %54 = load %struct.CuString** %2, align 8
  %55 = load i32* %failCount, align 4
  %56 = load %struct.CuTest** %testCase, align 8
  %57 = getelementptr inbounds %struct.CuTest* %56, i32 0, i32 0
  %58 = load i8** %57, align 8
  %59 = load %struct.CuTest** %testCase, align 8
  %60 = getelementptr inbounds %struct.CuTest* %59, i32 0, i32 4
  %61 = load i8** %60, align 8
  call void (%struct.CuString*, i8*, ...)* @CuStringAppendFormat(%struct.CuString* %54, i8* getelementptr inbounds ([12 x i8]* @.str18, i32 0, i32 0), i32 %55, i8* %58, i8* %61)
  br label %62

; <label>:62                                      ; preds = %51, %40
  br label %63

; <label>:63                                      ; preds = %62
  %64 = load i32* %i, align 4
  %65 = add nsw i32 %64, 1
  store i32 %65, i32* %i, align 4
  br label %34

; <label>:66                                      ; preds = %34
  %67 = load %struct.CuString** %2, align 8
  call void @CuStringAppend(%struct.CuString* %67, i8* getelementptr inbounds ([17 x i8]* @.str19, i32 0, i32 0))
  %68 = load %struct.CuString** %2, align 8
  %69 = load %struct.CuSuite** %1, align 8
  %70 = getelementptr inbounds %struct.CuSuite* %69, i32 0, i32 0
  %71 = load i32* %70, align 4
  call void (%struct.CuString*, i8*, ...)* @CuStringAppendFormat(%struct.CuString* %68, i8* getelementptr inbounds ([10 x i8]* @.str20, i32 0, i32 0), i32 %71)
  %72 = load %struct.CuString** %2, align 8
  %73 = load %struct.CuSuite** %1, align 8
  %74 = getelementptr inbounds %struct.CuSuite* %73, i32 0, i32 0
  %75 = load i32* %74, align 4
  %76 = load %struct.CuSuite** %1, align 8
  %77 = getelementptr inbounds %struct.CuSuite* %76, i32 0, i32 2
  %78 = load i32* %77, align 4
  %79 = sub nsw i32 %75, %78
  call void (%struct.CuString*, i8*, ...)* @CuStringAppendFormat(%struct.CuString* %72, i8* getelementptr inbounds ([12 x i8]* @.str21, i32 0, i32 0), i32 %79)
  %80 = load %struct.CuString** %2, align 8
  %81 = load %struct.CuSuite** %1, align 8
  %82 = getelementptr inbounds %struct.CuSuite* %81, i32 0, i32 2
  %83 = load i32* %82, align 4
  call void (%struct.CuString*, i8*, ...)* @CuStringAppendFormat(%struct.CuString* %80, i8* getelementptr inbounds ([11 x i8]* @.str22, i32 0, i32 0), i32 %83)
  br label %84

; <label>:84                                      ; preds = %66, %7
  ret void
}

; Function Attrs: noreturn
declare void @longjmp(i32*, i32) #7

attributes #0 = { nounwind ssp uwtable "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { nounwind "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { nounwind readnone }
attributes #4 = { nounwind }
attributes #5 = { returns_twice "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #6 = { nounwind readnone "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #7 = { noreturn "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #8 = { returns_twice }
attributes #9 = { noreturn }

!llvm.ident = !{!0}

!0 = metadata !{metadata !"Apple LLVM version 5.1 (clang-503.0.40) (based on LLVM 3.4svn)"}
