Ext.define('Splitwise.view.expense.List', {
    extend: 'Ext.grid.Panel',
    alias: 'widget.expenseslist',
    title: 'Expenses',
    store: 'Expenses',
    model: 'Expense',
    stateful: true,
    stateId: 'expensesList',
    features: [{
        ftype: 'groupingsummary',
        groupHeaderTpl: [
            '{groupValue:this.name}',
            {
                name: function(id){
                    if(!id)return 'No group';
                    var group = this.owner.grid.stores.groups.getById(id);
                    return group ? group.get('name') : 'Group ' + id;
                },
            },
        ],
        enableGroupingMenu: false,
    }, {
        ftype: 'filters',
        local: false,
        encode: true,
        stateful: true,
        stateId: 'expensesListFilter',
        buildQuery : function (filters) {
            var p = {}, i, f, name, len = filters.length;
            for (i = 0; i < len; i++) {
                f = filters[i];
                p[f.data.comparison || f.field] = f.data.value;
            }
            return p;
        },
    }],
    columns: [
        {header: 'Id', dataIndex: 'id', hidden: true},
        {
            header: 'People',
            xtype: 'templatecolumn',
            sortable: false,
            tpl: [
                '<tpl for="users" between=", ">',
                    '<img style="width: 16px; height: 16px;" ',
                    'src="{user.picture.medium}">',
                '{user.first_name} {user.last_name}',
                '</tpl>',
            ],
            summaryType: function(records){
                var users = new Ext.util.HashMap();
                Ext.each(records, function(record){
                    Ext.each(record.get('users'), function(user){
                        users.replace(user.user_id, true);
                    });
                });
                return users.getCount();
            },
            summaryRenderer: function(value){
                return Ext.String.format('{0} people', value);
            },
            dataIndex: 'group_id',
            filter: {
                type: 'list',
                single: true,
                labelField: 'name',
                store: 'Groups',
                menuFilterText: 'Group',
            },
        },
        {
            header: 'Cost',
            xtype: 'templatecolumn',
            tpl: '{cost} {currency_code}',
            getSortParam: function(){
                return 'cost';
            },
            summaryTpl: new Ext.XTemplate(
                '<tpl foreach="." between=", ">',
                '{.} {$}',
                '</tpl>'
            ),
            summaryRenderer: function(value){
                return this.summaryTpl.apply(value);
            },
            summaryType: function(records){
                var sums = new Ext.util.HashMap();
                Ext.each(records, function(record){
                    var currency = record.get('currency_code');
                    var sum = sums.get(currency) || 0;
                    sums.replace(currency, sum + record.get('cost'));
                });
                return sums.map;
            },
        },
        {
            xtype: 'filterdatetemplatecolumn',
            header: 'Date',
            tpl: '{date:date("Y-m-d")}',
            dataIndex: 'date',
            filter: {
                compareMap: {
                    before: 'dated_before',
                    after: 'dated_after',
                },
            },
        },
        {header: 'Description', dataIndex: 'description'},
        {
            header: 'Created by',
            xtype: 'datetemplatecolumn',
            dataIndex: 'created_at',
            getSortParam: function(){return 'created_by'},
            tpl: '<tpl if="created_by">'
                + '<span title="{created_at}">'
                + '<img style="width: 16px; height: 16px;" src="{created_by.picture.medium}">'
                + '{created_by.first_name} {created_by.last_name}'
                + '</tpl>',
        },
        {
            header: 'Updated by',
            xtype: 'datetemplatecolumn',
            dataIndex: 'updated_at',
            getSortParam: function(){return 'updated_by'},
            tpl: '<tpl if="updated_by">'
                + '<span title="{updated_at}">'
                + '<img style="width: 16px; height: 16px;" src="{updated_by.picture.medium}">'
                + '{updated_by.first_name} {updated_by.last_name}'
                + '</tpl>',
        },
        {
            header: 'Deleted by',
            xtype: 'datetemplatecolumn',
            dataIndex: 'deleted_at',
            getSortParam: function(){return 'deleted_by'},
            tpl: '<tpl if="deleted_by">'
                + '<span title="{deleted_at}">'
                + '<img style="width: 16px; height: 16px;" src="{deleted_by.picture.medium}">'
                + '{deleted_by.first_name} {deleted_by.last_name}'
                + '</tpl>',
        },
        {header: 'Created at', dataIndex: 'created_at', hidden: true},
        {
            xtype: 'filterdatetemplatecolumn',
            header: 'Updated at',
            dataIndex: 'updated_at',
            tpl: '{updated_at:date("Y-m-d")}',
            filter: {
                compareMap: {
                    before: 'updated_before',
                    after: 'updated_after',
                },
            },
            hidden: true,
        },
        {header: 'Deleted_at', dataIndex: 'deleted_at', hidden: true},
        {header: 'Category', xtype: 'templatecolumn', tpl: '{category.name}', hidden: true},
        {header: 'Creation method', dataIndex: 'creation_method', hidden: true},
        {header: 'Details', dataIndex: 'details', hidden: true},
        {header: 'Email reminder', dataIndex: 'email_reminder', hidden: true},
        {header: 'Email reminder in advance', dataIndex: 'email_reminder_in_advance', hidden: true},
        {header: 'Expense bundle id', dataIndex: 'expense_bundle_id', hidden: true},
        {header: 'Friendship id', dataIndex: 'friendship_id', hidden: true},
        {header: 'Next repeat', dataIndex: 'next_repeat', hidden: true},
        {header: 'Payment', dataIndex: 'payment', hidden: true},
        {header: 'Receipt', dataIndex: 'receipt', hidden: true},
        {header: 'Repayments', dataIndex: 'repayments', hidden: true},
        {header: 'Repeat interval', dataIndex: 'repeat_interval', hidden: true},
        {header: 'Repeats', dataIndex: 'repeats', hidden: true},
        {header: 'Transaction confirmed', dataIndex: 'transaction_confirmed', hidden: true},
        {header: 'Transaction method', dataIndex: 'transaction_method', hidden: true},
        {header: 'Comments', dataIndex: 'comments_count', hidden: true},
    ],
    dockedItems: [{
        xtype: 'pagingtoolbar',
        store: 'Expenses',
        dock: 'bottom',
        displayInfo: true,
        afterPageText: '',
        displayMsg: 'Displaying {0} - {1}',
        items: [{
            xtype: 'button',
            text: 'Import expenses',
            handler: function(){
                Ext.widget('expenseimport');
            },
        }],
    }],
    initComponent: function() {
        var self = this;
        this.stores = {
           groups: Ext.StoreManager.lookup('Groups'),
        };
        Ext.each(this.columns, function(column){
            if(column.filter && column.filter.store){
                var store = column.filter.store;
                if(!self.stores[store])self.stores[store] = Ext.StoreManager.lookup(store);
                column.filter.store = self.stores[store];
            }
        });
        this.callParent(arguments);
    }
});

