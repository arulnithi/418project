//Function foo parsed from ast_test.py

#include <stdio.h>
#include <math.h>
#include <stdlib.h>

#define pi 3.14159265

void foo(float* brg1,float* arg2) {
    for (int x=0; x<5; x+= 1) {
            for (int y=0; y<100; y+= 1) {
                brg1[x]=arg2[x]+1;
            }
    }
}

int main() {
    printf("STARTING MAIN FUNCTION\n");
    float brg1 [5]={1, 2, 3, 4, 5};
    float* arg2=(float*)malloc(5*sizeof(float));
    foo(brg1,arg2);
    free (arg2);
    return 0;
}
