use <trackpoint_extension.scad>
include <parameter_defaults.scad>

/*
 * Override Parameter Defaults
 */

// How far the TP is mounted BELOW the PCB.
// This should include the thickness of any plastic or electrical tape you use
// to isolate the TP mount.
// This TP is super large, so it will be at least 0.5mm below the pcb
tp_mounting_distance_default = 0.5;

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
tp_cap_height_total = 6.0;
tp_cap_hole_height = 5.0;
tp_cap_hole_width = tp_stem_width;


module draw_tp_ext_green_t430(
        desired_cap_height=desired_cap_height_default,
        tp_mounting_distance=tp_mounting_distance_default,
        adapter_hole_incr=adapter_hole_incr_default,
        adapter_width_below_pcb=adapter_width_below_pcb_default,
        adapter_width_above_pcb=adapter_width_above_pcb_default,
        tip_width_incr=tip_width_incr_default,
        pcb_height=pcb_height_default,
        for_kicad=for_kicad_default) {

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

        // The width of the adapter around the TP stem
        adapter_width_below_pcb=adapter_width_below_pcb,
        adapter_width_above_pcb=adapter_width_above_pcb,

        // By how much you want to increase the tip for a tighter cap fit
        tip_width_incr=tip_width_incr,

        // The thickness of the PCB
        pcb_height=pcb_height,

        // Orientate the extension for visualization in KiCad
        for_kicad=for_kicad
    );
}

// Allow inclusion of this file without running if do_not_run is set to true
// before the inclusion
if(is_undef(do_not_run) || do_not_run == false) {
    draw_tp_ext_green_t430();
}
