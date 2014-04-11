Ext.define('Splitwise.controller.Expenses', {
    extend: 'Ext.app.Controller',
    stores: [
        'Users',
        'Groups',
        'Friends',
        'Expenses',
    ],
    views: [
        'expense.List',
        'expense.Edit',
        'expense.Import',
    ],
    models: [
        'Picture',
        'Friend',
        'Balance',
        'Group',
        'User',
        'Expense',
    ],
    init: function() {
        this.control({
            'viewport > expenseslist': {
                itemdblclick: this.editExpense
            },
            'expenseedit button[action=save]': {
                click: this.updateExpense,
            }
        });
    },
    updateExpense: function(button) {
        var win    = button.up('window'),
            form   = win.down('form'),
            record = form.getRecord(),
            values = form.getValues();

        record.set(values);
        win.close();
    },
    editExpense: function(grid, record) {
        var view = Ext.widget('expenseedit');
        view.down('form').loadRecord(record);
    },
});

