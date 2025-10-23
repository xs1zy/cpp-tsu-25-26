#include <string>

struct Index {
    long long int index;
    double value;
};

struct Product {
    std::string name;
    double prices[100];
};

struct ScoredProduct {
    std::string name;
    double score;
};

void selection_sort(Index arr[], long long int n);
double average(double arr[], long long int n);

ScoredProduct convert_product(Product p, long long int k) {
    Index arr[100];
    for (long long int i = 0; i < k; ++i) {
        arr[i].index = i;
        arr[i].value = p.prices[i];
    }
    selection_sort(arr, k);
    double sorted[100];
    for (long long int i = 0; i < k; ++i)
        sorted[i] = arr[i].value;
    ScoredProduct result;
    result.name = p.name;
    result.score = average(sorted, k);
    return result;
}
