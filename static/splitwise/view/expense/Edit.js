Ext.define('Splitwise.view.expense.Edit', {
    extend: 'Ext.window.Window',
    alias: 'widget.expenseedit',

    title: 'Edit User',
    layout: 'fit',
    autoShow: true,

    initComponent: function() {
        this.items = [
            {
                xtype: 'form',
                items: [
                    {
                        xtype: 'textfield',
                        name : 'description',
                        fieldLabel: 'Description',
                    },
                    {
                        xtype: 'textfield',
                        name : 'cost',
                        fieldLabel: 'Cost',
                    },
                    {
                        xtype: 'textfield',
                        name : 'created_at',
                        fieldLabel: 'Created at',
                    },
                ],
            },
        ];

        this.buttons = [
            {
                text: 'Save',
                action: 'save',
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

