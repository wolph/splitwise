Ext.define('Splitwise.store.Expenses', {
    id: 'expenses-store',
    extend: 'Ext.data.Store',
    model: 'Splitwise.model.Expense',
    autoLoad: true,
    pageSize: 100,
    groupField: 'group_id',
    getGroupString: function(record){
        var group_id = record.get('group_id');
        return group_id ? group_id : 0;
    },
});

