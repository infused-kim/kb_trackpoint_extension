use <export_tp_green_t430.scad>

/*
 * Config Parameters
 */

add_spruces = true;
desired_cap_height = 11;

desired_cap_heights = [
    desired_cap_height - 1,
    desired_cap_height,
    desired_cap_height + 1,
];

adapter_hole_increases = [
    +0.2,
    +0.5,
    +0.7,
    +0.9,
    +1.1,
];

/*
 * Script Settings
 */

spacing = 6;
sprue_len=4;
sprue_radius=0.8;

for (i = [0 : len(desired_cap_heights) - 1]) {
    desired_cap_height = desired_cap_heights[i];

    for (j = [0 : len(adapter_hole_increases) - 1]) {
        adapter_hole_incr = adapter_hole_increases[j];
        spacing_offset = (i * len(adapter_hole_increases) + j) * spacing;
        translate([spacing_offset, 0, 0])
            draw_tp_ext_green_t430(
                adapter_hole_incr=adapter_hole_incr,
                desired_cap_height=desired_cap_height
            );
    }

    if(add_spruces) {
        count = len(desired_cap_heights) * len(adapter_hole_increases);
        for (i = [0 : count - 2]) {
            translate([
                (i + 1) * spacing - 2,
                +2.5,
                - 0.9 * sprue_radius
            ])
                rotate ([0, 90, 0])
                    cylinder(
                        h = sprue_len,
                        r = sprue_radius,
                        $fn=15
                    );
        }
    }
}
