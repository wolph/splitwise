Ext.define('Splitwise.model.Currency', {
    extend: 'Ext.data.Model',
    proxy: {
        type: 'rest',
        url: '/currencies/',
    },
    fields: [
        {name: 'currency_code', type: 'string'},
        {name: 'unit', type: 'string'},
        {name: 'transactions', type: 'int'},
        {name: 'amount', type: 'number'},
        {name: 'exchange', type: 'number'},
        {name: 'result', convert: function(value, record){
            return record.get('exchange') * record.get('amount');
        }}
    ]
});

