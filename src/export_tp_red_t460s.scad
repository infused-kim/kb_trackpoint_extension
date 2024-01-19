use <trackpoint_extension.scad>
use <shared/measurements.scad>

/*
 * TP Measurements
 */

// The metal and black bottom part.
// This is the height that sticks out below the pcb if the
// TP is mounted totally flush.
tp_board_thickness = 1.3;

// From bottom metal part to stem top
tp_total_height = 4.0;

// The height of the white stem
// (2.7mm)
tp_stem_height = tp_total_height - tp_board_thickness;

// How much the TP stem hangs out above the PCB when the TP is mounted
// flush to the bottom of the PCB.
// (0.7mm)
tp_stem_height_above_pcb = tp_stem_height - tp_isolator_thickness -  pcb_thickness;

tp_stem_height_below_pcb = tp_stem_height - tp_stem_height_above_pcb;

// TP white stem dimensions
tp_stem_width = 2.2;
tp_stem_diameter = 3.0;

// TP dot dimensions
tp_dot_height_total = 4.0;
tp_dot_hole_height = 3.0;

// But it could fit 3.0 for a tighter fit
tp_dot_hole_width = 2.5;

// The height added on top of the stem extension for the total TP height
// (1mm)
tp_dot_top_height = tp_dot_height_total - tp_dot_hole_height;


/*
 * Mount Parameters - The extension part that attaches to the TP stem
 */

// (2.2mm + x)
mount_hole_width = tp_stem_width + 0.5;

// (2.7mm + x)
mount_hole_height = tp_stem_height + 0.5;

// (4.4mm)
mount_width = switches_space_between_bottom;

// (2 + 2.2 - 2 = 4.0mm)
mount_height = tp_stem_height_below_pcb + choc_notch_to_pcb_z_space - 0.2;

// (~0.65 - 0.85mm)
mount_wall_thickness_sides = (mount_width - mount_hole_width) / 2;

// (~0.8mm)
mount_wall_thickness_top = mount_height - mount_hole_height;

// How high the extension extends above the pcb
mount_above_pcb_height = mount_height - tp_stem_height_below_pcb;

/*
 * Tip Parameters
 */

tip_width = tp_dot_hole_width + 0.5;
tip_height = tp_dot_hole_height;

/*
 * Extension Parameters
 */

// Where you want the red dot to end up
extension_total_height_above_pcb = 11;

// Height of the part between the mount at the bottom and tip at the top
extension_height = extension_total_height_above_pcb - tp_dot_top_height - tip_height - mount_above_pcb_height;

// Width of the extension
extension_width = 2.5;


module draw_tp_ext_red_t460s(tolerance_adjustment=tolerance_adjustment, height_adjustment=height_adjustment, wall_thickness=wall_thickness) {

    draw_trackpoint_extension(
        stem_width,
        stem_height,
        extension_height + height_adjustment,
        wall_thickness=wall_thickness,
        tolerance_adjustment=tolerance_adjustment
    );
}

draw_tp_ext_red_t460s(tolerance_adjustment, height_adjustment, wall_thickness);
