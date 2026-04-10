#include <iostream>

#include "engine.hpp"

int main() {
    eventd::Engine engine;
    std::cout << "eventd-core starting: " << engine.name() << std::endl;
    return 0;
}
