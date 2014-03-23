#define INDEX_CHUNK 409600 //50KB
//#define DATA_CHUNK 2097152 //2.5MB
#include <zlib.h>
#include <stdlib.h>
#include <iostream>
using namespace std;
/******************************************

 *Read a gz file into a buffer

 *@param fileName the filename to be read

 *@param size the initial size of the buffer

 *@return the buffer

 ******************************************/
char* memAlloc(gzFile* fileName, int size)    
{
    char* buffer=(char*)malloc(size);
    int oldSize=size;

    int count=0;             //The number of bytes that already read
    while (!gzeof(fileName))
    {
        count+=gzread(fileName,buffer+count,oldSize);
        if (count==size)                    // Reallocate when buffer is full
        {
            oldSize=size;
            size*=2;
            buffer=(char*)realloc(buffer,size);
        }
    }
    return buffer;
}

int main (int argc, char* argv[])
{
    gzFile *cData,*cIndex;
    char *indexBuffer, *dataBuffer;
    //cIndex=gzopen("nz2_merged/0_index","r");
    cIndex=static_cast<void**>(gzopen(argv[1],"r"));
    indexBuffer=memAlloc(cIndex, INDEX_CHUNK);
    cout << indexBuffer << endl;
    return 0;
}

