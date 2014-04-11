Ext.define('Splitwise.model.Balance', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'currency_code', type: 'string'},
        {name: 'amount', type: 'string'},
    ],
});
