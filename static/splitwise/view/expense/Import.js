Ext.define('Splitwise.view.expense.Import', {
    extend: 'Ext.window.Window',
    alias: 'widget.expenseimport',

    title: 'Import expenses',
    layout: 'fit',
    autoShow: true,

    initComponent: function() {
        this.items = [
            {
                xtype: 'form',
                items: [
                    {
                        xtype: 'filefield',
                        name : 'file',
                        emmptyText: 'Select an MT940 file (*.MTA)',
                        fieldLabel: 'Bank export file',
                        buttonText: '',
                        buttonConfig: {
                            iconCls: 'upload-icon',
                        },
                    },
                    {
                        xtype: 'button',
                        text: 'Upload',
                        fieldLabel: 'Submit',
                        handler: function(){
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


