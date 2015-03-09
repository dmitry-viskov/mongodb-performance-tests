% rebase('base.tpl')
<script type="text/javascript">
var graph_json_data = {{json_data}};
var graph_labels = {{!labels}};
var graph_title = '{{graph_title}}';
</script>
<a href="/">< -Back</a><br />
Choose proc count for compare: <select id="proc" name="proc">
%for v in range(1,max_proc):
    <% selected = ' selected="selected"' if v == current_proc_count else '' %>
    <option value="{{v}}"{{selected}}>{{v}}</option>\\
%end
</select>
<div id="chartdiv" class="cartblock"></div>