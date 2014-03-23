#define INDEX_CHUNK 409600 //50KB
#define DATA_CHUNK 20971520 //2.5MB
//#define DATA_CHUNK 2097152 //2.5MB
#include <zlib.h>
#include <stdlib.h>
#include <iostream>
#include <string>
using namespace std;
char *memAlloc(gzFile *, int);

int main (int argc, char * argv[])
{
    gzFile *cData,*cIndex;
    char *indexBuffer, *dataBuffer;
    //cIndex=gzopen("nz2_merged/0_index","r");
    cIndex=static_cast<void**>(gzopen("nz2_merged/0_index","r"));
    //cData=gzopen("nz2_merged/0_data","r");
    cData=static_cast<void**>(gzopen("nz2_merged/0_data","r"));
    indexBuffer=memAlloc(cIndex, INDEX_CHUNK);
    dataBuffer=memAlloc(cData, DATA_CHUNK);
    string indexString(indexBuffer);
    string dataString(dataBuffer);
    cout << dataString << endl;
}

/******************************************

 *Read a gz file into a buffer

 *@param fileName the filename to be read

 *@param size the initial size of the buffer

 *@return the buffer

 ******************************************/
char *memAlloc(gzFile *fileName, int size)    
{
    char *buffer=(char *)malloc(size);
    int oldSize=size;

    int count=0;             //The number of bytes that already read
    while (!gzeof(fileName))
    {
        count+=gzread(fileName,buffer+count,oldSize);
        if (count==size)                    // Reallocate when buffer is full
        {
            oldSize=size;
            size*=2;
            buffer=(char *)realloc(buffer,size);
        }
    }
    return buffer;
}
