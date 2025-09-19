#include <iostream>
using namespace std;
int main() {
    int n;
    double sum = 0;
    cin >> n;
    double num[n];
    for(int i = 0; i < n; i++) {
        cin >> num[i];
        sum += num[i];
    }
    double average = sum / n;
    cout << average << endl;
    return 0;
}
