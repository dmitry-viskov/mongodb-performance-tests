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
    <div class="sblock2">or compare test results:</div>
    <div class="clear"></div>
    <div class="sblock2">
        %for i in range(1,3):
        <div>
            <select id="select_{{i}}" name="select_{{i}}" class="compare">\\
            %for adapter,test in available_tests.iteritems():
                %if not isinstance(test, basestring):
                    %for val in test:
                <option value="{{adapter}}|{{val['id']}}">{{adapter}}: {{val['name']}}</option>\\
                    %end
                %end
            %end
            </select>
        </div>
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