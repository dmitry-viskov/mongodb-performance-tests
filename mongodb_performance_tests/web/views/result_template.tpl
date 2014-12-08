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
    $('#chartdiv').width($(window).width());
    $.jqplot('chartdiv', json_data, {
      series:[{showMarker:false}],
      title: '{{adapter_name}}',
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
<div id="chartdiv" style="height:768px;width:1024px;"></div>
</body>
</html>