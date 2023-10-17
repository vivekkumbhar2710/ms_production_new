// Copyright (c) 2023, Abhishek Chougule and contributors
// For license information, please see license.txt

frappe.ui.form.on('Production Schedule', {
	// refresh: function(frm) {

	// }
});


frappe.ui.form.on('Production Schedule', {
	material_cycle_time(frm,cdt,cdn) {
		frm.call({
			method:'calculate_total_time',
			doc:frm.doc,
		})
	},
});

frappe.ui.form.on('Production Schedule', {
	total_quantity_of_production(frm,cdt,cdn) {
		frm.call({
			method:'calculate_total_time',
			doc:frm.doc,
		})
	},
});

frappe.ui.form.on('Production Schedule', {
	shift_time(frm,cdt,cdn) {
		frm.call({
			method:'validate_shift',
			doc:frm.doc,
		})
	},
});

frappe.ui.form.on("Production Schedule", {
    refresh: function(frm) {
            frm.set_query("material_cycle_time", function() { // Replace with the name of the link field
                return {
                    filters: [
                        ["Material Cycle Time", "item", '=', frm.doc.item],
						["Material Cycle Time", "company", '=', frm.doc.company] // Replace with your actual filter criteria
                    ]
                };
            });
        }
    });