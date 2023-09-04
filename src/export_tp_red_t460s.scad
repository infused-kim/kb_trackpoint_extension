use <trackpoint_extension.scad>

// Parameters
wall_thickness = 1;
tolerance_adjustment = 0;
height_adjustment=0;

// TP Stem dimensions
stem_width = 2.2;
stem_height = 2.7;

// TP dot dimensions
tp_dot_height_total = 4;
tp_dot_height_hole = 2.8;
tp_dot_height = tp_dot_height_total - tp_dot_height_hole;

// Height from pcb bottom to choc keycap top
keycap_height = 12.5;

// The final desired height for the extension
extension_height = keycap_height - tp_dot_height;

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
