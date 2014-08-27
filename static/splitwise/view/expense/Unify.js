Ext.define('Splitwise.view.expense.Unify', {
    extend: 'Ext.window.Window',
    alias: 'widget.unify',

    title: 'Unify Currencies',
    layout: 'border',
    width: '90%',
    height: '90%',
    autoShow: true,

    initComponent: function() {
        this.items = [
            {
                xtype: 'grid',
                region: 'center',
                columns: [
                    {text: 'Convert', dataIndex: 'convert'},
                    {text: 'Transactions', dataIndex: 'transactions'},
                    {text: 'Currency', dataIndex: 'currency_code'},
                    {text: 'Unit', dataIndex: 'unit'},
                    {text: 'Amount', dataIndex: 'amount'},
                    {text: 'Exchange Rate', dataIndex: 'exchange'},
                    {text: 'Result', dataIndex: 'result'},
                ],
                model: 'Currency',
            },
        ];

        this.buttons = [
            {
                text: 'Convert',
                action: 'convert',
            },
            {
                text: 'Cancel',
                scope: this,
                handler: this.close,
            },
        ];

        this.callParent(arguments);
    }
});



