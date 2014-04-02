#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include "VByte.h"
#include "split.h"
#include <stdlib.h>

using namespace std;

void display(uint8_t *bytes, uint32_t len) {
  for (int i = 0; i < len; ++i) {
    cout << hex << (int)bytes[i] << endl;
  }
}

int main()
{
/*
  uint64_t from = 28038249122;
  uint8_t to[9];
  memset(to, 9, 0);
  uint32_t count_byte = VByte::encode(from, to);
  cout << to << endl;
  cout << to[0] << endl;
  uint64_t decoded = 0;
  memset(to, 9, 0);
  uint32_t byte_read = VByte::decode(&decoded, to);
  cout << "decoded " << decoded << endl;
*/

  const int len = 3;
  ofstream ofile ("inverted_list.vbyte", ofstream::binary);
  if (ofile.is_open())
  {
      ifstream ifile ("inverted.list", ifstream::binary);
      if (ifile.is_open())
      {
          ofstream lexicon ("lexicon.rpt", ofstream::binary);
          string line;
          while ( getline (ifile,line) )
          {
              vector<string> vs = split(line);
              lexicon << vs[0] << " " << ofile.tellp() << " "; 
              for (int i = 1; i != vs.size(); i++)
              {
                  uint64_t from = atol(vs[i].c_str());
                  uint8_t to[len];
                  memset(to, len, 0);
                  uint32_t count_byte = VByte::encode(from, to);
                  for (int i = 0; i < len; i++)
                  {
                      ofile << to[i]; 
                  }
              }
              lexicon << ofile.tellp() << endl; 
          }
          ifile.close();
          lexicon.close();
      }
      else
          cout << "Unable to open file"; 

      ofile.close();
  }
  else 
      cout << "Unable to open file";

  return 0;
}
