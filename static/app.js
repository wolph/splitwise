Ext.Loader.setPath('Ext.ux', STATIC_URL + 'ext/ux');
Ext.require([
    'Ext.grid.*',
    'Ext.data.*',
    'Ext.ux.grid.FiltersFeature',
    'Ext.toolbar.Paging',
]);

Ext.Ajax.on('requestexception', function (conn, response, options) {
    if (response.status === 401) {
        Ext.Msg.alert('Please login',
                      'You are currently not logged in, you will be '
                      + 'redirected to the login page shortly');
        window.location = '/login';
    }
});

Ext.state.Manager.setProvider(new Ext.state.LocalStorageProvider());

Ext.define('Ext.grid.column.DateTemplate', {
    extend: 'Ext.grid.column.Template',
    alias: ['widget.datetemplatecolumn'],
    summaryType: function(records){
        var min, max;
        var column = this.dataIndex || this.summaryColumn;

        Ext.each(records, function(record){
            var date = record.get(column);
            if(!min || min > date)min = date;
            if(!max || max < date)max = date;
        });
        this._summary_min = min;
        this._summary_max = max;
    },
    summaryTpl: new Ext.XTemplate('{0:date("Y-m-d")}  - {1:date("Y-m-d")}'),
    summaryRenderer: function(){
        var min = this._summary_min, max = this._summary_max;
        if(min && max)
            return this.summaryTpl.apply([min, max]);
        else
            return '';
    },
    initComponent: function(){
        this.summaryType = this.summaryType.bind(this);
        this.callParent(arguments);
    },
});

Ext.define('Ext.grid.column.FilterDateTemplate', {
    extend: 'Ext.grid.column.DateTemplate',
    alias: ['widget.filterdatetemplatecolumn'],
    filter: {
        type: 'date',
        menuItems : ['before', 'after'],
        dateFormat : 'Y-m-d',
        onPickerSelect: function(picker, date) {
            var fields = this.fields,
                field = this.fields[picker.itemId];

            field.setChecked(true);
            this.values[picker.itemId] = date;
            this.fireEvent('update', this);
        },
    },
    initComponent: function(){
        this.callParent(arguments);
    },
});

Ext.application({
    requires: ['Ext.container.Viewport'],
    name: 'Splitwise',
    appFolder: STATIC_URL + 'splitwise',
    controllers: [
        'Users',
        'Groups',
        'Expenses',
    ],
    launch: function() {
        Ext.create('Ext.container.Viewport', {
            layout: 'fit',
            items: [
                //{
                //    region: 'north',
                //    title: 'Hello Ext',
                //    html : 'Hello! Welcome to Ext JS.'
                //},
                {
                    region: 'center',
                //    xtype: 'grouplist',
                    xtype: 'expenseslist',
                },
                //{
                //    region: 'south',
                //    xtype: 'expenseslist',
                //},
            ],
//            items: {
//                xtype: 'grouplist',
//                //xtype: 'expenseslist',
//            },
        });
    },
});

Ext.Date.patterns = {
    ISO8601Long: 'Y-m-d H:i:s',
    ISO8601Short: 'Y-m-d',
    ShortDate: 'n/j/Y',
    LongDate: 'l, F d, Y',
    FullDateTime: 'l, F d, Y g:i:s A',
    MonthDay: 'F d',
    ShortTime: 'g:i A',
    LongTime: 'g:i:s A',
    SortableDateTime: 'Y-m-d\\TH:i:s\\Z',
    UniversalSortableDateTime: 'Y-m-d H:i:sO',
    YearMonth: 'F, Y'
};

