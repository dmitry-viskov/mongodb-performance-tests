<!doctype html>
<html>
<head>
<meta charset="utf-8">
<script type="text/javascript" src="/static/jquery.min.js"></script>
<script type="text/javascript">
$(document).ready(function() {
    $("#show_graphics").click(function() {
        location.href = '/result/' + $("select.adapter option:selected").val();
    });
});
</script>
</head>
<body>
<h1>Please, choose adapter to show results:</h1>
<select name="adapter" class="adapter">
<option value="mongodb">MongoDB</option>
<option value="mysql">MySQL</option>
</select>
<input type="button" name="show_graphics" id="show_graphics" value="Show graphics">
</body>
</html>