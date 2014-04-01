#include "VByte.h"
#include <iostream>
#include <fstream>
#include <string>
using namespace std;
class VByte;
int main()
{
    ofstream ofile;
    ofile.open("vbyte.txt");
    VByte vbyte = VByte();
    uint64_t value = 64;
    vbyte.encode(ofile, value);
    ofile.close();
    ifstream ifile("vbyte.txt");
    if (ifile.is_open())
    {
        string line;
        while (getline (ifile,line))
        {
          cout << line << '\n';
        }
        ifile.close();
    }
    unsigned char buffer[256];
    vbyte.encode(buffer, value);
    cout << buffer << endl;
    unsigned char max = 'Z';
    unsigned char* maxPtr = &max;
    uint64_t* value_ptr = &value;
    vbyte.decode(buffer, maxPtr, value_ptr);
    cout << buffer << endl;
}

