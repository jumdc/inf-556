#include <iostream>

using namespace std;

int main (int argc, char** argv) {
  
  char buf[256];
  int n;
  double x, y, z;
  
  cin.getline(buf, 255);

  cin >> n;
  cin.getline(buf, 255);

  while (n-->0) {
    cin >> x >> y >> z;
    cout << x << " " << y << " " << z << endl;
  }

}
