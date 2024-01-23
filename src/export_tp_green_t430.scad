use <trackpoint_extension.scad>

// WARNING: WRONG HEAD USED HERE -- HEAD OF RED S460

/*
 * Parameters
 */

// The height above the pcb where you want the top of the red cap to be
desired_cap_height_default = 11;

// By how much you want to increase the adapter hole compared to the
// actual TP stem width
adapter_hole_incr_default = 0.5;

// Thickness of the pcb
pcb_height_default = 1.6;

// How far the TP is mounted BELOW the PCB.
// This should include the thickness of any plastic or electrical tape you use
// to isolate the TP mount.
// This TP is super large, so it will be at least 0.5mm below the pcb
tp_mounting_distance_default = 0.5;

// By how much you want to increase the tip for a tighter cap fit
tip_width_incr_default = 0;


/*
 * TP Measurements
 */

// From bottom metal part to stem top
tp_total_height = 5.0;

// The metal and black bottom part.
// This is the height that sticks out below the pcb if the
// TP is mounted totally flush.
tp_board_thickness = 2.5;

// The height of the white stem
// (2.5mm)
tp_stem_height = tp_total_height - tp_board_thickness;

// TP white stem dimensions
tp_stem_width = 2.2;
tp_stem_diameter = 3.0;

// TP dot dimensions
tp_cap_height_total = 4.0;
tp_cap_hole_height = 3.0;

// But it could fit 3.0 for a tighter fit
tp_cap_hole_width = 2.5;


module draw_tp_ext_green_t430(
        desired_cap_height=desired_cap_height_default,
        tp_mounting_distance=tp_mounting_distance_default,
        adapter_hole_incr=adapter_hole_incr_default,
        tip_width_incr=tip_width_incr_default,
        pcb_height=pcb_height_default) {

    draw_trackpoint_extension(
        desired_cap_height=desired_cap_height,

        // How far below the pcb the TP is mounted (from start of the stem)
        tp_mounting_distance=tp_mounting_distance,

        // The measured width and height of the TP stem
        tp_stem_width=tp_stem_width,
        tp_stem_height=tp_stem_height,

        // The red cap dimensions
        tp_cap_height_total=tp_cap_height_total,
        tp_cap_hole_height=tp_cap_hole_height,
        tp_cap_hole_width=tp_cap_hole_width,

        // By how much you want to increase the adapter hole compared to the
        // actual TP stem width
        adapter_hole_incr=adapter_hole_incr,

        // By how much you want to increase the tip for a tighter cap fit
        tip_width_incr=tip_width_incr,

        // The thickness of the PCB
        pcb_height=pcb_height
    );
}

draw_tp_ext_green_t430();