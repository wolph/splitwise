Ext.define('Splitwise.view.expense.Unify', {
    extend: 'Ext.window.Window',
    alias: 'widget.unify',

    title: 'Unify Currencies',
    layout: 'border',
    width: '80%',
    height: '80%',
    autoShow: true,

    items: [{
        xtype: 'grid',
        region: 'center',
        dockedItems: [{
            dock: 'top',
            xtype: 'toolbar',
            items: [{
                xtype: 'combo',
                width: 200,
                emptyText: 'Select a group...',
                store: 'Groups',
                editable: false,
                valueField: 'id',
                displayField: 'name',
                hideLabel: false,
                allowBlank: false,
                typeAhead: true,
                mode: 'local',
                triggerAction: 'all'
            }, {
                text: 'Convert',
                handler: function(){
                    var store = this.ownerCt.ownerCt.store;
                    var combo = this.ownerCt.items.items[0];
                    store.getProxy().setExtraParam('group_id',
                                                   combo.getValue());
                    store.sync();
                }
            }]
        }],
        viewConfig:{
            markDirty: false,
        },
        columns: [
            {
                xtype: 'checkcolumn',
                text: '#',
                dataIndex: 'convert',
                width: 25,
            },
            {text: '', dataIndex: 'unit', width: 45},
            {text: 'Cur', dataIndex: 'currency_code', width: 45},
            {
                text: 'New',
                dataIndex: 'new_currency_code',
                field: {
                    xtype: 'text'
                },
                width: 45,
            },
            {
                text: 'Exchange Rate',
                dataIndex: 'exchange',
                field: {
                    xtype: 'numberfield'
                },
                width: 120,
            },
        ],
        model: 'Currency',
        store: 'Currencies',
        plugins: [Ext.create('Ext.grid.plugin.CellEditing', {
            clicksToEdit: 1
        })],
    }],
    initComponent: function() {
        this.callParent(arguments);
    },
});

