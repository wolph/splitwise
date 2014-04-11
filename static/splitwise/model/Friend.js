Ext.define('Splitwise.model.Friend', {
    extend: 'Splitwise.model.User',
    fields: [
        {name: 'updated_at', type: 'date', dateFormat: Ext.Date.Timestamp},
    ],
    proxy: {
        type: 'rest',
        url: '/friends/',
    },
    associations: [{
        name: 'balance',
        type: 'hasMany',
        model: 'Splitwise.model.Balance',
        autoLoad: true,
        foreignKey: 'currency_code',
        associationKey: 'balance',
    }],
});
