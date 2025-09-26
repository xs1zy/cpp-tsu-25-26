#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int result = 0;
    int i = 0; 
    while (i < n) {
        int amount, cost;
        cin >> amount >> cost;
        result += amount * cost;
        i++;
    }
    cout << result << endl;
    return 0;
}
