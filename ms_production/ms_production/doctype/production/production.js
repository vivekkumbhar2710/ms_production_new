// Copyright (c) 2023, Abhishek Chougule and contributors
// For license information, please see license.txt


frappe.ui.form.on('Production', {
	
	item:function(frm) {
		frm.clear_table("other_details")
		frm.refresh_field('other_details')
		frm.clear_table("qty_details")
		frm.refresh_field('qty_details')
		frm.call({
			method:'get_od',
			doc:frm.doc,
		})
	}
});


frappe.ui.form.on('Production', {
	
	ok_qty:function(frm) {
		frm.call({
			method:'totalqty_em',
			doc:frm.doc,
		})
	}
});

frappe.ui.form.on('Production', {
	cr_qty(frm) {
		frm.call({
			method:'totalqty_em',
			doc:frm.doc,
		})
	}
});

frappe.ui.form.on('Production', {
	mr_qty(frm ) {
		frm.call({
			method:'totalqty_em',
			doc:frm.doc,
		})
	}
});

frappe.ui.form.on('Production', {
	rw_qty(frm) {
		frm.call({
			method:'totalqty_em',
			doc:frm.doc,
		})
	}
});

frappe.ui.form.on('Production', {
	worked_time(frm) {
		frm.call({
			method:'time_diff',
			doc:frm.doc,
		})
	}
});

frappe.ui.form.on('Production', {
	before_save(frm) {
		frm.call({
			method:'time_diff',
			doc:frm.doc,
		})
	}
});
// new code


frappe.ui.form.on('Consumable Details', {
		qty(frm,cdt,cdn) {
				frm.call({
					method:'consumable_amount',
					doc:frm.doc,
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

