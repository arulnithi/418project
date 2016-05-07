//Function foo parsed from ast_test.py

#include <stdio.h>
#include <math.h>
#include <stdlib.h>

#define pi 3.14159265

__global__ void foo(int alpha,float* x,float* y,float* result) {
    int index = blockIdx.x * blockDim.x + threadIdx.x;
    if (index > 20) {
        return;
    }
    result[index]=alpha*x[index]+y[index];
}

int main() {
    printf("STARTING MAIN FUNCTION\n");
    
    //Define constants to use
    const int N = 20;
    const int blocksize = 128;
    
    //Allocate the variables
    float x [20]={1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20};
    float y [20]={1, 2, 3, 4, 2, 4, 2, 63, 4, 7, 4, 8, 3, 1, 2, 5, 1, 5, 2, 2};
    float* result=(float*)malloc(20*sizeof(float));
    
    //Declare and allocate the variables and copy it over to device
    float *xCuda;
    float *yCuda;
    float *resultCuda;
    const int csize = N*sizeof(float);
    cudaMalloc( (void**)&xCuda, csize );
    cudaMalloc( (void**)&yCuda, csize );
    cudaMalloc( (void**)&resultCuda, csize );
    cudaMemcpy( xCuda, x, csize, cudaMemcpyHostToDevice );
    cudaMemcpy( yCuda, y, csize, cudaMemcpyHostToDevice );
    
    //Setup variables for cuda block and grid and then call function
    dim3 dimBlock( blocksize, 1 );
    dim3 dimGrid( ((N + blocksize - 1) / blocksize), 1 );
    foo<<<dimGrid, dimBlock>>>(2,xCuda,yCuda,resultCuda);
    
    //Copy back result data
    cudaMemcpy(result, resultCuda, N * sizeof(float), cudaMemcpyDeviceToHost);
    
    //Free allocated memory
    cudaFree( xCuda );
    cudaFree( yCuda );
    cudaFree( resultCuda );
    free (result);
    return 0;
}
