Ext.define('Splitwise.store.Currencies', {
    id: 'currencies-store',
    extend: 'Ext.data.Store',
    model: 'Splitwise.model.Currency',
    autoLoad: true,
});

