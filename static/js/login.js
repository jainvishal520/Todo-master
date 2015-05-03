function validateName()
{
  var a = document.getElementById("name").value;
  
  if(a.length == 0)
{
  producePrompt("Username is required","nameMe","red");
  return false;
}
 if (!a.match(/^[A-Za-z0-9._-]/))
{
  producePrompt("Username invalid","nameMe","red");
  return false;
 }
producePrompt("Welcome "+a,"nameMe","green");
return true;
}
function validatePassword()
{
  var b = document.getElementById("pass").value;
  
  if(b.length == 0)
{
  producePrompt("Password is required","passMe","red");
  return false;
} 
producePrompt("","passMe","green");
return true;
}
         
function producePrompt(message,promptlocation,color)
{
  document.getElementById(promptlocation).innerHTML=message;
  document.getElementById(promptlocation).style.color=color;
} 