; ModuleID = 'pg8.c'
target datalayout = "e-p:64:64:64-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:64:64-f32:32:32-f64:64:64-v64:64:64-v128:128:128-a0:0:64-s0:64:64-f80:128:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.7.4"

%struct.anon = type { float, float }
%struct.anon.0 = type { %struct.anon*, %struct.anon* }

define void @dx(%struct.anon* %m, float %d) nounwind uwtable ssp {
  %1 = alloca %struct.anon*, align 8
  %2 = alloca float, align 4
  store %struct.anon* %m, %struct.anon** %1, align 8
  store float %d, float* %2, align 4
  %3 = load float* %2, align 4
  %4 = load %struct.anon** %1, align 8
  %5 = getelementptr inbounds %struct.anon* %4, i32 0, i32 0
  %6 = load float* %5, align 4
  %7 = fadd float %6, %3
  store float %7, float* %5, align 4
  ret void
}

define void @segment_dx(%struct.anon.0* %s, float %d) nounwind uwtable ssp {
  %1 = alloca %struct.anon.0*, align 8
  %2 = alloca float, align 4
  store %struct.anon.0* %s, %struct.anon.0** %1, align 8
  store float %d, float* %2, align 4
  %3 = load %struct.anon.0** %1, align 8
  %4 = getelementptr inbounds %struct.anon.0* %3, i32 0, i32 0
  %5 = load %struct.anon** %4, align 8
  %6 = load float* %2, align 4
  call void @dx(%struct.anon* %5, float %6)
  %7 = load %struct.anon.0** %1, align 8
  %8 = getelementptr inbounds %struct.anon.0* %7, i32 0, i32 1
  %9 = load %struct.anon** %8, align 8
  %10 = load float* %2, align 4
  call void @dx(%struct.anon* %9, float %10)
  ret void
}
