#include <iostream>

int main() {
    int price;   
    int count;   
    int total;
    
    std::cin >> price;
    std::cin >> count;
    
    total = price * count;
    
    std::cout << price << std::endl;
    std::cout << count << std::endl;
    std::cout << total << std::endl;
    
    return 0;
}
