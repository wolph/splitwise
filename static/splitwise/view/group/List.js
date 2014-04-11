Ext.define('Splitwise.view.group.List', {
    extend: 'Ext.grid.Panel',
    alias: 'widget.grouplist',
    title: 'Groups',
    store: 'Groups',
    model: 'Group',
    columns: [
        {header: 'Id', dataIndex: 'id'},
        {header: 'Name', dataIndex: 'name'},
        {header: 'Members', dataIndex: 'members'},
        {header: 'Group type', dataIndex: 'group_type'},
        {header: 'Country code', dataIndex: 'country_code'},
        {header: 'Updated at', dataIndex: 'updated_at'},
        {header: 'Balance', dataIndex: 'balance'},
        {header: 'Suggested repayments', dataIndex: 'suggested_repayments'},
        {header: 'Original debts', dataIndex: 'original_debts'},
    ],

    initComponent: function() {
        this.callParent(arguments);
    },
});

//         {header: 'Users', dataIndex: 'users', renderer: function(value){
//             var names = [];
//             var i = value.length;
//             while(i--){
//                 names.push(renderUser(value[i].user));
//             }
//             if(names.length){
//                 return names.join(', ');
//             }else{
//                 return '';
//             }
//         }},
