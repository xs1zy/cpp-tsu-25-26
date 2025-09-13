#include "header/testlib.h"

typedef unsigned long long int ull;
typedef long long int ll;
typedef long double ld;

int main(int argc, char *argv[]) {
  setName("compare files");
  registerTestlibCmd(argc, argv);

  while (!ans.eof()) {
    if (ans.readChar() != ouf.readChar()) {
      quitf(_wa, "files differ");
    }
  }

  ouf.readEof();
  quit(_ok, "files are identical");
}
