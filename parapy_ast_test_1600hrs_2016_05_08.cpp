//Function foo parsed from ast_test.py

#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <iostream>

#define pi 3.14159265

void foo(int alpha,float* x,float* y,float* result) {
    int index=0;
    result[index]=alpha*x[index]+y[index];
    std::cout << "hi " << 1 << " "  << std::endl;
}

int main() {
    printf("STARTING MAIN FUNCTION\n");
    float x [20]={1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20};
    float y [20]={1, 2, 3, 4, 2, 4, 2, 63, 4, 7, 4, 8, 3, 1, 2, 5, 1, 5, 2, 2};
    float* result=(float*)malloc(20*sizeof(float));
    foo(2,x,y,result);
    free (result);
    return 0;
}
