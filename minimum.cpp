#include <limits>

double minimum(double arr[], long long int n) {
    double m = std::numeric_limits<double>::infinity();
    for (long long int i = 0; i < n; ++i)
        if (arr[i] < m) m = arr[i];
    return m;
}
