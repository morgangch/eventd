#pragma once

#include <string>

namespace eventd {

class Engine {
public:
    [[nodiscard]] std::string name() const { return "internal-monitor-engine"; }
};

} // namespace eventd
