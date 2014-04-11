Ext.define('Splitwise.model.User', {
    extend: 'Ext.data.Model',
    proxy: {
        type: 'rest',
        url: '/users/',
    },
    fields: [
        {name: 'id', type: 'int'},
        {name: 'first_name', type: 'string'},
        {name: 'last_name', type: 'string'},
        {name: 'email', type: 'string'},
        {name: 'picture'},
        {name: 'registration_status', type: 'string'},
        {name: 'locale', type: 'string'},
        {name: 'date_format', type: 'string'},
        {name: 'default_currency', type: 'string'},
        {name: 'default_group_id', type: 'int'},
        {name: 'notifications'},
    ],
    associations: [{
        type: 'hasOne',
        model: 'Splitwise.model.Picture',
        name: 'picture',
        associationKey: 'picture',
    }, {
        type: 'belongsTo',
        model: 'Splitwise.model.Group',
        name: 'default_group',
        foreignKey: 'default_group_id',
    }],
});

/* notifications
{name: 'added_as_friend', type: 'string'},
{name: 'added_to_group', type: 'string'},
{name: 'expense_added', type: 'string'},
{name: 'expense_updated', type: 'string'},
{name: 'bills', type: 'string'},
{name: 'payments', type: 'string'},
{name: 'monthly_summary', type: 'string'},
{name: 'announcements', type: 'string'},
*/
