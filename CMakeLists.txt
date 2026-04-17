
##################################################################################
#                                                                                #
# CMake file to be used to install KDSource distribution.                        #
#                                                                                #
# See README.md file for installation instructions.                              #
#                                                                                #
# Written 2021 by O. I. Abbate.                                                  #
#                                                                                #
##################################################################################

cmake_minimum_required(VERSION 3.10.0)

project(KDSource VERSION 0.1.0)
configure_file(include/kdsource/KDSourceConfig.h.in KDSourceConfig.h)

enable_testing()

set(INSTALL_PY OFF CACHE STRING "Whether to also install kdsource and mcpl python files.")


set(CMAKE_C_STANDARD 99)

set(SRC "${PROJECT_SOURCE_DIR}/src")
set(INC "${PROJECT_SOURCE_DIR}/include")

find_package(LibXml2 REQUIRED)

set(BUILD_WITHG4 OFF CACHE STRING "Whether to build Geant4 plugins if Geant4 is available.")
#add_subdirectory(mcpl)

set(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib")

# Set installation paths
set(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib")
set(KDSource_CMAKEDIR "${CMAKE_INSTALL_LIBDIR}/cmake/KDSource")
set(KDSource_BINDIR "${CMAKE_INSTALL_BINDIR}")
set(KDSource_LIBDIR "${CMAKE_INSTALL_LIBDIR}")
set(KDSource_INCDIR "${CMAKE_INSTALL_INCLUDEDIR}")

# Install destination setting
set(INSTDEST "RUNTIME;DESTINATION;${KDSource_BINDIR};LIBRARY;DESTINATION;${KDSource_LIBDIR};ARCHIVE;DESTINATION;${KDSource_LIBDIR}")

# Define kdsource shared library and sources
add_library(kdsource SHARED "${SRC}/kdsource/kdsource.c"
                            "${SRC}/kdsource/plist.c"
                            "${SRC}/kdsource/geom.c"
                            "${SRC}/kdsource/utils.c")

# Include directories for kdsource library
target_include_directories(kdsource
    PUBLIC
        $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
        $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/src>
        $<INSTALL_INTERFACE:${KDSource_INCDIR}>
)

# Include directory for the configured version file
target_include_directories(kdsource
PUBLIC $<BUILD_INTERFACE:${CMAKE_BINARY_DIR}>)

# Link necessary libraries
target_link_libraries(kdsource PUBLIC m LibXml2::LibXml2 mcpl)


# Install kdsource library and export targets for other projects
install(TARGETS kdsource EXPORT KDSourceTargets ${INSTDEST} )
install(EXPORT KDSourceTargets FILE KDSourceTargets.cmake NAMESPACE KDSource:: DESTINATION ${KDSource_CMAKEDIR} )

add_library(KDSource::kdsource ALIAS kdsource)#always alias namespaces locally

# Install kdsource headers
install(FILES "${INC}/kdsource/kdsource.h"
              "${INC}/kdsource/plist.h"
              "${INC}/kdsource/geom.h"
              "${INC}/kdsource/utils.h"
              "${CMAKE_CURRENT_BINARY_DIR}/KDSourceConfig.h"
              DESTINATION ${KDSource_INCDIR}/kdsource)

# Install scripts for kdtool and kdtool's utilities
install(PROGRAMS "${SRC}/kdtool/kdtool.sh" DESTINATION ${KDSource_BINDIR} RENAME kdtool)
install(PROGRAMS "${SRC}/kdtool/templates.sh" DESTINATION ${KDSource_BINDIR} RENAME kdtool-templates)
add_executable(kdtool-resample "${SRC}/kdtool/resample.c")
add_executable(kdtool-beamtest "${SRC}/kdtool/beamtest.c")
target_link_libraries(kdtool-resample PUBLIC kdsource)
target_link_libraries(kdtool-beamtest PUBLIC kdsource)
install(TARGETS kdtool-resample kdtool-beamtest ${INSTDEST} )

# Install tests
add_subdirectory(tests)

# Install additional directories
install(DIRECTORY docs mcstas templates DESTINATION .)

if (INSTALL_PY)
	install(DIRECTORY "python/kdsource" DESTINATION python)
endif()

# Configure and install KDSource CMake configuration file
configure_file(cmake/KDSourceConfig.cmake.in "${CMAKE_CURRENT_BINARY_DIR}/KDSourceConfig.cmake" @ONLY)
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/KDSourceConfig.cmake" DESTINATION ${KDSource_CMAKEDIR})