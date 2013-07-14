$(document).ready(function() {
    $('#example').dataTable( {
        "bProcessing": true,
        "bServerSide": true,
        "sAjaxSource": '/machinedb/json/datatable.json'
    } );
} );

