
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
configure_file(KDSourceConfig.h.in KDSourceConfig.h)

enable_testing()

set(INSTALL_PY OFF CACHE STRING "Whether to also install kdsource and mcpl python files.")


set(CMAKE_C_STANDARD 99)

set(SRC "${CMAKE_CURRENT_SOURCE_DIR}/src")

find_package(LibXml2 REQUIRED)

set(BUILD_WITHG4 OFF CACHE STRING "Whether to build Geant4 plugins if Geant4 is available.")
#add_subdirectory(mcpl)

set(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib")

add_library(kdsource SHARED "${SRC}/kdsource/kdsource.c"
                            "${SRC}/kdsource/plist.c"
                            "${SRC}/kdsource/geom.c"
                            "${SRC}/kdsource/utils.c")
target_include_directories(kdsource PUBLIC "${SRC}/kdsource" "${CMAKE_CURRENT_BINARY_DIR}")
target_link_libraries(kdsource PUBLIC m LibXml2::LibXml2 mcpl)
install(TARGETS kdsource DESTINATION lib)
install(FILES "${SRC}/kdsource/kdsource.h"
              "${SRC}/kdsource/plist.h"
              "${SRC}/kdsource/geom.h"
              "${SRC}/kdsource/utils.h"
              "${CMAKE_CURRENT_BINARY_DIR}/KDSourceConfig.h"
              DESTINATION include)

install(PROGRAMS "${SRC}/kdtool/kdtool.sh" DESTINATION bin RENAME kdtool)
install(PROGRAMS "${SRC}/kdtool/templates.sh" DESTINATION bin RENAME kdtool-templates)
add_executable(kdtool-resample "${SRC}/kdtool/resample.c")
add_executable(kdtool-beamtest "${SRC}/kdtool/beamtest.c")
target_link_libraries(kdtool-resample PUBLIC kdsource)
target_link_libraries(kdtool-beamtest PUBLIC kdsource)
install(TARGETS kdtool-resample kdtool-beamtest DESTINATION bin)

add_library(stockmcpl SHARED "${SRC}/tripolistock/stockmcpl.c" "${SRC}/tripolistock/stockread.c")
target_include_directories(stockmcpl PUBLIC "${SRC}/tripolistock")
target_link_libraries(stockmcpl mcpl)
if (MATH_NEEDS_LIBM)
  target_link_libraries(stockmcpl m)
endif()
add_executable(stock2mcpl "${SRC}/tripolistock/stock2mcpl_app.c")
target_link_libraries(stock2mcpl stockmcpl)
if (binaryprops)
  set_target_properties(stockmcpl PROPERTIES ${binaryprops})
  set_target_properties(stock2mcpl PROPERTIES ${binaryprops})
endif()
install(TARGETS stock2mcpl stockmcpl ${INSTDEST})
if (BUILD_EXAMPLES)
  install(FILES "${SRCEX}/example_tripolistock.stock" DESTINATION examples)
endif()

add_library(ssvmcpl SHARED "${SRC}/ssv/ssvmcpl.c" "${SRC}/ssv/ssvread.c")
target_include_directories(ssvmcpl PUBLIC "${SRC}/ssv")
target_link_libraries(ssvmcpl mcpl)
if (MATH_NEEDS_LIBM)
  target_link_libraries(ssvmcpl m)
endif()
add_executable(ssv2mcpl "${SRC}/ssv/ssv2mcpl_app.c")
target_link_libraries(ssv2mcpl ssvmcpl)
add_executable(mcpl2ssv "${SRC}/ssv/mcpl2ssv_app.c")
target_link_libraries(mcpl2ssv ssvmcpl)
if (binaryprops)
  set_target_properties(ssvmcpl PROPERTIES ${binaryprops})
  set_target_properties(ssv2mcpl PROPERTIES ${binaryprops})
  set_target_properties(mcpl2ssv PROPERTIES ${binaryprops})
endif()
install(TARGETS ssv2mcpl mcpl2ssv ssvmcpl ${INSTDEST})
if (BUILD_EXAMPLES)
  install(FILES "${SRCEX}/example_ascii.ssv" "${SRCEX}/example_writessv.ipynb" DESTINATION examples)
endif()



add_subdirectory(tests)

install(DIRECTORY docs mcstas templates DESTINATION .)

if (INSTALL_PY)
	install(DIRECTORY "python/kdsource" DESTINATION python)
endif()
