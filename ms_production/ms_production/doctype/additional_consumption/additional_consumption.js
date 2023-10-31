// Copyright (c) 2023, Abhishek Chougule and contributors
// For license information, please see license.txt

frappe.ui.form.on('Additional Consumption', {
	// refresh: function(frm) {

	// }
});


// ============================================================= Additional Consumption =================================================


frappe.ui.form.on('Additional Consumption', {
	date: function (frm) {

		if (frm.doc.reference_doc) {
			frm.clear_table("items_table");
			frm.refresh_field('items_table');
			frm.clear_table("supervisor_wages_table");
			frm.refresh_field('supervisor_wages_table');
			frm.call({
				method: 'set_data_in_items_table',
				doc: frm.doc,
			})
		}
	}
});

frappe.ui.form.on('Additional Consumption', {
	reference_process: function (frm) {
		if (frm.doc.date) {
			frm.clear_table("items_table");
			frm.refresh_field('items_table');
			frm.clear_table("supervisor_wages_table");
			frm.refresh_field('supervisor_wages_table');
			frm.call({
				method: 'set_data_in_items_table',
				doc: frm.doc,
			})
		}
	}
});

frappe.ui.form.on('Additional Consumption', {
	reference_doc: function (frm) {
		if (frm.doc.date) {
			frm.clear_table("items_table");
			frm.refresh_field('items_table');
			frm.clear_table("supervisor_wages_table");
			frm.refresh_field('supervisor_wages_table');
			frm.call({
				method: 'set_data_in_items_table',
				doc: frm.doc,
			})
		}
	}
});


frappe.ui.form.on('Additional Consumption', {
	setup: function (frm) {
		frm.set_query("source_warehouse", "consumption_table", function (doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: [['company', '=', frm.doc.company],]
			};
		});
	}
});

frappe.ui.form.on('Additional Consumption', {
	setup: function (frm) {
		frm.set_query("cunsumption_item", "consumption_table", function (doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: [['company', '=', frm.doc.company],]
			};
		});
	}
});

frappe.ui.form.on("Additional Consumption", {
	setup: function (frm) {
		frm.set_query("expense_account_for_consumption", function () { // Replace with the name of the link field
			return {
				filters: [
					["Account", "company", '=', frm.doc.company] // Replace with your actual filter criteria
				]
			};
		});
	}
});

// frappe.ui.form.on('Additional Consumption', {
//     items_table_remove: function (frm, cdt, cdn) {
//         var d = locals[cdt][cdn];
//         frappe.msgprint("Row deleted successfully!");
//     }
// });

// this code is located inside `todo.js`

// frappe.ui.form.on('Additional Consumption', { // The child table is defined in a DoctType called "Dynamic Link"
//     items_table_remove: function(frm, cdt, cdn){ // "links" is the name of the table field in ToDo, "_add" is the event
//         // frm: current ToDo form
//         // cdt: child DocType 'Dynamic Link'
//         // cdn: child docname (something like 'a6dfk76')
//         // cdt and cdn are useful for identifying which row triggered this event

//         frappe.msgprint('A row has been added to the links table 🎉 ');
// 		frm.call({
// 			method: 'calculate_total_ok_qty',
// 			doc: frm.doc,
// 		})
//     }
// });

frappe.ui.form.on("Additional Consumption", {
	items_table_remove: function (frm) {
		frappe.msgprint('A row has been added to the links table 🎉 ');
		frm.call({
			method: 'calculate_total_ok_qty',
			doc: frm.doc,
		})
	}
});


// ============================================================= Additional Consumption Consumption =================================================

frappe.ui.form.on('Additional Consumption Consumption', {
	source_warehouse: function (frm) {
		frm.call({
			method: 'find_avalable_qty',
			doc: frm.doc,
		})

	}
});

// ============================================================= Additional Consumption Items =================================================

// frappe.ui.form.on('Additional Consumption Items', {
// 	table_remove: function (frm, cdt, cdn) {
// 		debugger
// 		var d = locals[cdt][cdn];
// 		frappe.msgprint("Row deleted successfully!");
// 	}
// })


