#define INDEX_CHUNK 409600 //50KB
//#define DATA_CHUNK 2097152 //2.5MB
#include <zlib.h>
#include <ctype.h>
#include <algorithm>
#include <iterator>
#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <set>
#include "split.h"
#include "parser.h"
using namespace std;
/******************************************

 *Read a gz file into a buffer

 *@param fileName the filename to be read

 *@param size the initial size of the buffer

 *@return the buffer

 ******************************************/
string make_lowercase(const string& in )
{
  string out;

  transform( in.begin(), in.end(), std::back_inserter( out ), ::tolower );
  return out;
}

string memAlloc(gzFile* fileName, int length)    
{
//    int oldSize=size;

//    int count=0;             //The number of bytes that already read
    char* buffer = new char [length];
    while (!gzeof(fileName))
    {
//        count+=gzread(fileName,buffer+count,oldSize);
        gzread(fileName,buffer, length);
/*
        if (count==size)                    // Reallocate when buffer is full
        {
            oldSize=size;
            size*=2;
            buffer=(char*)realloc(buffer,size);
        }
*/
    }
    string content(buffer);
    free(buffer);
    return content;
}

int main (int argc, char* argv[])
{
    ifstream is ("words.list");
    string english_words;
    getline(is, english_words);
    set<string> english_words_set;
    vector<string> english_words_vector = split(english_words); 
    for (vector<string>::iterator it = english_words_vector.begin(); it != english_words_vector.end(); it++)
    {
        english_words_set.insert(*it);
        //cout << *it << endl;
    }

    const string docID_url = "docID_url.rpt";
    long doc_num = atoi(argv[2]);
    //cout << "doc_num " << doc_num << endl;

    gzFile *cData,*cIndex;
    ofstream myfile;

    int j = atoi(argv[1]);
    //cout << "j " << j << endl;

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
        //cout << file_num << endl;

        cIndex=static_cast<void**>(gzopen((file_num + "_index").c_str(),"r"));
        cData=static_cast<void**>(gzopen((file_num + "_data").c_str(),"r"));

        vector<string> indexes = split(memAlloc(cIndex, INDEX_CHUNK), '\n');

        for (vector<string>::iterator it = indexes.begin(); it != indexes.end(); ++it)
        {
            vector<string> status = split(*it);
            //cout << *it << endl;
            string url = status[0];
            string len = status[3];

            //cout << "size " << atoi(len.c_str()) << " length " << length << endl;
            int length = atoi(len.c_str());
            //cout << "length " << length << endl;
            char* buffer = new char [length];
            gzread(cData,buffer,length);
            char* pool = new char [2*length+1];
            int ret = parser(buffer, pool, 2*length+1);
            //cout << buffer << endl;

            myfile.open(docID_url.c_str(), ios::app | ios::binary);
            myfile << doc_num << " " << url << " " << len << endl;
            //cout << "doc_num " << doc_num << endl;
            myfile.close();

            myfile.open((file_num + ".txt").c_str(), ios::app | ios::binary);
            //cout << "ret " << ret << endl;

            if (ret > 0)
            {
                //cout << "parse_num " << doc_num << endl;
                vector<string> words = split(pool, '\n');
                for (vector<string>::iterator wit = words.begin(); wit != words.end(); wit++)
                {
                    //ostringstream num_convert;
                    //num_convert << doc_num;
                    //string docNum(num_convert.str());
                    vector<string> word = split(*wit);
                    if (english_words_set.find(make_lowercase(word[0])) != english_words_set.end())    
                    {
                        myfile << make_lowercase(word[0]) << " " << doc_num << endl;
                    }
                }
            }
            myfile.close();

            free(pool);
            free(buffer);
            doc_num++;
        }
    }
    return 0;
}
