.DEFAULT_GOAL := help

EXPORT_DIR := exports
RELEASE_DIR := $(EXPORT_DIR)/release
RELEASE_PATH := $(RELEASE_DIR)/<tp_model>/tp_extension_<tp_model>_<parameters>.<format>

TRACKPOINT_MODELS_VALUES := red_t460s green_t430 blue_x1_carbon
MOUNTING_DISTANCE_VALUES := 0.5 2.0
ADAPTER_HOLE_INCREASE_VALUES := 0.1 0.2 0.3 0.4 0.5

release:
	@for tp in $(TRACKPOINT_MODELS_VALUES); do \
		for mounting_distance in $(MOUNTING_DISTANCE_VALUES); do \
			for hole_increase in $(ADAPTER_HOLE_INCREASE_VALUES); do \
				./tp_extension_builder/cli.py build $$tp -e "exports/release/<tp_model>/tp_extension_<tp_model>_<parameters>.<format>" --overwrite --mounting-distance $$mounting_distance --adapter-hole-increase $$hole_increase; \
			done; \
		done; \
	done
	@for tp in $(TRACKPOINT_MODELS_VALUES); do \
		./tp_extension_builder/cli.py combine -f stl -e "exports/release/$${tp}/tp_extension_$${tp}_combined.<format>" --overwrite "exports/release/$${tp}/"*.step; \
		./tp_extension_builder/cli.py combine -f step -e "exports/release/$${tp}/tp_extension_$${tp}_combined.<format>" --overwrite  "exports/release/$${tp}/"*.step; \
	done
	@for tp in $(TRACKPOINT_MODELS_VALUES); do \
		for mounting_distance in $(MOUNTING_DISTANCE_VALUES); do \
			./tp_extension_builder/cli.py build-kicad-model $$tp -e "exports/release/kicad_models/tp_extension_<tp_model>_<parameters>.<format>" --overwrite --mounting-distance $$mounting_distance; \
		done; \
	done

clean:
	find $(RELEASE_DIR) -type f \( -name "*.stl" -o -name "*.step" -o -name "*.log" \) -exec rm -f {} +
	find $(RELEASE_DIR) -type d -empty -delete

help:
	@echo "Usage:"
	@echo "  make release  - Run the release commands with varying parameters."
	@echo "  make clean    - Remove generated files."
