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
         
function validatePassword1()
{
  var b = document.getElementById("pass1").value;
  
  if(b.length == 0)
{
  producePrompt("Password is required","pass1Me","red");
  return false;
} 
producePrompt("","pass1Me","green");
return true;
}
         
function validatePassword2()
{
var b = document.getElementById("pass1").value;
var c = document.getElementById("pass2").value;

  if(c.length == 0)
{
  producePrompt("Confirm your password","pass2Me","red");
  return false;
}
if(b!==c)
{
producePrompt("Password donot match ","pass2Me","red");
  return false;
}
producePrompt("Password matched","pass2Me","green");
return true;
}
          
function producePrompt(message,promptlocation,color)
{
  document.getElementById(promptlocation).innerHTML=message;
  document.getElementById(promptlocation).style.color=color;
}
function validateForm()
{
  var p = validateName();
  var q = validatePassword1();
  var r = validatePassword2();
  return p && q && r;
}