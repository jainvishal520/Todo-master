jQuery(document).ready(function() {
             $.get('/todo/tasks').done(function(data){
                 for(var i = 0; i < data.length; i++) 
{
                 var tr = '<tr class="gradeX"><td><span class="fa fa-edit"><a class="task" href=/todo/'+data[i]["id"]+'>'+data[i]["name"]+'</a></td><td>'+data[i]["user"]+'</td><td class=""><div class="date-container pull-left">'+data[i]["timestamp"]+'</div></td><td class=""><div class="date-container pull-left">'+data[i]["due_date"]+'</div></td></div></td><td><input type="checkbox" name="tasks_id" value="'+data[i]["id"]+'"></td></tr>';
                 $('#task-body').append(tr);
                  }
                  $('#task').dataTable();
                  });
                  });
function validateName()
{
           var a = document.getElementById("name").value;
           
           if(a.length == 0)
{
           producePrompt("Task name is required","nameMe","red");
           return false;
}         
producePrompt("Task name is "+a,"nameMe","green");
return true;
}
function producePrompt(message,promptlocation,color)
           {
           document.getElementById(promptlocation).innerHTML=message;
           document.getElementById(promptlocation).style.color=color;
           }
