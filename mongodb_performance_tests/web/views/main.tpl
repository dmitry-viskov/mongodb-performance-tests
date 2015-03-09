% rebase('base.tpl')
<script type="text/javascript">
var available_tests = {{!adapters_tests_json}};
</script>
<div class="sblock">
    <div class="sblock2">Please, choose adapter to show results:&nbsp;</div>
    <div class="clear"></div>
    <div class="sblock2">
        <select name="adapter" id="adapter" class="adapter">
            <option value="-">...</option>\\
            %for v in adapters:
            <option value="{{v}}">{{v}}</option>\\
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
            <select id="select_{{adapter}}" name="{{adapter}}" class="compare">\\
            %for val in test:
            <option value="{{val['id']}}">{{val['name']}}</option>\\
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