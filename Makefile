#
# Setup
#

# Much faster, but requires OpenScad snapshot
OPENSCAD="/Applications/OpenSCAD Snapshot.app/Contents/MacOS/OpenSCAD" --enable=manifold

# This will work with the stable openscad
#OPENSCAD="/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD"

#
# Parameters
#

# By how much you want to increase the adapter hole compared to the
# actual TP stem width.
# Sets the parameter `adapter_hole_incr_default`
HOLE_INCR ?= 0

# How wide the adapter should be below and above the pcb.
# Pay attention to the adapter wall thickness calculations in the logs to
# ensure it is thick enough to withstand the pressure of the TP.
#
# You also need to consider the size of your TP hole, as well as how much your
# switches are going to protrude into the hole.
#
# Sets the parameter `adapter_width_below_pcb` and `adapter_width_above_pcb`
ADAPTER_WIDTH_BOTTOM ?= 0
ADAPTER_WIDTH_TOP ?= 0

# The height from the pcb to where you want the cap to end.
# Sets the parameter `desired_cap_height`
HEIGHT ?= 0

# How far the TP is mounted BELOW the PCB.
# This should include the thickness of any plastic or electrical tape you use
# to isolate the TP mount.
# Sets the parameter `tp_mounting_distance_default`
MOUNTING_DISTANCE ?= 0

# Thickness of the pcb (1.6mm by default)
# Sets the parameter `pcb_height_default`
PCB_HEIGHT ?= 0

# By how much you want to increase the tip for a tighter cap fit.
# Sets the parameter `tip_width_incr_default`
TIP_INCR ?= 0

#
# Don't change below
#

.DEFAULT_GOAL := help

ifeq ($(HOLE_INCR),0)
  HOLE_INCR_VAL=
  HOLE_INCR_FNAME=
else
  HOLE_INCR_VAL=-D adapter_hole_incr_default=$(HOLE_INCR)
  HOLE_INCR_FNAME=_hw$(HOLE_INCR)
endif

ifeq ($(ADAPTER_WIDTH_BOTTOM),0)
  ADAPTER_WIDTH_BOTTOM_VAL=
  ADAPTER_WIDTH_BOTTOM_FNAME=
else
  ADAPTER_WIDTH_BOTTOM_VAL=-D adapter_width_below_pcb_default=$(ADAPTER_WIDTH_BOTTOM)
  ADAPTER_WIDTH_BOTTOM_FNAME=_awb$(ADAPTER_WIDTH_BOTTOM)
endif

ifeq ($(ADAPTER_WIDTH_TOP),0)
  ADAPTER_WIDTH_TOP_VAL=
  ADAPTER_WIDTH_TOP_FNAME=
else
  ADAPTER_WIDTH_TOP_VAL=-D adapter_width_above_pcb_default=$(ADAPTER_WIDTH_TOP)
  ADAPTER_WIDTH_TOP_FNAME=_awt$(ADAPTER_WIDTH_TOP)
endif

ifeq ($(HEIGHT),0)
  HEIGHT_VAL=
  HEIGHT_FNAME=
else
  HEIGHT_VAL=-D desired_cap_height_default=$(HEIGHT)
  HEIGHT_FNAME=_h$(HEIGHT)
endif

ifeq ($(MOUNTING_DISTANCE),0)
  MOUNTING_DISTANCE_VAL=
  MOUNTING_DISTANCE_FNAME=
else
  MOUNTING_DISTANCE_VAL=-D tp_mounting_distance_default=$(MOUNTING_DISTANCE)
  MOUNTING_DISTANCE_FNAME=_md$(MOUNTING_DISTANCE)
endif

ifeq ($(PCB_HEIGHT),0)
  PCB_HEIGHT_VAL=
  PCB_HEIGHT_FNAME=
else
  PCB_HEIGHT_VAL=-D pcb_height_default=$(PCB_HEIGHT)
  PCB_HEIGHT_FNAME=_pcb$(PCB_HEIGHT)
endif

ifeq ($(TIP_INCR),0)
  TIP_INCR_VAL=
  TIP_INCR_FNAME=
else
  TIP_INCR_VAL=-D tip_width_incr_default=$(TIP_INCR)
  TIP_INCR_FNAME=_t$(TIP_INCR)
endif

PARAMS = $(HEIGHT_VAL) $(MOUNTING_DISTANCE_VAL) $(PCB_HEIGHT_VAL) $(HOLE_INCR_VAL) $(TIP_INCR_VAL) $(ADAPTER_WIDTH_BOTTOM_VAL) $(ADAPTER_WIDTH_TOP_VAL)
FNAME_POSTFIX = $(HEIGHT_FNAME)$(MOUNTING_DISTANCE_FNAME)$(PCB_HEIGHT_FNAME)$(ADAPTER_WIDTH_BOTTOM_FNAME)$(ADAPTER_WIDTH_TOP_FNAME)$(HOLE_INCR_FNAME)$(TIP_INCR_FNAME)

# Pathes for combined
COMBINED_STL_ARRAY=[]

# OpenScad options
OPENSCAD_OPTIONS=--export-format binstl
OPENSCAD_CMD=$(OPENSCAD) $(OPENSCAD_OPTIONS)

# Directories
SRC_DIR := src
STL_DIR := stl/output
LOG_DIR=$(STL_DIR)/logs

# Create targets for files starting with `export_`
EXPORT_SCAD_FILES := $(wildcard $(SRC_DIR)/export_*.scad)

STL_TARGETS := $(patsubst $(SRC_DIR)/export_%.scad,%,$(EXPORT_SCAD_FILES))

all: $(STL_TARGETS) combined

%: $(SRC_DIR)/export_%.scad $(SRC_DIR)/trackpoint_extension.scad
	@output_file="$(STL_DIR)/$@$(FNAME_POSTFIX).stl"; \
	log_file="$(LOG_DIR)/$@$(FNAME_POSTFIX).log"; \
	mkdir -p "$(STL_DIR)" "$(LOG_DIR)"; \
	echo "Building $$output_file..."; \
	echo "> $(OPENSCAD_CMD) $(PARAMS) --render -o $$output_file $<\n" | tee $$log_file; \
	$(OPENSCAD_CMD) $(PARAMS) --render -o $$output_file $< 2>&1 | tee -a $$log_file; \
	echo; \
	echo

combined:
	@echo "Building $@..."
	$(eval COMBINED_STL_ARRAY:=$(shell bash -c 'printf "["; for file in "$(STL_DIR)"/*.stl; do if [ "$$file" != "$(STL_DIR)/tp_ext_combined.stl" ] && [ -e "$$file" ]; then printf "\\\"../%s\\\", " "$$file"; fi; done | sed "s/, $$//"; printf "]"'))
	$(OPENSCAD_CMD) $(PARAMS) --render -D stl_array='$(COMBINED_STL_ARRAY)' -o $(STL_DIR)/tp_ext_combined.stl $(SRC_DIR)/stl_combiner.scad
	@echo
	@echo

# Remove generated STL files
clean:
	rm -f $(STL_DIR)/*.stl
	rm -f $(LOG_DIR)/*.log

# Help target
help: help-text targets

help-text:
	@echo "Help:"
	@echo
	@echo "  You can customize the output using the following parameters with any of the targets below..."
	@echo
	@echo "  To see the available targets run:"
	@echo "    make targets"
	@echo
	@echo "  And then to run a target:"
	@echo "    make tp_red_t460s HOLE_INCR=0.2 HEIGHT=10.5"
	@echo
	@echo "  You can also run multiple targets with the same parameters at once:"
	@echo "    make tp_red_t460s tp_green_t430 HOLE_INCR=0.2 HEIGHT=10.5"
	@echo
	@echo "  Or you can build all targets with:"
	@echo "    make all HOLE_INCR=0.2 HEIGHT=10.5"
	@echo
	@echo "Parameters:"
	@echo
	@echo "  HOLE_INCR=0.2"
	@echo "    By how much you want to increase the adapter hole compared to the actual TP stem width."
	@echo
	@echo "  ADAPTER_WIDTH_BOTTOM=5 ADAPTER_WIDTH_TOP=4"
	@echo "    The width of the stem adapter below and above the PCB."
	@echo
	@echo "  HEIGHT=10.5"
	@echo "    The height from the pcb to where you want the cap to end."
	@echo
	@echo "  MOUNTING_DISTANCE=1.0"
	@echo "    How far the TP is mounted BELOW the PCB. This should include the thickness of any plastic or electrical tape you use to isolate the TP mount."
	@echo
	@echo "  PCB_HEIGHT=1.6"
	@echo "    Thickness of the pcb."
	@echo
	@echo "  TIP_INCR=0.3"
	@echo "    By how much you want to increase the tip for a tighter cap fit."
	@echo

targets:
	@echo "Available targets:"
	@$(foreach target,$(STL_TARGETS),echo "  $(target)";)
	@echo
	@echo "  combined"
	@echo "    Combines all .stl files in $(STL_DIR) into one stl with sprues for printing at JLC3DP."
	@echo
	@echo "  all"
	@echo "    Runs all targets (including combined)"
	@echo
	@echo "  clean"
	@echo "    Removes all .stl and .log files from $(STL_DIR)."
	@echo
