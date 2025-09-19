#include <iostream>

int main() {
    int price;   
    int count;   
    int total; 
    std::cout << "СТОИМОСТИ ТОВАРА" << std::endl;
    std::cout << std::endl;
    std::cin >> price;
    std::cin >> count;
    total = price * count;
    std::cout << std::endl;
    std::cout << "Цена за одно: " << price << " руб." << std::endl;
    std::cout << "Количество: " << count << " шт." << std::endl;
    std::cout << "Общая стоимость: " << total << " руб." << std::endl;
    return 0;
}
