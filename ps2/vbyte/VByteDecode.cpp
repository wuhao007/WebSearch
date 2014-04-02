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

  const int len = 4;
  ifstream ifile ("inverted_list.vbyte", ifstream::binary);
  if (ifile.is_open())
  {
      ofstream ofile ("inverted_list.cmp", ofstream::binary);
      if (ifile.is_open())
      {
          string line;
          ifstream lexicon ("lexicon.rpt", ifstream::binary);
          while ( getline (lexicon,line) )
          {
              vector<string> vs = split(line);
              ofile << vs[0];
              int start = atoi(vs[1].c_str());
              int end = atoi(vs[2].c_str());
 
              while (start < end)
              {
                  char buffer[len];
                  ifile.read(buffer, len);

                  uint8_t val[len];
                  memset(val, len, 0);

                  memcpy(val, string(buffer).substr(0, len).c_str(), len);

                  uint64_t decoded;

                  uint32_t byte_read = VByte::decode(&decoded, val);
                  
                  ofile << " " << decoded;

                  start += len;
              }
              ofile << endl;
          }
          ofile.close();
      }
      else
          cout << "Unable to open file"; 

      ofile.close();
  }
  else 
      cout << "Unable to open file";

  return 0;
}
