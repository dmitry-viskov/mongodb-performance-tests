<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>MongoDB performance tests</title>
<link rel="stylesheet" type="text/css" href="/static/jquery.jqplot.min.css" />
<script type="text/javascript" src="/static/jquery.min.js"></script>
<script type="text/javascript" src="/static/jquery.jqplot.min.js"></script>
<script type="text/javascript">
var json_data = {{json_data}};
$(document).ready(function() {
    $("#proc").change(function() {
        location.href = '/compare/' + $(this).val() + '/' + location.search;
    });

    $('#chartdiv').width($(window).width());
    $.jqplot('chartdiv', json_data, {
      series:[],
      seriesDefaults:{showMarker:true, showLine:false},
      title: 'Compare',
      axes:{
        xaxis:{
          label: 'request № (first, second, etc.)',
          labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
          min: 0
        },
        yaxis:{
          label: 'time (sec)',
          labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
          min: 0
        }
      },
      legend: {
        show: true,
        labels: {{!labels}}
      }
  });
});
</script>
</head>
<body>
<a href="/">< -Back</a><br />
Choose proc count for compare: <select id="proc" name="proc">
%for v in range(1,max_proc):
    %if v == current_proc_count:
    <option value="{{v}}" selected="selected">{{v}}</option>
    %else:
    <option value="{{v}}">{{v}}</option>
    %end
%end
</select>
<div id="chartdiv" style="height:768px;width:1024px;"></div>
</body>
</html>