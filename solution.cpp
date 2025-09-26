#include <iostream>
using namespace std;

int main() {
    int n;
    double sum = 0;
    cin >> n;
    
    for(int i = 0; i < n; i++) {
        double num;
        cin >> num;
        sum += num;
    }
    
    double average = sum / n;
    cout << average << endl;
    
    return 0;
}
