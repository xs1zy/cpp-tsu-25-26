#include <iostream>
#include <string>
using namespace std;

long long extractValue(const string &text) {
    int p = text.length() - 1;
    while (p >= 0 && text[p] == ' ') p--;
    int endPos = p;
    while (p >= 0 && text[p] >= '0' && text[p] <= '9') p--;
    
    long long total = 0;
    for (int idx = p + 1; idx <= endPos; idx++) {
        total = total * 10 + (text[idx] - '0');
    }
    return total;
}

void sortArray(long long arr[], int size) {
    for (int current = 1; current < size; current++) {
        long long temp = arr[current];
        int previous = current - 1;
        while (previous >= 0 && arr[previous] > temp) {
            arr[previous + 1] = arr[previous];
            previous--;
        }
        arr[previous + 1] = temp;
    }
}

int main() {
    int totalEmployees;
    cin >> totalEmployees;
    cin.ignore();
    
    long long compensation[totalEmployees];
    
    for (int idx = 0; idx < totalEmployees; idx++) {
        string employeeData;
        getline(cin, employeeData);
        compensation[idx] = extractValue(employeeData);
    }
    
    sortArray(compensation, totalEmployees);
    
    cout << compensation[totalEmployees / 2] << endl;
    
    return 0;
}
