Ext.define('Splitwise.view.expense.Edit', {
    extend: 'Ext.window.Window',
    alias: 'widget.expenseedit',

    title: 'Edit Expense',
    layout: 'fit',
    autoShow: true,
    width: 300,
    height: 700,

    initComponent: function() {
        this.items = [
            {
                xtype: 'propertygrid',
                sourceConfig: {
                    id: {
                        readOnly: true,
                        isEditableValue: false,
                        disableSelection: true,
                    },
                },
                listeners: {
                    'beforeedit': function (e) {
                    console.log('args', arguments);
                        switch (e.record.id) {
                            case 'readonly properties':
                                return false;

                            default:
                                return true;
                        }
                    },
                },
                //xtype: 'form',
                //items: [
                //    {
                //        xtype: 'textfield',
                //        name : 'description',
                //        fieldLabel: 'Description',
                //    },
                //    {
                //        xtype: 'textfield',
                //        name : 'cost',
                //        fieldLabel: 'Cost',
                //    },
                //    {
                //        xtype: 'textfield',
                //        name : 'created_at',
                //        fieldLabel: 'Created at',
                //    },
                //],
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

