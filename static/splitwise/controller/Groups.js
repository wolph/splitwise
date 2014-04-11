Ext.define('Splitwise.controller.Groups', {
    extend: 'Ext.app.Controller',
    stores: [
        'Groups',
    ],
    views: [
        'group.List',
    ],
    models: [
        'Group',
    ],
    init: function() {
        this.control({
            'viewport > grouplist': {
                itemdblclick: this.editGroup
            },
            'groupedit button[action=save]': {
                click: this.updateGroup,
            }
        });
    },
    updateGroup: function(button) {
        var win    = button.up('window'),
            form   = win.down('form'),
            record = form.getRecord(),
            values = form.getValues();

        record.set(values);
        win.close();
    },
    editGroup: function(grid, record) {
        var view = Ext.widget('groupedit');
        view.down('form').loadRecord(record);
    },
});

