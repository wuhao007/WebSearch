#include "split.h"
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <list>
#include <map>
#include <set>
using namespace std;
int main()
{
    ifstream file("merge.rpt");
    ofstream myfile, lexicon;
    myfile.open("merge.map", ios::app | ios::binary);
    lexicon.open("lexicon.rpt", ios::app | ios::binary);
    string str; 
    string pre("");
    int preFre = -1;
    //string docs("");
    list<int> docID;
    set<int> idset;
    map<int,int> fre;
    long line = 0;
    string file_name("");
    while (getline(file, str))
    {
        vector<string> v = split(str);
        int id = atoi(v[1].c_str());
        if (pre == v[0])
        {
           idset.insert(id);
           //docs += (v[1] + " ");  
           if (fre.find(id) != fre.end())
           {
               fre[id]++;
           }
           else
           {
               fre[id] = 1;
           }
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
           preFre = id;
           docID.clear();
           for (set<int>::iterator it = idset.begin(); it != idset.end(); it++)
           {
               docID.push_back(*it);
           }
           docID.sort();
           for (list<int>::iterator it = docID.begin(); it != docID.end(); it++)
           {
               myfile << "  " << *it << " " << fre[*it];
           }
           myfile << endl;
           lexicon << v[0] << " " << file_name << " " << (line%10000)+1 << endl;
           //docs = (v[0] + " " + v[1] + " ");
           myfile << v[0];
           fre.clear();
           idset.clear();
           idset.insert(id);
           fre[id] = 1;
        }
    }
    file.close();
    myfile.close();

    return 0;
}
