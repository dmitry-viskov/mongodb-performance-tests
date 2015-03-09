$(document).ready(function() {

    /* ------- main_template ------- */

    $("#adapter").change(function() {
        var adp = $("#adapter").val();
        var adp_tmp = available_tests[adp];

        if (adp == '-') {
            $('#tests').html('');
            $('#button_show_resulsts').hide();
        } else {
            if (typeof adp_tmp == 'string' || adp_tmp instanceof String) {
                $('#tests').html(adp_tmp);
                $('#button_show_resulsts').hide();
            } else {
                var s = $("<select id=\"available_tests\" name=\"available_tests\" />");
                for (var i in adp_tmp) {
                    $("<option />", {value: adp_tmp[i].id, text: adp_tmp[i].name}).appendTo(s);
                }
                $('#tests').html(s);
                $('#button_show_resulsts').show();
            }
        }
    });

    $("#show_graphics").click(function() {
        location.href = '/result/' + $("#adapter").val() + '/' + $("#available_tests").val();
    });

    $("#compare").click(function() {
        var url = '/compare/0/?';
        var url_params = [];
        $('select.compare').each(function() {
            url_params.push($(this).attr('name') + '=' + $(this).val());
        });
        location.href = url + url_params.join('&');
    });

    /* ------- compare_template ------- */

    $("#proc").change(function () {
        location.href = '/compare/' + $(this).val() + '/' + location.search;
    });

    /* ------- graphics ------- */

    if($('#chartdiv').length > 0) {
        $('#chartdiv').width($(window).width());
        $.jqplot('chartdiv', graph_json_data, {
            series: [],
            seriesDefaults: {showMarker: true, showLine: false},
            title: graph_title,
            axes: {
                xaxis: {
                    label: 'request № (first, second, etc.)',
                    labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                    min: 0
                },
                yaxis: {
                    label: 'time (sec)',
                    labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                    min: 0
                }
            },
            legend: {
                show: true,
                labels: graph_labels
            }
        });
    }
});