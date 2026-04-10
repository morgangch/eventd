#include <cassert>

#include "engine.hpp"

int main() {
    eventd::Engine engine;
    assert(!engine.name().empty());
    return 0;
}
