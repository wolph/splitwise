Ext.define('Splitwise.model.Picture', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'small', type: 'string'},
        {name: 'medium', type: 'string'},
        {name: 'large', type: 'string'},
    ],
    belongsTo: 'User',
});

