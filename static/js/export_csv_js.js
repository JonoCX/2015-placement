/**
 * Created by Jonathan on 02/09/15.
 */

/**
 * Select all check box in table header,
 * allows all rows to be selected on clicking
 * @param source:   this
 */
function toggle(source)
{
    checkboxes = document.getElementsByName('select');
    for (var i = 0, n = checkboxes.length; i < n; i++)
    {
        checkboxes[i].checked = source.checked;
    }
}

$(document).ready(function ()
{
    $('#jq-datatables').DataTable();
    $('#jq-datatables_wrapper .table-caption').text('Export Audited Articles');
    $('#jq-datatables_wrapper .dataTables_filter input').attr('placeholder', 'Search...');

    // Turns the table into a searchable table
    $('#jq-datatables_filter').on('keyup', function()
    {
        $('#jq-datatables').search(this.value).draw();
    });

    // Highlights selected row
    $('#jq-datatables tbody').on('click', 'tr', function()
    {
        $(this).toggleClass('info');
    });


    $('#download').on('click', function()
    {
        var checkboxValues = [];

        // Fetch all the selected rows
        $('input[name="select"]:checked').map(function()
        {
            checkboxValues.push($(this).val());
        });

        // Post to the backend
        $.ajax(
            {
                type: "POST",
                url: "{% url 'export_to_csv' 0 %}",
                data:
                {
                    'id[]': checkboxValues,
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
                }
            }
        )
    });
});