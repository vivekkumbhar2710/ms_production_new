// Copyright (c) 2023, Abhishek Chougule and contributors
// For license information, please see license.txt

frappe.ui.form.on('Job Order', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Job Order', {
	production_schedule(frm,cdt,cdn) {

		frm.clear_table("raw_item");
		frm.refresh_field('raw_item');
		frm.call({
			method:'set_data_raw_item',
			doc:frm.doc,
		})
	},
});


frappe.ui.form.on("Job Order", {
    refresh: function(frm) {
            frm.set_query("production_schedule", function() { // Replace with the name of the link field
                return {
                    filters: [
                        ["Production Schedule", "docstatus", '=', 1],
						["Production Schedule", "item", '=', frm.doc.item],
						["Production Schedule", "company", '=', frm.doc.company]  // Replace with your actual filter criteria
                    ]
                };
            });
        }
    });

	frappe.ui.form.on("Job Order", {
		refresh: function(frm) {
				frm.set_query("target_warehouse", function() { // Replace with the name of the link field
					return {
						filters: [
							["Warehouse", "company", '=', frm.doc.company], // Replace with your actual filter criteria
						]
					};
				});
				frm.set_query("source_warehouse", function() { // Replace with the name of the link field
					return {
						filters: [
							["Warehouse", "company", '=', frm.doc.company], // Replace with your actual filter criteria
						]
					};
				});
				frm.set_query("cr_warehouse", function() { // Replace with the name of the link field
					return {
						filters: [
							["Warehouse", "company", '=', frm.doc.company], // Replace with your actual filter criteria
						]
					};
				});
				frm.set_query("mr_warehouse", function() { // Replace with the name of the link field
					return {
						filters: [
							["Warehouse", "company", '=', frm.doc.company], // Replace with your actual filter criteria
						]
					};
				});
				frm.set_query("rw_warehouse", function() { // Replace with the name of the link field
					return {
						filters: [
							["Warehouse", "company", '=', frm.doc.company], // Replace with your actual filter criteria
						]
					};
				});
			}
		});