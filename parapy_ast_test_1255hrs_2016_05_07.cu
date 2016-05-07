//Function foo parsed from ast_test.py

#include <stdio.h>
#include <math.h>
#include <stdlib.h>

#define pi 3.14159265

__global__ void foo(float* arg,float* ret) {
    int index = blockIdx.x * blockDim.x + threadIdx.x;
    if (index > 20) {
        return;
    }
    if (arg[index]>10) {
        ret[index]=1.0;
    }
    else {
        ret[index]=0.0;
    }
}

int main() {
    printf("STARTING MAIN FUNCTION\n");
    
    //Define constants to use
    const int N = 20;
    const int blocksize = 128;
    
    //Allocate the variables
    float arg [20]={1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20};
    float* ret=(float*)malloc(20*sizeof(float));
    
    //Declare and allocate the variables and copy it over to device
    float *argCuda;
    float *retCuda;
    const int csize = N*sizeof(float);
    cudaMalloc( (void**)&argCuda, csize );
    cudaMalloc( (void**)&retCuda, csize );
    cudaMemcpy( argCuda, arg, csize, cudaMemcpyHostToDevice );
    
    //Setup variables for cuda block and grid and then call function
    dim3 dimBlock( blocksize, 1 );
    dim3 dimGrid( ((N + blocksize - 1) / blocksize), 1 );
    foo<<<dimGrid, dimBlock>>>(argCuda,retCuda);
    
    //Copy back result data
    cudaMemcpy(ret, retCuda, N * sizeof(float), cudaMemcpyDeviceToHost);
    
    //Free allocated memory
    cudaFree( argCuda );
    cudaFree( retCuda );
    free (ret);
    return 0;
}
