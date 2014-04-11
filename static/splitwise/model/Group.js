Ext.define('Splitwise.model.Group', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', type: 'int'},
        {name: 'name', type: 'string'},
        {name: 'group_type', type: 'string'},
        {name: 'country_code', type: 'string'},
        {name: 'updated_at', type: 'date', dateFormat: Ext.Date.Timestamp},
        {name: 'balance'},
        {name: 'suggested_repayments'},
        {name: 'original_debts'},
    ],
    associations: [{
        type: 'hasMany',
        model: 'User',
        foreignKey: 'members.user_id',
        associationKey: 'members',
        name: 'members',
        autoLoad: true,
    }],
    proxy: {
        type: 'rest',
        url: '/groups/',
    },
});

