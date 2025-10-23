double average(double arr[], long long int n) {
    double s = 0;
    for (long long int i = 0; i < n; ++i)
        s += arr[i];
    return s / n;
}
