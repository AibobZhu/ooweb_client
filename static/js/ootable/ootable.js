$(function(){

    var fetch_table_html = function(id, table_name, sort, dir, offset){

        sort = typeof sort !== 'undefined' ? sort : '';
        dir = typeof dir !== 'undefined' ? dir : 'asc';
        offset = typeof offset !== 'untab-panedefined' ? offset : '0';

        $.get(
            window.location+'api?table_name='+table_name+'&sort='+sort+'&dir='+dir+'&offset='+offset,
            function(data){
                $("#"+id).html(data);
                loadTab();
            }
        )

        .fail(function(d) {
            $("#ootable").html('<div class="alert alert-danger margin4020" role="alert">An error occurred. Check <a href="'+window.location+'api?table='+tab+'&sort='+sort+'&dir='+dir+'&offset='+offset+'" target="_blank">here</a> for more information</div>')
            console.log(d.responseText)
        })

    }
})