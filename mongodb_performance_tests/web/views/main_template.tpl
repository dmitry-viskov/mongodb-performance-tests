<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>MongoDB performance tests</title>
<style type='text/css'>
#button_show_resulsts {
    display: none;
}
.sblock {
    margin: 5px;
}
.sblock2 {
    margin: 2px;
    float: left;
}
.sblock3 {
    margin: 2px;
}
.clear {
    clear:both;
}
.warning {
    color: red;
}
</style>
<script type="text/javascript" src="/static/jquery.min.js"></script>
<script type="text/javascript">
var available_tests = {{!adapters_tests_json}};
$(document).ready(function() {
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
});
</script>
</head>
<body>
<div class="sblock">
    <div class="sblock2">Please, choose adapter to show results:&nbsp;</div>
    <div class="clear"></div>
    <div class="sblock2">
        <select name="adapter" id="adapter" class="adapter">
            <option value="-">...</option>
            %for v in adapters:
            <option value="{{v}}">{{v}}</option>
            %end
        </select>
    </div>
    <div class="sblock2" id="tests"></div>
    <div class="sblock2" id="button_show_resulsts">
    <input type="button" name="show_graphics" id="show_graphics" value="Show graphics">
    </div>
    <div class="clear"></div>
</div>
<div class="sblock">
    <div class="sblock2">or compare DBs results:</div>
    <div class="clear"></div>
    <div class="sblock2">
    %for adapter,test in available_tests.iteritems():
        <label for="select_{{adapter}}">{{adapter}}</label>:
        %if isinstance(test, basestring):
            <span class="warning">{{test}}</span>
        %else:
            <select id="select_{{adapter}}" name="{{adapter}}" class="compare">
            %for val in test:
            <option value="{{val['id']}}">{{val['name']}}</option>
            %end
            </select>
        %end
        <br />
    %end
    </div>
    <div class="clear"></div>
    <div class="sblock3">
    %if may_compare:
    <input type="button" name="compare" id="compare" value="Compare">
    %end
    </div>
    <div class="clear"></div>
</div>
</body>
</html>