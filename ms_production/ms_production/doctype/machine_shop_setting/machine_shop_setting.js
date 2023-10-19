// Copyright (c) 2023, Abhishek Chougule and contributors
// For license information, please see license.txt

frappe.ui.form.on('Machine Shop Setting', {
	// refresh: function(frm) {

	// }
});


frappe.ui.form.on("Machine Shop Setting", {
	setup: function (frm) {
		frm.set_query("target_warehouse_p", function () { // Replace with the name of the link field
			return {
				filters: [
					["Warehouse", "company", '=', frm.doc.company],// Replace with your actual filter criteria
					["Warehouse", "is_group", '=', 0],
				]
			};
		});

	}
});

frappe.ui.form.on("Machine Shop Setting", {
	setup: function (frm) {
		frm.set_query("source_warehouse_p", function () { // Replace with the name of the link field
			return {
				filters: [
					["Warehouse", "company", '=', frm.doc.company],// Replace with your actual filter criteria
					["Warehouse", "is_group", '=', 0],

				]
			};
		});

	}
});

frappe.ui.form.on("Machine Shop Setting", {
	setup: function (frm) {
		frm.set_query("cr_warehouse_p", function () { // Replace with the name of the link field
			return {
				filters: [
					["Warehouse", "company", '=', frm.doc.company],// Replace with your actual filter criteria
					["Warehouse", "is_group", '=', 0],

				]
			};
		});

	}
});

frappe.ui.form.on("Machine Shop Setting", {
	setup: function (frm) {
		frm.set_query("mr_warehouse_p", function () { // Replace with the name of the link field
			return {
				filters: [
					["Warehouse", "company", '=', frm.doc.company],// Replace with your actual filter criteria
					["Warehouse", "is_group", '=', 0],

				]
			};
		});

	}
});

frappe.ui.form.on("Machine Shop Setting", {
	setup: function (frm) {
		frm.set_query("rw_warehouse_p", function () { // Replace with the name of the link field
			return {
				filters: [
					["Warehouse", "company", '=', frm.doc.company],// Replace with your actual filter criteria
					["Warehouse", "is_group", '=', 0],

				]
			};
		});

	}
});

frappe.ui.form.on("Machine Shop Setting", {
	setup: function (frm) {
		frm.set_query("target_warehouse_dp", function () { // Replace with the name of the link field
			return {
				filters: [
					["Warehouse", "company", '=', frm.doc.company],// Replace with your actual filter criteria
					["Warehouse", "is_group", '=', 0],

				]
			};
		});

	}
});

frappe.ui.form.on("Machine Shop Setting", {
	setup: function (frm) {
		frm.set_query("source_warehouse_dp", function () { // Replace with the name of the link field
			return {
				filters: [
					["Warehouse", "company", '=', frm.doc.company],// Replace with your actual filter criteria
					["Warehouse", "is_group", '=', 0],

				]
			};
		});

	}
});

frappe.ui.form.on("Machine Shop Setting", {
	setup: function (frm) {
		frm.set_query("cr_warehouse_dp", function () { // Replace with the name of the link field
			return {
				filters: [
					["Warehouse", "company", '=', frm.doc.company],// Replace with your actual filter criteria
					["Warehouse", "is_group", '=', 0],

				]
			};
		});

	}
});

frappe.ui.form.on("Machine Shop Setting", {
	setup: function (frm) {
		frm.set_query("mr_warehouse_dp", function () { // Replace with the name of the link field
			return {
				filters: [
					["Warehouse", "company", '=', frm.doc.company],// Replace with your actual filter criteria
					["Warehouse", "is_group", '=', 0],

				]
			};
		});

	}
});
frappe.ui.form.on("Machine Shop Setting", {
	setup: function (frm) {
		frm.set_query("rw_warehouse_dp", function () { // Replace with the name of the link field
			return {
				filters: [
					["Warehouse", "company", '=', frm.doc.company],// Replace with your actual filter criteria
					["Warehouse", "is_group", '=', 0],

				]
			};
		});

	}
});

