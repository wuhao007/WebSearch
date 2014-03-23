#include <zlib.h>

int compress (Bytef *dest, uLongf *destLen, const Bytef *source, uLong sourceLen)
{
  return 0;
}

int uncompress (Bytef *dest, uLongf *destLen, const Bytef *source, uLong sourceLen)
{
  return 0;
}

int main()
{
  unsigned char a[1000];
  unsigned char b[1000];
  unsigned char c[1000];

  long compressedSize, uncompressedSize;
  int status;

  /* fill array a with data */
  compressedSize = 800;
  uncompressedSize = 800;
  int i;
  for (i = 0; i < uncompressedSize; i++) {
    a[i] = (unsigned char)(i & 255);
    status = compress(b, &compressedSize, a, uncompressedSize);
    status = uncompress(c, &uncompressedSize, b, compressedSize);
  }
  return status;
}
