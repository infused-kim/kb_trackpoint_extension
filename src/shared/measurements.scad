

/*
 * Keyboard Measurements
 */

pcb_thickness = 1.6;

// The plastic used to cover the TP mount's metal part to make
// sure it doesn't short the switch pins.
tp_isolator_thickness = 0.4;




/*
 * Kailh Choc Switch Measurements
 * http://www.kailh.com/uploads/allimg/171208/2-1G20Q0432C29.png
 */

// The width of the choc switch where it touches the bottom plate
choc_width_bottom = 13.6;

// The width of the choc switch with the notch that sits above the top plate
choc_width_notch = 15.0;

// How much the notch adds in width on each side
// (0.7mm)
choc_notch_width = (choc_width_notch - choc_width_bottom) / 2;

// The space from the pcb until the choc switch notch
choc_notch_to_pcb_z_space = 2.2;

// Total x distance between switch center points (choc x spacing)
choc_spacing_x = 18;

// The space between two switches at the bottom plate
// (4.4mm)
choc_switches_space_between_bottom = choc_spacing_x - choc_width_bottom;

// The space between two switches at the top with the little notch
// (3mm)
choc_switches_space_between_top = choc_spacing_x - choc_width_notch;
