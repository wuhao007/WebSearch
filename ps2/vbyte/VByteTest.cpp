#include <iostream>
#include "VByte.h"

using namespace std;

void display(uint8_t *bytes, uint32_t len) {
  for (int i = 0; i < len; ++i) {
    cout << hex << (int)bytes[i] << endl;
  }
}

int main()
{
  uint64_t from = 1;
  uint8_t to[9] = {0};
  memset(to, 9, 0);
  uint32_t count_byte = VByte::encode(from, to);

  memset(to, 9, 0);
  from = 127;
  count_byte = VByte::encode(from, to);

  memset(to, 9, 0);
  from = 128;
  count_byte = VByte::encode(from, to);
/*
  uint64_t from = 28038249122;
  uint8_t to[9];
  memset(to, 9, 0);
  uint32_t count_byte = VByte::encode(from, to);

  uint64_t decoded = 0;
  uint32_t byte_read = VByte::decode(&decoded, to);

  uint8_t from[9];

  memset(from, 0, 9);
  from[0] = 0x87;
  uint64_t value;
  uint32_t byte_count = VByte::decode(&value, from);

  memset(from, 0, 9);
  from[0] = 0x7F;
  from[1] = 0x81;
  byte_count = VByte::decode(&value, from);

  memset(from, 0, 9);
  memset(from, 0x7f, 4);
  from[4] = 0x8f;
  //display(from, 9);
  byte_count = VByte::decode(&value, from);
  //cout << endl << "value" << endl;
  //display((uint8_t *)&value, sizeof(uint64_t));

  uint64_t expected = ~0ULL >> 32;
*/
return 0;
}
