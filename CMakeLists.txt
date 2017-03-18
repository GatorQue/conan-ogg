PROJECT(conanogg)
cmake_minimum_required(VERSION 2.8)
include(${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

if(MSVC)
    add_definitions(-D_CRT_SECURE_NO_DEPRECATE)
    add_definitions(-D_CRT_NONSTDC_NO_DEPRECATE)
    add_definitions(-DLIBOGG_EXPORTS)
endif()

set(LIB_VERSION_MAJOR 1)
set(LIB_VERSION_MINOR 3)
set(LIB_VERSION_PATCH 2)
set(LIB_VERSION ${LIB_VERSION_MAJOR}.${LIB_VERSION_MINOR}.${LIB_VERSION_PATCH})

set(LIB_SOURCES src/bitwise.c src/framing.c)

include(CheckIncludeFiles)
check_include_files(inttypes.h INCLUDE_INTTYPES_H)
check_include_files(stdint.h INCLUDE_STDINT_H)
check_include_files(sys/types.h INCLUDE_SYS_TYPES_H)
set(SIZE16 int16_t)
set(USIZE16 uint16_t)
set(SIZE32 int32_t)
set(USIZE32 uint32_t)
set(SIZE64 int64_t)

configure_file(include/ogg/config_types.h.in include/ogg/config_types.h @ONLY)
include_directories(${PROJECT_BINARY_DIR}/include)
include_directories(include)

set(LIB_PUBLIC_HEADERS include/ogg/ogg.h include/ogg/os_types.h
    ${PROJECT_BINARY_DIR}/include/ogg/config_types.h)

install(FILES ${LIB_PUBLIC_HEADERS} DESTINATION include/ogg)

add_library(ogg ${LIB_SOURCES})

set_target_properties(ogg PROPERTIES SOVERSION ${LIB_VERSION_MAJOR})
if(NOT CYGWIN)
    # This property causes shared libraries on Linux to have the full version
    # encoded into their final filename.  We disable this on Cygwin because
    # it causes cygz-${ZLIB_FULL_VERSION}.dll to be created when cygz.dll
    # seems to be the default.
    set_target_properties(ogg PROPERTIES VERSION ${LIB_VERSION})
endif()

install(TARGETS ogg
        RUNTIME DESTINATION bin
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib)

if(BUILD_SHARED_LIBS)
    set(LIB_PC ${PROJECT_BINARY_DIR}/ogg.pc)
    set(prefix ${CMAKE_INSTALL_PREFIX})
    set(exec_prefix ${CMAKE_INSTALL_PREFIX})
    set(libdir ${CMAKE_INSTALL_PREFIX}/lib)
    set(includedir ${CMAKE_INSTALL_PREFIX}/include)
    set(VERSION ${LIB_VERSION})
    configure_file(ogg.pc.in ${LIB_PC} @ONLY)
    install(FILES ${LIB_PC} DESTINATION lib/pkgconfig)
endif()

