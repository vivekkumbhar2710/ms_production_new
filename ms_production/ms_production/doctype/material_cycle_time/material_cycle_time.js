// Copyright (c) 2023, Abhishek Chougule and contributors
// For license information, please see license.txt

frappe.ui.form.on('Material Cycle Time', {
	// refresh: function(frm) {

	// }
});



frappe.ui.form.on('Material Cycle Time', {
    item: function(frm) {
		frm.clear_table("row_items");
		frm.refresh_field('row_items');

        frm.call({
			method:'set_auto_item_in_row_items',
			doc:frm.doc,
		})
    }
});