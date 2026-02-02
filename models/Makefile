# TODO: customize the project here
CPPC=RBRBR_CPPC_RBRBRBR
CPPC_VERSION_OPTION=RBRBR_CPPC_VERSION_OPTION_RBRBRBR
CPPC_VERSION_DIRECTORY=RBRBR_CPPC_VERSION_DIRECTORY_RBRBRBR
MODULE_FILENAME=RBRBRBR_MODULE_FILENAME_RBRBRBR
MODULE_DIRECTORY_TREE=RBRBRBR_MODULE_DIRECTORY_TREE_RBRBRBR


DIRECTORY_BASE=..
DIRECTORY_PRIVATE=$(MODULE_FILENAME)/private
DIRECTORY_PUBLIC=$(MODULE_FILENAME)/public

FILES_DIRECTORY_PRIVATE=$(DIRECTORY_PRIVATE)/$(MODULE_DIRECTORY_TREE)
FILES_DIRECTORY_PUBLIC=$(DIRECTORY_PUBLIC)/$(MODULE_DIRECTORY_TREE)

# TODO: Enter the files here
#   remember that "../" will be prepended as the Makefile is inside a directory
#       inside the root
#   so you need to put the full path from there.
HEADERS_LIST=$(FILES_DIRECTORY_PRIVATE)/main.hpp
SOURCES_LIST=$(FILES_DIRECTORY_PRIVATE)/main.cpp

PATH_HEADERS_LIST=$(foreach file,$(HEADERS_LIST),$(DIRECTORY_BASE)/$(file))
PATH_SOURCES_LIST=$(foreach file,$(SOURCES_LIST),$(DIRECTORY_BASE)/$(file))


# macro definitions
CPPC_CFLAGS=-c -Wall -Wextra -pedantic $(CPPC_VERSION_OPTION)
CPPC_LFLAGS=
PATH_DIRECTORY_OBJ=$(DIRECTORY_BASE)/__obj/$(MODULE_FILENAME)/$(CPPC_VERSION_DIRECTORY)
PATH_DIRECTORY_BIN=$(DIRECTORY_BASE)/__bin/$(CPPC_VERSION_DIRECTORY)
PROJECT_EXE=$(MODULE_FILENAME).exe

INCLUDES_ALL=-I$(DIRECTORY_BASE)/$(DIRECTORY_PUBLIC) -I$(DIRECTORY_BASE)/$(DIRECTORY_PRIVATE)

OBJECTS_LIST=$(subst .cpp,.obj,$(SOURCES_LIST))
PATH_OBJECTS_LIST=$(foreach file,$(OBJECTS_LIST),$(PATH_DIRECTORY_OBJ)/$(file))



all: do_lines create_directories object_files executable_file launching_executable_file



.PHONY: clean
clean:
	@rm -f $(PATH_DIRECTORY_BIN)/$(PROJECT_EXE) $(PATH_OBJECTS_LIST)



do_lines :
	$(info )
	$(info )
	$(info )
	$(info )
	$(info )
	$(info )
	$(info )
	$(info )
	$(info )
	$(info )
	$(info )
	$(info )
	$(info )
	$(info )
	$(info )
	$(info )
	$(info )
	$(info )
	$(info )
	$(info ==========================================================)



create_directories :
	@mkdir -p $(PATH_DIRECTORY_OBJ)/$(FILES_DIRECTORY_PRIVATE)
	@mkdir -p $(PATH_DIRECTORY_OBJ)/$(FILES_DIRECTORY_PUBLIC)
	@mkdir -p $(PATH_DIRECTORY_BIN)
	$(info )



launching_executable_file :
	$(info )
	$(info ==========================================================)
	$(info )
	$(info EXECUTING $(PATH_DIRECTORY_BIN)/$(PROJECT_EXE))
	$(info )
	$(info ==========================================================)
	$(info )
	@$(PATH_DIRECTORY_BIN)/$(PROJECT_EXE)



executable_file : $(PATH_DIRECTORY_BIN)/$(PROJECT_EXE)



$(PATH_DIRECTORY_OBJ)/%.obj : $(DIRECTORY_BASE)/%.cpp $(PATH_HEADERS_LIST)
#	$(info TARGET="$@")
#	$(info PREREQ="$<")
#	$(info PATH_DIRECTORY_OBJ="$(PATH_DIRECTORY_OBJ)")
	$(info COMPILING $<)
	$(info )
	@$(CPPC) $(CPPC_CFLAGS) $(INCLUDES_ALL) $< -o $@



object_files : $(PATH_OBJECTS_LIST)
	$(info )



$(PATH_DIRECTORY_BIN)/$(PROJECT_EXE) : $(PATH_OBJECTS_LIST)
	$(info LINKING $<)
	$(info )
	$(CPPC) $(CPPC_LFLAGS) $^ -o $@


	
$(DIRECTORY_BASE)/%.cpp : 
	$(info )
