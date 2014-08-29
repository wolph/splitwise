Ext.define('Splitwise.model.Currency', {
    extend: 'Ext.data.Model',
    proxy: {
        type: 'rest',
        url: '/currencies/',
        batchActions: true,
        reader: {
            root: 'currencies',
        },
    },
    fields: [
        {name: 'currency_code', type: 'string'},
        {name: 'unit', type: 'string'},
        {name: 'exchange', type: 'number'},
        {name: 'new_currency_code', type: 'string'},
        {name: 'convert', type: 'boolean'},
    ]
});

