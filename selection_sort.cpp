#include <utility>

struct Index {
    long long int index;
    double value;
};

void selection_sort(Index arr[], long long int n) {
    for (long long int i = 0; i < n - 1; ++i) {
        long long int minIdx = i;
        for (long long int j = i + 1; j < n; ++j)
            if (arr[j].value < arr[minIdx].value)
                minIdx = j;
        std::swap(arr[i], arr[minIdx]);
    }
}
