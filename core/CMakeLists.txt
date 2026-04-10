cmake_minimum_required(VERSION 3.16)
project(eventd_core VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(eventd-core
    src/main.cpp
)

target_include_directories(eventd-core
    PRIVATE include
)

include(CTest)
if(BUILD_TESTING)
    add_executable(core-smoke-tests
        tests/test_smoke.cpp
    )
    add_test(NAME core-smoke COMMAND core-smoke-tests)
endif()
