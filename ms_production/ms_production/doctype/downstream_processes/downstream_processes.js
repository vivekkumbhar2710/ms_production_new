// Copyright (c) 2023, Abhishek Chougule and contributors
// For license information, please see license.txt

frappe.ui.form.on('Downstream Processes', {
	// refresh: function(frm) {

	// }
});


frappe.ui.form.on('Downstream Processes', {
    refresh: function(frm) {
        $('.layout-side-section').hide();
    }
});

frappe.ui.form.on('Downstream Processes', {
    button: function(frm) {

        frm.call({
			method:'test_method',
			doc:frm.doc,
		})
        frm.refresh_field('raw_items')
    }
});


//abc
// ============================================================= Downstream Processes =================================================


frappe.ui.form.on('Downstream Processes', {
    production: function(frm) {
		frm.clear_table("items");
		frm.refresh_field('items');
		frm.clear_table("raw_items");
		frm.refresh_field('raw_items');
        frm.clear_table("qty_details");
		frm.refresh_field('qty_details');
        frm.call({
			method:'method_to_set_data_in_table',
			doc:frm.doc,
		})
    }
});

frappe.ui.form.on('Downstream Processes', {
    downstream_process: function(frm) {

        if (frm.doc.production && frm.doc.production.length > 0) {
		frm.clear_table("items");
		frm.refresh_field('items');
		frm.clear_table("raw_items");
		frm.refresh_field('raw_items');
        frm.clear_table("qty_details");
		frm.refresh_field('qty_details');
        frm.call({
			method:'method_to_set_data_in_table',
			doc:frm.doc,
		})
    }
    }
});


frappe.ui.form.on('Downstream Processes', {
    get_rejected_item: function(frm) {

        frm.clear_table("rejected_items_reasons");
		frm.refresh_field('rejected_items_reasons');
        frm.call({
			method:'set_data_in_rejected_items_reasons',
			doc:frm.doc,
		});
    }
});



frappe.ui.form.on('Downstream Processes', {
    setup: function(frm) {
        frm.set_query("rejection_reason", "rejected_items_reasons", function(doc, cdt, cdn) {
            let d = locals[cdt][cdn];
            return {
                filters: {
                    'rejection_type': d.rejection_type
                }
            };
        });
    }
});

frappe.ui.form.on('Downstream Processes', {
    setup: function(frm) {
        frm.set_query("target_warehouse", "rejected_items_reasons", function(doc, cdt, cdn) {
            let d = locals[cdt][cdn];
            return {
                filters: [['company', '=', frm.doc.company], ]
            };
        });
    }
});

frappe.ui.form.on('Downstream Processes', {
    setup: function(frm) {
        frm.set_query("target_warehouse", "items", function(doc, cdt, cdn) {
            let d = locals[cdt][cdn];
            return {
                filters: [['company', '=', frm.doc.company], ]
            };
        });
    }
});


frappe.ui.form.on('Downstream Processes', {
    setup: function(frm) {
        frm.set_query("source_warehouse", "raw_items", function(doc, cdt, cdn) {
            let d = locals[cdt][cdn];
            return {
                filters: [['company', '=', frm.doc.company], ]
            };
        });
    }
});

// ============================================================= Downstream Qty Details =================================================

frappe.ui.form.on('Downstream Qty Details', {
    ok_qty: function(frm) {

		frm.clear_table("rejected_items_reasons");
		frm.refresh_field('rejected_items_reasons');
            frm.call({
			method:'calculate_total_qty',
			doc:frm.doc,
		});
    }
});
frappe.ui.form.on('Downstream Qty Details', {
    cr_qty: function(frm) {
		frm.clear_table("rejected_items_reasons");
		frm.refresh_field('rejected_items_reasons');
        
        frm.call({
			method:'calculate_total_qty',
			doc:frm.doc,
		});
		
		
    }
});

frappe.ui.form.on('Downstream Qty Details', {
    mr_qty: function(frm) {
		frm.clear_table("rejected_items_reasons");
		frm.refresh_field('rejected_items_reasons');
		frm.call({
			method:'calculate_total_qty',
			doc:frm.doc,
		});

		
    }
});

frappe.ui.form.on('Downstream Qty Details', {
    rw_qty: function(frm) {
		frm.clear_table("rejected_items_reasons");
		frm.refresh_field('rejected_items_reasons');

            frm.call({
			method:'calculate_total_qty',
			doc:frm.doc,
		});

		
		
    }
});

// ============================================================= Downstream Items Production =================================================

frappe.ui.form.on('Downstream Items Production', {
    qty: function(frm) {
		frm.clear_table("raw_items"),
        frm.clear_table("qty_details"),
        frm.call({
			method:'method_to_set_raw_item',
			doc:frm.doc,
		})
    }
});

frappe.ui.form.on('Downstream Items Production', {
    item: function(frm) {
        frm.call({
			method:'set_warehouse_if_not',
			doc:frm.doc,
		})
    }
});



// frappe.ui.form.on('Downstream Items Production', {
//     setup: function(frm) {
// 		frm.clear_table("raw_items"),
//         frm.clear_table("qty_details"),
//         frm.call({
// 			method:'method_to_set_raw_item',
// 			doc:frm.doc,
// 		})
//     }
// });

// ============================================================= Downstream Raw Items Production =================================================

frappe.ui.form.on('Downstream Raw Items Production', {
    source_warehouse: function(frm) {
        frm.call({
			method:'set_available_qty',
			doc:frm.doc,
		})
    }
});