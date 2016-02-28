<html>
<head>
<title>TickTock</title>
</head>
<body>
<style>
    * {
      font-family: verdana,sans-serif;
    }
</style>
<table border="0" width="600" align="center">
<tr>
<td>
<?php
  #ini_set('display_errors', 1);
  #ini_set('display_startup_errors', 1);
  #error_reporting(E_ALL);
  session_start();
  #print_r($_REQUEST);
 
  if($_REQUEST["action"] == "I am done!")
  {   
      $round = count($_SESSION["c"]);
      //print_r($_SESSION["c"]);
      echo "<script type=\"text/javascript\">
      function validateForm() {
         var x = document.forms[\"rateform\"][\"turkid\"].value;
         if (x == null || x == \"\") {
             alert(\"Please fill in your TurkID\");
             return false;
         }
       
         for(r = 0; r < " . $round . "; r++){
             var radios = document.getElementsByName(\"turn\" + r);
             var formValid = false;

             var i = 0;
             while (!formValid && i < radios.length) {
                if (radios[i].checked)
                    formValid = true;
                i++;        
             }

             if (!formValid){
                 alert(\"Please select your rating for turn \" + (r + 1));
                 return false;
             }
         }
      }
      </script>";
      echo "<form name=\"rateform\" method=\"POST\" action=\"a.php\" accept-charset=\"UTF-8\" onsubmit=\"return validateForm()\">\n";
      echo "Rate how appropriate you feel the system's response with respect to your input.  Try to make the decision for each round independently, try not to take context into consideration.<br><br>\n

\"Not appropriate\" means the system response is not coherent at all, e.g. Participant:  How old are you? TickTock:  Apple<br><br>\n

\"Interpretable\" means the system response is related and can be interpreted in a way. e.g. Participant: How old are you? TickTock: That's too big a question for me to answer. <br><br>\n

\"Appropriate\" means the system response, is very coherent with the user's previous utterance. e.g.Participant: How is the weather today? TickTock: Very good.<br><br><br>\n";
      echo "Your Turk ID: <input type=\"text\" name=\"turkid\"><br><br>\n";

      for($i = 0; $i < count($_SESSION["c"]); $i++)
      {
          echo "Turn: " . ($i + 1) . "<br>\n";
          echo "<i>You</i>: " . $_SESSION["c"][$i]["user"] . "<br>\n";
          echo "<i>TickTock</i>: " . $_SESSION["c"][$i]["ticktock"] . "<br>\n";
          echo "What do you think of the response?<br>\n";
          echo "<INPUT TYPE=\"radio\" NAME=\"turn" . $i . "\" VALUE=\"1\">Not Appropriate";
          
          echo "<INPUT TYPE=\"radio\" NAME=\"turn" . $i . "\" VALUE=\"2\">Interpretable";
          
          echo "<INPUT TYPE=\"radio\" NAME=\"turn" . $i . "\" VALUE=\"3\">Appropriate";
          echo "<br><br>\n";
      }

      echo "<input type=\"submit\" name=\"action\" value=\"Submit Ratings\"></p>
</form>";
  }
  else if ($_REQUEST["action"] == "Submit Ratings"){
      $fn = "/home/ubuntu/zhou/Backend/rating_log/rating" . date("Y-m-d-H-i-s", time()) . ".txt";
      $file = fopen($fn, "w");
      fwrite($file, "TurkID: " . $_REQUEST["turkid"] . "\n");
      fwrite($file, "UserID: " . $_SESSION["user"] . "\n");
      for($i = 0; $i < count($_SESSION["c"]); $i++)
      {
          fwrite($file, "Turn: " . ($i + 1) . "\n");
          fwrite($file, "You: " . $_SESSION["c"][$i]["user"] . "\n");
          fwrite($file, "TickTock: " . $_SESSION["c"][$i]["ticktock"] . "\n");
          fwrite($file, "Appropriateness: " . $_REQUEST["turn" . $i] . "\n\n");
      }
      fclose($file);
      echo "Thank you. <a = href=\"a.php\">One more time.</a>";
      unset($_SESSION["c"]);
  }
  else
  {

?>

<form method="POST" action="a.php" accept-charset="UTF-8">
<p>
<?php

   echo "<i>TickTock</i>: Please type in the box below and press 'Send Message' to talk to me. <br> <i>TickTock</i>: You can send multiple rounds of messages to me.<br> <i>TickTock</i>: Click 'I am done!' when you don't want to talk to me anymore<br> <i>TickTock</i>: Then you will rate how well I did.<br> <i>TickTock</i>: Now it is your turn to say something!  <br>\n";	  
  if(!array_key_exists("user", $_SESSION))
  {
     $_SESSION["user"] = rand();
  }

  if($_REQUEST["message"] == "")
  {
    unset($_SESSION["user"]);
}
  else
  {
    $s = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
    if ($s === false)
      echo "socket_create() fail\n";
    else
    {
      $result = socket_connect($s, "localhost", 13111);
      if ($result === false)
        echo "socket_connect() failed.\nReason: ($result) " . socket_strerror(socket_last_error($s)) . "\n"; 
    }
    $msg = $_SESSION["user"] . "|" . $_REQUEST["message"];
    socket_write($s, $msg, strlen($msg));
    $ans = socket_read($s, 2048);
    $turn = count($_SESSION["c"]);
    
    $_SESSION["c"][$turn]["user"] = $_REQUEST["message"];
    $_SESSION["c"][$turn]["ticktock"] = $ans; 
    for($i = 0; $i < count($_SESSION["c"]); $i++)
    {
        echo "<i>You</i>: " . $_SESSION["c"][$i]["user"] . "<br>\n";
        echo "<i>TickTock</i>: " . $_SESSION["c"][$i]["ticktock"] . "<br>\n";
    }
    socket_close($s);
  }

?>
<br>

<script type="text/javascript">
function entsub(event,ourform) {
  if (event && event.which == 13)
    ourform.submit();
  else
    return true;}

function done(){
  if(<?php echo count($_SESSION["c"]) ?> < 10)
  {
    alert("Please submit after the 10th round\n");
    return false;
  }
  return confirm('Are you sure?')
}

window.onload = function() {
  document.getElementById("msg1").focus();
};

</script>

<label>Press Enter to submit<br>
<i>You</i>: <input type="text" size="50" id="msg1" name="message" onkeypress="return entsub(event,this.form)" ></label></p>
<p><input type="submit" name="action" value="Send Message"></p>
<p><input type="submit" name="action" value="I am done!" onclick="return done()"></p>
</form>

<?php
  }
?>

</td>
</tr>
</table>
</body>
</html>
