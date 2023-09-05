use <export_tp_red_t460s.scad>

tolerance_adjustments = [
    +0.3,
    +0.4,
];

height_adjustments = [
    -1,
    +0,
    +1
    +2,
];

spacing = 6;

sprue_len=2.5;
sprue_radius=0.8;

for (i = [0 : len(tolerance_adjustments) - 1]) {
    tolerance_adjustment = tolerance_adjustments[i];

    for (j = [0 : len(height_adjustments) - 1]) {
        height_adjustment = height_adjustments[j];

        spacing_offset = (i * len(height_adjustments) + j) * spacing;
        translate([spacing_offset, 0, 0])
            draw_tp_ext_red_t460s(
                tolerance_adjustment,
                height_adjustment
            );
    }

    count = len(tolerance_adjustments) * len(height_adjustments);
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
