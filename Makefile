# Much faster, but requires OpenScad snapshot
OPENSCAD="/Applications/OpenSCAD Snapshot.app/Contents/MacOS/OpenSCAD" --enable=manifold

# This will work with the stable openscad
#OPENSCAD="/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD"

# OpenScad options
OPENSCAD_OPTIONS=--export-format binstl
OPENSCAD_CMD=$(OPENSCAD) $(OPENSCAD_OPTIONS)

# Directories
SRC_DIR := src
STL_DIR := stl

# Create targets for files starting with `export_`
EXPORT_SCAD_FILES := $(wildcard $(SRC_DIR)/export_*.scad)

STL_TARGETS := $(patsubst $(SRC_DIR)/export_%.scad,$(STL_DIR)/%.stl,$(EXPORT_SCAD_FILES))

$(STL_DIR)/%.stl: $(SRC_DIR)/export_%.scad $(SRC_DIR)/trackpoint_extension.scad
	@echo "Building $@..."
	$(OPENSCAD_CMD) --render -o $@ $<
	@echo
	@echo

# Default target
all: $(STL_TARGETS)

# Remove generated STL files
clean:
	rm -f $(STL_TARGETS)

# Help target
help:
	@echo "Available targets:"
	@$(foreach target,$(STL_TARGETS),echo "  $(target)";)
