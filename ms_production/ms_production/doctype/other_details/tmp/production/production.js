// Copyright (c) 2023, Abhishek Chougule and contributors
// For license information, please see license.txt


// frappe.ui.form.on('Production', {
	
// 	item:function(frm) {
// 		frm.clear_table("other_details")
// 		frm.refresh_field('other_details')
// 		frm.clear_table("qty_details")
// 		frm.refresh_field('qty_details')
// 		frm.call({
// 			method:'get_od',
// 			doc:frm.doc,
// 		})
// 	}
// });



// frappe.ui.form.on('Production', {
	
// 	ok_qty:function(frm) {
// 		frm.call({
// 			method:'totalqty_em',
// 			doc:frm.doc,
// 		})
// 	}
// });

// frappe.ui.form.on('Production', {
// 	cr_qty(frm) {
// 		frm.call({
// 			method:'totalqty_em',
// 			doc:frm.doc,
// 		})
// 	}
// });

// frappe.ui.form.on('Production', {
// 	mr_qty(frm ) {
// 		frm.call({
// 			method:'totalqty_em',
// 			doc:frm.doc,
// 		})
// 	}
// });

// frappe.ui.form.on('Production', {
// 	rw_qty(frm) {
// 		frm.call({
// 			method:'totalqty_em',
// 			doc:frm.doc,
// 		})
// 	}
// });

// frappe.ui.form.on('Production', {
// 	worked_time(frm) {
// 		frm.call({
// 			method:'time_diff',
// 			doc:frm.doc,
// 		})
// 	}
// });

// // frappe.ui.form.on('Production', {
// // 	before_save(frm) {
// // 		frm.call({
// // 			method:'time_diff',
// // 			doc:frm.doc,
// // 		})
// // 	}
// // });


frappe.ui.form.on('Consumable Details', {
		qty(frm,cdt,cdn) {
				frm.call({
					method:'consumable_amount',
					doc:frm.doc,
				})
			}
});

frappe.ui.form.on('Items Production', {
	item(frm,cdt,cdn) {
		var row = locals[cdt][cdn];
		var rowIndex = row.idx;
		var rawItems = frm.doc.raw_items;
		var itemOperations = frm.doc.item_operations;
 
		frm.clear_table("raw_items")
		frm.clear_table("item_operations")
		frm.clear_table("qty_detials")
 
		frm.call({
			method:'update_raw_data',
			doc:frm.doc,
			args: {
            index: rowIndex,
			raw_items: rawItems,
			item_operations: itemOperations,
	    	},
		})
	}
});



frappe.ui.form.on('Production', {
	operation:function(frm) {
		frm.call({
			method:'fetch_oprations',
			doc:frm.doc,
		})
	}
});


frappe.ui.form.on('Item operations', {
	cycle_time(frm,cdt,cdn) {
		var row = locals[cdt][cdn];
		var rowIndex = row.idx;
		var qtyItems = frm.doc.qty_details;
		frm.clear_table("qty_details")

		frm.call({
			method:'cycle_time_changed',
			doc:frm.doc,
			args: {
				index: rowIndex,
				qty_items: qtyItems,
			},
		})
	},
	ok_qty(frm,cdt,cdn) {
		var row = locals[cdt][cdn];
		var rowIndex = row.idx;
		var qtyItems = frm.doc.qty_details;
		frm.clear_table("qty_details")

		frm.call({
			method:'cycle_time_changed',
			doc:frm.doc,
			args: {
				index: rowIndex,
				qty_items: qtyItems,
			},
		})
	},
	cr_qty(frm,cdt,cdn) {
		var row = locals[cdt][cdn];
		var rowIndex = row.idx;
		var qtyItems = frm.doc.qty_details;
		frm.clear_table("qty_details")

		frm.call({
			method:'cycle_time_changed',
			doc:frm.doc,
			args: {
				index: rowIndex,
				qty_items: qtyItems,
			},
		})
	},
	mr_qty(frm,cdt,cdn) {
		var row = locals[cdt][cdn];
		var rowIndex = row.idx;
		var qtyItems = frm.doc.qty_details;
		frm.clear_table("qty_details")

		frm.call({
			method:'cycle_time_changed',
			doc:frm.doc,
			args: {
				index: rowIndex,
				qty_items: qtyItems,
			},
		})
	},
	rw_qty(frm,cdt,cdn) {
		var row = locals[cdt][cdn];
		var rowIndex = row.idx;
		var qtyItems = frm.doc.qty_details;
		frm.clear_table("qty_details")

		frm.call({
			method:'cycle_time_changed',
			doc:frm.doc,
			args: {
				index: rowIndex,
				qty_items: qtyItems,
			},
		})
	},
	
});

frappe.ui.form.on('Qty Details', {
	ok_qty(frm,cdt,cdn) {
		var row = locals[cdt][cdn];
		var rowIndex = row.idx;
		frm.call({
			method:'calculate_qty',
			doc:frm.doc,
			// args: {
			// 	index: rowIndex,
			// },
		})
	}
});

frappe.ui.form.on('Qty Details', {
	cr_qty(frm,cdt,cdn) {
		var row = locals[cdt][cdn];
		frm.clear_table("rejected_items_reasons")
		frm.call({
			method:'calculate_rejection_qty',
			doc:frm.doc,
		})
	}
});
frappe.ui.form.on('Qty Details', {
	mr_qty(frm,cdt,cdn) {
		var row = locals[cdt][cdn];
		var rowIndex = row.idx;
		frm.clear_table("rejected_items_reasons") 
		frm.call({
			method:'calculate_rejection_qty',
			doc:frm.doc,
			// args: {
			// 	index: rowIndex,
			// },
		})
	}
});
frappe.ui.form.on('Qty Details', {
	rw_qty(frm,cdt,cdn) {
		var row = locals[cdt][cdn];
		var rowIndex = row.idx;
		frm.call({
			method:'calculate_qty',
			doc:frm.doc,
			// args: {
			// 	index: rowIndex,
			// },
		})
	}
});


// frappe.ui.form.on('Raw Items Production', {
// 	item(frm,cdt,cdn) {
// 		frm.call({
// 			method:'calculate_boring',
// 			doc:frm.doc,
// 		})
// 	}
// });


frappe.ui.form.on('Raw Items Production', {
	raw_item(frm,cdt,cdn) {
		frm.call({
			method:'calculate_boring',
			doc:frm.doc,
		})
	}
});

frappe.ui.form.on('Raw Items Production', {
	
	raw_item(frm,cdt,cdn) {
		frm.call({
			method:'calculate_boring',
			doc:frm.doc,
		})
		frm.events.calculate_basic_amount(frm, stockEntryDetailData);
		console.log(stockEntryDetailData.basic_rate)
	}

	
});


frappe.ui.form.on('Raw Items Production', {
	source_warehouse(frm,cdt,cdn) {
		frm.call({
			method:'get_available_qty',
			doc:frm.doc,
		})
	}
});


frappe.ui.form.on('Tooling Details', {
	source_warehouse(frm,cdt,cdn) {
		frm.call({
			method:'get_available_qty_of_tooling',
			doc:frm.doc,
		})
	}
});

 

frappe.ui.form.on('Consumable Details', {
	source_warehouse(frm,cdt,cdn) {
		frm.call({
			method:'get_available_qty_of_consumables',
			doc:frm.doc,
		})
	}
});

frappe.ui.form.on('Tooling Details', {
	tooling_item(frm,cdt,cdn) {
		frm.call({
			method:'get_rate_of_tooling',
			doc:frm.doc,
		})
	}
});












// frappe.ui.form.on('Item operations', {
// 	operation(frm,cdt,cdn) {
// 		var row = locals[cdt][cdn];
// 		var rowIndex = row.idx;
// 		var qtyItems = frm.doc.qty_details;
// 		frm.clear_table("qty_detials")
// 			frm.call({
// 				method:'cycle_time_changed',
// 				doc:frm.doc,
// 				args: {
// 					index: rowIndex,
// 					qty_items: qtyItems,
// 				},
// 			})
// 	}
// });

// frappe.ui.form.on('Item operations', {
// 	machine(frm,cdt,cdn) {
// 		var row = locals[cdt][cdn];
// 		var rowIndex = row.idx;
// 		var qtyItems = frm.doc.qty_details;
// 		frm.clear_table("qty_details")
// 			frm.call({
// 				method:'cycle_time_changed',
// 				doc:frm.doc,
// 				args: {
// 					index: rowIndex,
// 					qty_items: qtyItems,
// 				},
// 			})
// 	}
// });





