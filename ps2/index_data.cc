#define INDEX_CHUNK 409600 //50KB
//#define DATA_CHUNK 2097152 //2.5MB
#include <zlib.h>
#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include "split.h"
#include "parser.h"
using namespace std;
/******************************************

 *Read a gz file into a buffer

 *@param fileName the filename to be read

 *@param size the initial size of the buffer

 *@return the buffer

 ******************************************/
string memAlloc(gzFile* fileName, int size)    
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
    string content(buffer);
    free(buffer);
    return content;
}

int main (int argc, char* argv[])
{
    long doc_num = atoi(argv[2]);
    gzFile *cData,*cIndex;
    ofstream myfile;
    int j = atoi(argv[1]);
    cout << j << endl;
    ostringstream start;
    ostringstream end;
    start << j;
    int n = (j == 4100)? 79:99;
    end << (j + 99);
    string folder_name("vol_" + start.str() + "_" + end.str() + "/");
    for (int i = 0; i <= n; i++)
    {
        ostringstream convert;
        convert << (i+j);
        string file_num(folder_name + convert.str());
        cout << file_num << endl;
        cIndex=static_cast<void**>(gzopen((file_num + "_index").c_str(),"r"));
        cData=static_cast<void**>(gzopen((file_num + "_data").c_str(),"r"));
        vector<string> indexes = split(memAlloc(cIndex, INDEX_CHUNK), '\n');
        int length = 0;
        string docID_url = "docID_url.rpt";
        for (vector<string>::iterator it = indexes.begin(); it != indexes.end(); ++it)
        {
            vector<string> status = split(*it);
            string url = status[0];
            string len = status[3];
            length += atoi(len.c_str());
            char* buffer=(char*)malloc(length);
            gzread(cData,buffer,length);
            char* pool = (char*)malloc(2*length+1);
            int ret = parser(buffer, pool, 2*length+1);

            myfile.open(docID_url.c_str(), ios::app | ios::binary);
            myfile << doc_num++ << " " << url << endl;
            myfile.close();

            myfile.open((file_num + ".txt").c_str(), ios::app | ios::binary);

            if (ret > 0)
            {
                vector<string> words = split(pool, '\n');
                for (vector<string>::iterator it = words.begin(); it != words.end(); it++)
                {
                    vector<string> word = split(*it);
                    myfile << word[0] << " " << doc_num << endl;
                }
            }
            myfile.close();

            free(pool);
            free(buffer);
        }
    }
    return 0;
}

