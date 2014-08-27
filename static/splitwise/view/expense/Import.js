Ext.define('Splitwise.view.expense.Import', {
    extend: 'Ext.window.Window',
    alias: 'widget.expenseimport',

    title: 'Import Expenses',
    layout: 'border',
    width: '90%',
    height: '90%',
    autoShow: true,

    initComponent: function() {
        this.items = [
            {
                xtype: 'form',
                region: 'north',
                items: [
                    {
                        xtype: 'filefield',
                        name : 'file',
                        emmptyText: 'Select an MT940 file (*.MTA)',
                        buttonText: 'Upload file',
                        buttonOnly: true,
                        listeners: {
                            'change': function(fb, v){
                                var form = this.up('form').getForm();
                                if(form.isValid()){
                                    form.submit({
                                        url: '/upload/',
                                        waitMsg: 'Uploading your file',
                                        success: function(fp, o){
                                            msg('Success', tpl.apply(o.result));
                                        },
                                    });
                                }
                            },
                        },
                    },
                ],
            }, {
                xtype: 'grid',
                title: 'Expenses',
                region: 'center',
                columns: [
                    {text: 'Cost', dataIndex: 'cost'},
                    {text: 'Description', dataIndex: 'description'},
                ],
                model: 'Expense',
                height: 200,
                width: 200,
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


