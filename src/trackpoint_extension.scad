
// Overlap Buffer for cutting
ovb = 0.01;

module draw_trackpoint_extension(stem_width, stem_height, extension_height, wall_thickness=1, tolerance_adjustment=0) {

    echo(str("Building TP extension with ", extension_height, "mm height"));

    stem_adapter_w = stem_width + wall_thickness * 2 + tolerance_adjustment;
    stem_adapter_h = stem_height + wall_thickness + tolerance_adjustment;

    hole_w = stem_width + tolerance_adjustment;
    hole_h = stem_height + tolerance_adjustment;
    hole_offset = (stem_adapter_w - hole_w) / 2;

    extension_w = stem_width;
    extension_h = extension_height - stem_adapter_h;
    extension_offset = (stem_adapter_w - extension_w) / 2;

    // Top extension
    translate([+extension_offset, +stem_adapter_h, +extension_offset])
        cube([extension_w, extension_h, extension_w]);

    difference() {
        // Adapter
        translate([0, 0, 0])
            cube([stem_adapter_w, stem_adapter_h, stem_adapter_w]);

        // Hole
        translate([hole_offset, -ovb, hole_offset])
            cube([hole_w, hole_h + ovb, hole_w]);
    };
}
