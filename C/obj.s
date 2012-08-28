; ModuleID = 'obj.c'
target datalayout = "e-p:64:64:64-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:64:64-f32:32:32-f64:64:64-v64:64:64-v128:128:128-a0:0:64-s0:64:64-f80:128:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.7.4"

%struct.impl1 = type { i32, i32, i8 }
%struct.impl2 = type { i32, %struct.impl1*, %struct.impl1* }

@impl1_anonymous = common global %struct.impl1* null, align 8
@impl2_anonymous = common global %struct.impl2* null, align 8

define void @op1(%struct.impl1* %a) nounwind uwtable ssp {
  %1 = alloca %struct.impl1*, align 8
  store %struct.impl1* %a, %struct.impl1** %1, align 8
  %2 = load %struct.impl1** %1, align 8
  %3 = getelementptr inbounds %struct.impl1* %2, i32 0, i32 0
  %4 = load i32* %3, align 4
  %5 = add nsw i32 %4, 1
  %6 = load %struct.impl1** %1, align 8
  %7 = getelementptr inbounds %struct.impl1* %6, i32 0, i32 0
  store i32 %5, i32* %7, align 4
  ret void
}

define void @op2(%struct.impl1* %a, i32* %r) nounwind uwtable ssp {
  %1 = alloca %struct.impl1*, align 8
  %2 = alloca i32*, align 8
  store %struct.impl1* %a, %struct.impl1** %1, align 8
  store i32* %r, i32** %2, align 8
  %3 = load %struct.impl1** %1, align 8
  %4 = getelementptr inbounds %struct.impl1* %3, i32 0, i32 0
  %5 = load i32* %4, align 4
  %6 = load i32** %2, align 8
  store i32 %5, i32* %6
  ret void
}

define void @op3(%struct.impl2* %a) nounwind uwtable ssp {
  %1 = alloca %struct.impl2*, align 8
  store %struct.impl2* %a, %struct.impl2** %1, align 8
  %2 = load %struct.impl2** %1, align 8
  %3 = getelementptr inbounds %struct.impl2* %2, i32 0, i32 1
  %4 = load %struct.impl1** %3, align 8
  call void @op1(%struct.impl1* %4)
  %5 = load %struct.impl2** %1, align 8
  %6 = getelementptr inbounds %struct.impl2* %5, i32 0, i32 2
  %7 = load %struct.impl1** %6, align 8
  call void @op1(%struct.impl1* %7)
  ret void
}
