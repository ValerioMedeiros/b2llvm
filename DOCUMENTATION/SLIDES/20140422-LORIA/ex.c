extern void gcd(int *, int, int);
typedef struct {
  int s;
  int n;
  int d;
} * Trat;
void norm(Trat P)
{
  int g;
  if (P->d == 0)
    goto end;
  gcd(&g, P->n, P->d);
  P->n /= g;
  P->d /= g;
end:
  return;
}
