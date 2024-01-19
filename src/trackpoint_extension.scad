include <shared/measurements.scad>

// Overlap Buffer for cutting
ovb = 0.01;

module draw_trackpoint_extension(
        // The height from the pcb to where you want the cap to end
        desired_cap_height,

        // How far below the pcb the TP is mounted (from start of the stem)
        tp_mounting_distance,

        // The measured width and height of the TP stem
        tp_stem_width,
        tp_stem_height,

        // The red cap dimensions
        tp_cap_height_total,
        tp_cap_hole_height,
        tp_cap_hole_width,

        // By how much you want to increase the adapter hole compared to the
        // actual TP stem width
        adapter_hole_incr=0.5,

        // By how much you want to increase the tip for a tighter cap fit
        tip_width_incr=0,

        // The thickness of the PCB
        pcb_height=1.6) {

    echo(str("Building TP extension with ", extension_height, "mm height"));

    adapter_width = choc_switches_space_between_bottom;
    adapter_height = tp_mounting_distance + pcb_height + choc_notch_to_pcb_z_space - 0.2;

    adapter_hole_width = tp_stem_width + adapter_hole_incr;
    adapter_hole_height = tp_stem_height + adapter_hole_incr;
    adapter_hole_offset = (adapter_width - adapter_hole_width) / 2;

    // Since a portion of the extension adapter will be below the top of the
    // pcb, we calculate the length that it will extend above the pcb here
    adapter_above_pcb_height = adapter_height - pcb_height - tp_mounting_distance;

    tip_width = tp_cap_hole_width + tip_width_incr;
    tip_height = tp_cap_hole_height;
    tip_offset = (adapter_width - tip_width) / 2;

    // The height added on top of the stem extension. Needed for the total TP
    // extension height
    tp_cap_top_height = tp_cap_height_total - tp_cap_hole_height;

    // Height of the part between the mount at the bottom and tip at the top
    extension_height = desired_cap_height - tp_cap_top_height - tip_height - adapter_above_pcb_height;

    // Width of the extension (maximum possible on choc switches)
    extension_width = choc_switches_space_between_top;
    extension_offset = (adapter_width - extension_width) / 2;

    difference() {
        // Adapter
        translate([0, 0, 0])
            cube([adapter_width, adapter_height, adapter_width]);

        // Hole
        translate([adapter_hole_offset, -ovb, adapter_hole_offset])
            cube([adapter_hole_width, adapter_hole_height + ovb, adapter_hole_width]);
    };

    // Top extension
    translate([+extension_offset, +adapter_height, +extension_offset])
        cube([extension_width, extension_height, extension_width]);

    // Tip for red cap
    translate([+tip_offset, +adapter_height + extension_height, +tip_offset])
        cube([tip_width, tip_height, tip_width]);

}
