jQuery(document).ready(function() {
            $('#comment_pannel').hide();
            var tid = $('#tid').val();
            var url = "/todo/"+tid+"/data";
         	$.get(url).done(function(data){
         			$('#task_name').append(data["task"]["name"]);
                  $('#user').append('<td>'+data["task"]["user"]+'</td>');
                  $('#text').append('<td>'+data["task"]["description"]+'</td>');
                  $('#timestamp').append('<td>'+data["task"]["timestamp"]+'</td>');
         			
                  if (data["task"]["status"] == 0){
         			   $('#status').append('<td><select name="status" class="inputDisabled"><option value="0" selected="selected">Pending</option><option value="1">Done</option></select></td>');
                  }
                  if (data["task"]["status"] == 1){
         			   $('#status').append('<td><select name="status" class="inputDisabled"><option value="0" >Pending</option><option value="1" selected="selected">Done</option></select></td>');
                  }
                  if (data["task"]["priority"] == 1){
         			   $('#priority').append('<td><select class="inputDisabled" name="priority"><option value="3">High</option><option value="2" >Medium</option><option value="1" selected="selected">Low</option></select></td>');
                  }
                  if (data["task"]["priority"] == 2){
         			   $('#priority').append('<td><select class="inputDisabled" name="priority"><option value="3">High</option><option value="2" selected="selected">Medium</option><option value="1" >Low</option></select></td>');
                  }
                  if (data["task"]["priority"] == 3){
         			   $('#priority').append('<td><select class="inputDisabled" name="priority"><option selected="selected" value="3">High</option><option value="2" >Medium</option><option value="3" >Low</option></select></td>');
                  }
                  $('.date').val(data["task"]["due_date"]);
                  for(var i = 0; i < data["assign_user"].length; i++) {	
                     $('#assign').append('<a class="btn btn-default" href="/todo/'+data["assign_user"][i]["id"]+'/delassign">'+data["assign_user"][i]['user']+' x</a>'); 
                  }
                  $('#assign').append(' <span style="padding:5px"></span> <a href="#" type="button" class="fa fa-plus-square btn btn-sm btn-default" data-toggle="modal" data-target="#myModal1"></a>');

                  if (data["comments"].length > 0)
                  {
                     $('#comment_pannel').show();
                  }

                  for(var i = 0; i < data["comments"].length; i++) {  
                     var desc = (data["comments"][i]["description"]).replace(/(?:\r\n|\r|\n)/g, '<br />');
                     $('#comments').append('<li class="list-group-item"><div class="row"><div class="col-xs-10 col-md-11"><div style="font-size:15px" class="mic-info">By:<a id="by" href="#">'+data["comments"][i]["user"]+'</a> at: <a id="timestamp" href="#">'+data["comments"][i]["timestamp"]+'</a></div><div id="comment" class="comment-text"><b>'+desc+'</b></div><a type="button" class="btn btn-primary btn-xs" href="/todo/comment/'+data["comments"][i]["id"]+'/edit" title="Delete"><span class="glyphicon glyphicon-pencil "></span></a> <a type="button" class="btn btn-danger btn-xs" href="/todo/comment/'+data["comments"][i]["id"]+'/delete" title="Delete"><span class="glyphicon glyphicon-trash"></span></a></div></div></div></li>');

                  }

            }); 	
} );