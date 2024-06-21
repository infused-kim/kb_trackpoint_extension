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
        adapter_hole_incr=0.2,

        // The width of the adapter around the TP stem
        adapter_width_below_pcb=5.0,
        adapter_width_above_pcb=4.0,

        // By how much you want to increase the tip for a tighter cap fit
        tip_width_incr=0,

        // The thickness of the PCB
        pcb_height=1.6,
        for_kicad=false) {

    adapter_radius_below_pcb = adapter_width_below_pcb / 2;
    adapter_radius_above_pcb = adapter_width_above_pcb / 2;
    adapter_height = (
        tp_mounting_distance + pcb_height + choc_notch_to_pcb_z_space - 0.2
    );

    adapter_hole_width = tp_stem_width + adapter_hole_incr;
    adapter_hole_height = tp_stem_height + adapter_hole_incr;
    adapter_hole_offset = adapter_radius_below_pcb - adapter_hole_width / 2;

    adapter_hole_corner_distance = (
        sqrt(
            adapter_hole_width * adapter_hole_width +
            adapter_hole_width * adapter_hole_width
        ) / 2
    );
    adapter_wall_thickness_below_pcb = (
        adapter_radius_below_pcb - adapter_hole_corner_distance
    );
    adapter_wall_thickness_above_pcb = (
        adapter_radius_above_pcb - adapter_hole_corner_distance
    );
    adapter_wall_thickness_top = adapter_height - adapter_hole_height;

    // Since a portion of the extension adapter will be below the top of the
    // pcb, we calculate the length that it will extend above the pcb here
    adapter_height_below_pcb = pcb_height + tp_mounting_distance;
    adapter_height_above_pcb = adapter_height - adapter_height_below_pcb;

    tip_width = tp_cap_hole_width + tip_width_incr;
    tip_height = tp_cap_hole_height;
    tip_offset = adapter_radius_below_pcb - tip_width / 2;

    // The height added on top of the stem extension. Needed for the total TP
    // extension height
    tp_cap_top_height = tp_cap_height_total - tp_cap_hole_height;

    // Height of the part between the mount at the bottom and tip at the top
    extension_height = (
        desired_cap_height - tp_cap_top_height - tip_height
        - adapter_height_above_pcb
    );

    extension_width = 2;
    extension_offset = adapter_radius_below_pcb - extension_width / 2;

    total_height = adapter_height + extension_height + tip_height;
    above_pcb_height = total_height - adapter_height_below_pcb;
    above_pcb_height_cap = above_pcb_height + tp_cap_top_height;

    center = [false, false, false];

    echo(str("Building TP extension..."));
    echo(str("\t Total height: ", total_height, "mm"));
    echo(str("\t Below PCB height: ", adapter_height_below_pcb, "mm"));
    echo(str("\t Above PCB height: ", above_pcb_height, "mm"));
    echo(str("\t Above PCB height with cap: ", above_pcb_height_cap, "mm"));
    echo(str("\t Adapter height: ", adapter_height, "mm"));
    echo(str("\t Adapter width below pcb: ", adapter_width_below_pcb, "mm"));
    echo(str("\t Adapter width above pcb: ", adapter_width_above_pcb, "mm"));
    echo(str("\t Adapter hole height: ", adapter_hole_height, "mm (+", adapter_hole_height - tp_stem_height, "mm)"));
    echo(str("\t Adapter hole width: ", adapter_hole_width, "mm (+", adapter_hole_width - tp_stem_width, "mm)"));
    echo(str("\t Adapter wall thickness below pcb: ", adapter_wall_thickness_below_pcb, "mm"));
    echo(str("\t Adapter wall thickness above pcb: ", adapter_wall_thickness_above_pcb, "mm"));
    echo(str("\t Adapter wall thickness top: ", adapter_wall_thickness_top, "mm"));

    // Places the upright, centered and moves it to the mounting distance.
    // This makes the visualization in KiCad easier.
    kicad_rotate = for_kicad == true ? [90, 0, 0] : [0, 0, 0];
    kicad_transform = (
        for_kicad == true
        ? [
            -adapter_radius_below_pcb,
            -(tp_mounting_distance + pcb_height),
            -adapter_radius_below_pcb
        ]
        : [0, 0, 0]
    );

    rotate(kicad_rotate)
    translate(kicad_transform)
    union() {
    difference() {

        union() {
            // Adapter below pcb
            translate([adapter_radius_below_pcb, 0, adapter_radius_below_pcb])
            rotate([-90, 0, 0])
                cylinder(
                    $fn=120,
                    h=adapter_height_below_pcb,
                    r=adapter_radius_below_pcb
                );

            // Adapter above pcb
            translate([
                adapter_radius_below_pcb,
                adapter_height_below_pcb,
                adapter_radius_below_pcb
            ])
            rotate([-90, 0, 0])
                cylinder(
                    $fn=120,
                    h=adapter_height_above_pcb,
                    r=adapter_radius_above_pcb
                );
        }

        // Hole
        translate([adapter_hole_offset, -ovb, adapter_hole_offset])
            cube([
                adapter_hole_width,
                adapter_hole_height + ovb,
                adapter_hole_width
            ]);
    };

    // Top extension
    translate([+extension_offset, +adapter_height, +extension_offset])
        cube(
            [extension_width, extension_height, extension_width]
        );

    // Tip for red cap
    translate([+tip_offset, +adapter_height + extension_height, +tip_offset])
        cube([tip_width, tip_height, tip_width]);
    }
}
