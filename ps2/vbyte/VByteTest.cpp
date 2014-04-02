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
  const int len = 8;
  uint64_t from = 28038249122;
  //uint64_t from = 2;
  uint8_t to[len];
  memset(to, len, 0);
  uint32_t count_byte = VByte::encode(from, to);
  ofstream lfile("ltest.txt", ifstream::binary);
  ofstream ofile("otest.txt", ifstream::binary);
  lfile << ofile.tellp();
  ofile << to;
  lfile << ofile.tellp();
  ofile.close();
  lfile.close();

  ifstream ifile("otest.txt", ifstream::binary);
  char buffer[len];
  //string buffer;
  ifile.read(buffer, len);
  cout << "buffer:" << buffer << endl;
  cout << "to:" << to << endl;

  uint8_t val[len];
  memset(val, len, 0);

  memcpy(val, string(buffer).substr(0, len).c_str(), len);
//  cout << "val:" << (val+offset) << '\n';
/*
  for (int i = 0; i< buffer.size(); i++)
  {
    memset(to[i], 1, buffer[i]);
  }
*/
  cout << "val:" << val << endl;
  uint64_t decoded;
  memset(to, len, 0);
  //uint32_t byte_read = VByte::decode(&decoded, to);
  uint32_t byte_read = VByte::decode(&decoded, val);
  cout << "decode " << decoded << endl;
  return 0;
}
