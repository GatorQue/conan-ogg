PROJECT(MyHello)
cmake_minimum_required(VERSION 2.8)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

find_package("Ogg")

IF(OGG_FOUND)
    ADD_EXECUTABLE(testpkg testpkg.c)
    include_directories(${OGG_INCLUDE_DIR})
    TARGET_LINK_LIBRARIES(testpkg ${OGG_LIBRARY})
ELSE()
    MESSAGE(FATAL_ERROR "Ogg not found")
ENDIF()
