% rebase('base.tpl')
<script type="text/javascript">
var graph_json_data = {{json_data}};
var graph_labels = {{!labels}};
var graph_title = '{{adapter_name}} results';
</script>
<a href="/">< -Back</a><br />
<div id="chartdiv" class="cartblock"></div>