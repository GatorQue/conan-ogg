#.rst:
# FindOgg
# --------
#
# Find ogg
#
# Find the ogg libraries
#
# ::
#
#   This module defines the following variables:
#      OGG_FOUND       - True if OGG_INCLUDE_DIR & OGG_LIBRARY are found
#      OGG_LIBRARIES   - Set when OGG_LIBRARY is found
#      OGG_INCLUDE_DIRS - Set when OGG_INCLUDE_DIR is found
#
#
#
# ::
#
#      OGG_INCLUDE_DIR - where to find asoundlib.h, etc.
#      OGG_LIBRARY     - the asound library

find_path(OGG_INCLUDE_DIR NAMES ogg/ogg.h
          DOC "The OGG include directory"
)

find_library(OGG_LIBRARY NAMES ogg
          DOC "The OGG library"
)

# handle the QUIETLY and REQUIRED arguments and set OGG_FOUND to TRUE if
# all listed variables are TRUE
include(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(OGG
                                  REQUIRED_VARS OGG_LIBRARY OGG_INCLUDE_DIR)

if(OGG_FOUND)
  set( OGG_LIBRARIES ${OGG_LIBRARY} )
  set( OGG_INCLUDE_DIRS ${OGG_INCLUDE_DIR} )
endif()

mark_as_advanced(OGG_INCLUDE_DIR OGG_LIBRARY)
