// Copyright (c) 2023, Abhishek Chougule and contributors
// For license information, please see license.txt



frappe.ui.form.on('Production', {
    job_order: function(frm) {
			debugger
            frappe.call({
                method: 'set_filters_for_items',
                doc: frm.doc,
                callback: function(r) {
                    if (r.message) {
                        var k = r.message;
                        frm.set_query("item", "items", function(doc, cdt, cdn) {
                            let d = locals[cdt][cdn];
                            return {
                                filters: [
                                    ['Item', 'item_group', '=', 'Products'],
                                    ['Item', 'name', 'in', k],
                                ]
                            };
                        });
                    }
                }
			});
        
    }
});



frappe.ui.form.on('Production', {
	refresh: function(frm) {
		frm.set_query("raw_item", "raw_items", function(doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {

				filters: [
				  ['Item', 'item_group', '=', "Raw Material"],
				]
			};
		});
	},
});

frappe.ui.form.on('Production', {
	refresh: function(frm) {
		frm.set_query("tooling_item", "tooling_details", function(doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {

				filters: [
				  ['Item', 'item_group', '=', "Tooling"],
				]
			};
		});
	},
});


frappe.ui.form.on("Production", {
    refresh: function(frm) {
            frm.set_query("job_order", function() { // Replace with the name of the link field
                return {
                    filters: [
                        ["Job Order", "company", '=', frm.doc.company],// Replace with your actual filter criteria

					]
                };
            });

        }
    });

frappe.ui.form.on('Production', {
    refresh: function(frm) {
        $('.layout-side-section').hide();
        // $('.layout-main-section-wrapper').css('margin-left', '0');
    }
});

frappe.ui.form.on('Raw Items Production', {
	required_time: function(frm,cdt, cdn) {
		frappe.call({
			method: 'validate_required_time_per_row_material',
			doc: frm.doc,
		});
		frm.refresh_field('raw_items');

		// frm.refresh_field('cycle_time');
		// frm.refresh_field('taxes');
	}
}); 

frappe.ui.form.on('Item operations', {
	operation: function(frm,cdt, cdn) {
		frappe.call({
			method: 'set_cycle_time',
			doc: frm.doc,
		});
		frm.refresh_field('cycle_time');
		// frm.refresh_field('taxes');
	}
}); 

frappe.ui.form.on('Items Production', {
	item: function(frm) {
 
			frappe.call({
				method: 'set_filters_IOM',
				doc: frm.doc,
				callback: function(r) {
					if(r.message) {
						var k = r.message[0];
						var m = r.message[1]; 
						frm.set_query("operation", "item_operations", function(doc, cdt, cdn) {
							let d = locals[cdt][cdn];
							return {
								filters: [['name', 'in',m],]
							};
						});
						      
					
					}
				}
			});
			
		}
	});

	frappe.ui.form.on('Production', {
		refresh: function(frm) {
	 
				frappe.call({
					method: 'set_filters_IOM',
					doc: frm.doc,
					callback: function(r) {
						if(r.message) {
							var k = r.message[0];
							var m = r.message[1]; 
							frm.set_query("operation", "item_operations", function(doc, cdt, cdn) {
								let d = locals[cdt][cdn];
								return {
									filters: [['name', 'in',m],]
								};
							});
								  
						
						}
					}
				});
				
			}
		});
	





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
	operation(frm,cdt,cdn) {
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
	rw_qty(frm,cdt,cdn) {
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
		})
	}
});




frappe.ui.form.on('Raw Items Production', {
	required_time(frm,cdt,cdn) {
		frm.call({
			method:'calculate_boring',
			doc:frm.doc,
		})
	}
});

frappe.ui.form.on('Raw Items Production', {
	source_warehouse(frm,cdt,cdn) {
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

frappe.ui.form.on('Qty Details', {
	ok_qty(frm,cdt,cdn) {
		frm.call({
			method:'validate_qty_on_earned_min',
			doc:frm.doc,
		})
	},
	
	
});


frappe.ui.form.on('Qty Details', {
	cr_qty(frm,cdt,cdn) {
		frm.call({
			method:'validate_qty_on_earned_min',
			doc:frm.doc,
		})
	},
	
	
});

frappe.ui.form.on('Qty Details', {
	mr_qty(frm,cdt,cdn) {
		frm.call({
			method:'validate_qty_on_earned_min',
			doc:frm.doc,
		})
	},
	
	
});

frappe.ui.form.on('Qty Details', {
	rw_qty(frm,cdt,cdn) {
		frm.call({
			method:'validate_qty_on_earned_min',
			doc:frm.doc,
		})
	},
	
	
});

frappe.ui.form.on('Qty Details', {
	ok_qty(frm,cdt,cdn) {
		frm.call({
			method:'calculate_total_weges',
			doc:frm.doc,
		})
	},
	
	
});


frappe.ui.form.on('Qty Details', {
	cr_qty(frm,cdt,cdn) {
		frm.call({
			method:'calculate_total_weges',
			doc:frm.doc,
		})
	},
	
	
});

frappe.ui.form.on('Qty Details', {
	mr_qty(frm,cdt,cdn) {
		frm.call({
			method:'calculate_total_weges',
			doc:frm.doc,
		})
	},
	
	
});

frappe.ui.form.on('Qty Details', {
	rw_qty(frm,cdt,cdn) {
		frm.call({
			method:'calculate_total_weges',
			doc:frm.doc,
		})
	},
	
	
});


frappe.ui.form.on('Production', {
	refresh: function(frm) {
		frm.set_query("target_warehouse", "items", function(doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: [['company', '=', frm.doc.company], ]
			};
		});
		// frm.set_query("item", "items", function(doc, cdt, cdn) {
		// 	let d = locals[cdt][cdn];
		// 	return {
		// 		filters: [['name', 'in', ["1010100007","1010100018"]], ]
		// 	};
		// });


	},
});




frappe.ui.form.on('Production', {
	refresh: function(frm) {
		frm.set_query("source_warehouse", "raw_items", function(doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: [['company', '=', frm.doc.company], ]
			};
		});


	},
});

// frappe.ui.form.on('Items Production', {
// 	item: function(frm) {
// 		frm.set_query("item", "item_operations", function(doc, cdt, cdn) {
// 			let d = locals[cdt][cdn];
// 			var list_of_filtered_item = [];
// 			frm.doc.items.forEach(function(row) {
// 				list_of_filtered_item.push(row.item);
// 			});
// 			return {
// 				filters: [['name', 'in', list_of_filtered_item], ]
// 			};
// 		});


// 	},
// });


frappe.ui.form.on('Production', {
    job_order: function(frm) {
		// frm.clear_table("items")
		// frm.refresh_field('items')
        frappe.call({
			method: 'after_select_job_order',
			doc: frm.doc,
		});
		frm.refresh_field('items')
		frm.refresh_field('raw_items')
    }
});

