#include "split.h"
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
using namespace std;
int main() 
{ 
    ifstream file("merge.rpt");
    ofstream myfile, lexicon;
    myfile.open("merge.map", ios::app | ios::binary);
    lexicon.open("lexicon.rpt", ios::app | ios::binary);
    string str; 
    string pre("");
    string docs("");
    long line = 0;
    string file_name("");
    while (getline(file, str))
    {
        vector<string> v = split(str);
        if (pre == v[0])
        {
           docs += (v[1] + " ");  
        }
        else
        {
           if ((line++)%10000 == 0)
           {
              int file_num = line/10000;
              ostringstream convert;
              convert << file_num;
              myfile.close();
              file_name = "merge_" + convert.str() + ".map";
              myfile.open(file_name.c_str(), ios::app | ios::binary);
           }
           pre = v[0];
           myfile << docs << endl;
           lexicon << v[0] << " " << file_name << " " << (line%10000)+1 << endl;
           docs = (v[0] + " " + v[1] + " ");
        }
    }
    file.close();
    myfile.close();

    return 0;
}
