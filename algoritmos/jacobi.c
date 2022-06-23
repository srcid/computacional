#include <stdio.h>
#include <stdlib.h>

double max_arr(double* arr, int n) {
  double max = arr[0];
  int i;
  for (i=1;i<n;i++) if (arr[i] > max) max = arr[i];
  return max;
}

double* sub_arr(double* arr1, double* arr2, int n) {
  double* res = calloc(sizeof(double), n);
  int i;
  for (i=0;i<n;i++) {
    res[i]=arr1[i]-arr2[i];
  }
  return res;
}

double* abs_arr(double* arr, int n) {
  double* res = calloc(sizeof(double), n);
  int i;
  for (i=0; i<n; i++) res[i] = arr[i] < 0 ? arr[i]*(-1) : arr[i];
  return res;
}

double* jacobi(double** m, double* b, int n, int lim, double err) {
  double* x = (double*)calloc(n, sizeof(double));
  double* xk = (double*)calloc(n, sizeof(double));
  unsigned int i, j, k;
  double acc;

  printf("iniciando iterações\n");
  for (k=0; k<lim; k++) {
    printf("it: %d\n", k);
    for (i=0; i<n; i++) {
      acc = 0.0;
      
      for (j=0; j<n; j++) {
        if (i != j) acc = acc + m[i][j]*x[j];
      }

      xk[i] = (b[i] - acc) / m[i][i];
      printf("%f ", xk[i]);
    }

    printf("\n");

    double* sub = sub_arr(xk, x, n);
    double* sub_abs = abs_arr(sub, n);
    double max = max_arr(sub_abs, n);

    free(sub);
    free(sub_abs);

    if (max <= err) return xk;

    for (i=0; i<n; i++) x[i]=xk[i];
  }
  return x;
}

int main(int argc, char const *argv[])
{ 
  int i;
  int n = 2;
  double** m;
  double b[2] = {5,4};
  const unsigned int lim = 10;
  double err = 0.01;
  double* res;

  m = (double**)malloc(sizeof(double*)*n);
  for (i=0;i<n;i++) m[i] = (double*)malloc(sizeof(double)*n);

  m[0][0]=2;
  m[0][1]=1;
  m[1][0]=1;
  m[1][1]=2;

  printf("chamando jacobi\n");
  res = jacobi(m, b, n, lim, err);

  for (i=0; i<n; i++) {
    printf("%f\n", res[i]);
  }

  return 0;
}
