#include <iostream>
#include <cmath>
#include <string>

struct Product {
    std::string name;
    double prices[100];
};

struct ScoredProduct {
    std::string name;
    double score;
};

void read_data(Product products[], long long int n, long long int k);
ScoredProduct convert_product(Product p, long long int k);
double minimum(double arr[], long long int n);

int main() {
    long long int N, K;
    std::cin >> N >> K;
    Product products[100];
    read_data(products, N, K);
    ScoredProduct scored[100];
    for (long long int i = 0; i < N; ++i)
        scored[i] = convert_product(products[i], K);
    double scores[100];
    for (long long int i = 0; i < N; ++i)
        scores[i] = scored[i].score;
    double total = minimum(scores, N);
    long long int best = 0;
    double diff = std::abs(scored[0].score - total);
    for (long long int i = 1; i < N; ++i) {
        double d = std::abs(scored[i].score - total);
        if (d < diff) {
            best = i;
            diff = d;
        }
    }
    std::cout << "Total score: " << total << std::endl;
    std::cout << "Best product: " << scored[best].name
              << " (score: " << scored[best].score << ")" << std::endl;
    return 0;
}
