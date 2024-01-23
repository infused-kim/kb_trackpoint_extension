// Adds multiple stl into one file and then connects them with
// cylinder sprues for cost-effective printing at JLCPCB

stl_array = ["../stl/tp_green_t430.stl", "../stl/tp_red_t460s.stl"];
spacing_default = 8;
sprue_len_default = 2;
sprue_radius_default=0.8;

module gen_sprues(count, spacing=spacing_default, sprue_len=sprue_len_default, sprue_radius=sprue_radius_default) {

        for (i = [0 : count - 1]) {
            translate([
                i * (spacing) + sprue_len,
                1,
                - 0.9 * sprue_radius
            ])
                rotate ([0, 90, 0])
                    cylinder(
                        h = spacing,
                        r = sprue_radius,
                        $fn=15
                    );
        }
}

module combine_stl(stl_array, spacing=spacing_default, sprue_len=sprue_len_default, sprue_radius=sprue_radius_default) {

    assert(len(stl_array) > 0);

    echo(str("\t Combining: ", stl_array, ""));

    union() {
        for (i = [0 : len(stl_array) - 1]) {
            stl = stl_array[i];
            translate([i * spacing, 0, 0]) import(stl);
        }

        gen_sprues(len(stl_array) - 1, spacing=spacing, sprue_len=sprue_len, sprue_radius=sprue_radius);
    };
}

combine_stl(
    stl_array=stl_array,
    spacing=spacing_default,
    sprue_len=sprue_len_default,
    sprue_radius=sprue_radius_default
);
