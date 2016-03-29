<form method="POST" action="d.php" accept-charset="UTF-8">
<link rel="stylesheet" href="/css/bootstrap.min.css">
<link rel="stylehseet" href="css/custom.css">
<div class="container">
<div class="starter-template">
<h1>Conversations with TickTock</h1>
<p class="starter-template">
<?php
  function open_socket()
  {
    $s = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
    if ($s === false)
    {
      echo "socket_create() fail\n";
      return false;
    }
    else
    {
      $result = socket_connect($s, "localhost", 11332);
      if ($result === false)
        echo "socket_connect() failed.\nReason: ($result) " . socket_strerror(socket_last_error($s)) . "\n";
      return $result;
    }
  }
  session_start();
  if(array_key_exists("turkid", $_REQUEST))
  {
     $_SESSION["user"] = $_REQUEST["turkid"];
     $_SESSION["count"] = 0;
     /*$s = open_socket();
     $msg = $_SESSION["user"] . "1|get_the_intro";
     socket_write($s, $msg, strlen($msg));
     $ans = socket_read($s, 1024);
     echo $ans;
     socket_close($s);*/
  }


    if(!array_key_exists("user", $_SESSION))
    {
       echo "Pretend that you are TickTock, a chatbot, what would you respond to the participant that is talking to you. Fill in the blank of what you think TickTock should reply to the user given the conversation history displayed.<br>\nPlease input your TurkID first and press 'send message' to start the task.<br>";
       $msg_type = "turkid";


?>
TurkID:<input type="text" name="turkid" cols="48" rows="8"></label></p>
<?php


    }
    else
    {
    //if($_REQUEST["message"] == "")
    //{
    //  echo "Please input a response and press submit<br>\n";
    //}
    //else
    //{
      $msg_type = "message";
      $s = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
      if ($s === false)
        echo "socket_create() fail\n";
      else
      {
        $result = socket_connect($s, "localhost", 11332);
        if ($result === false)
          echo "socket_connect() failed.\nReason: ($result) " . socket_strerror(socket_last_error($s)) . "\n";
      }
      if ($_REQUEST["message"] != ""){
        $msg = $_SESSION["user"] . "1|" . $_REQUEST["question"] . "|" . $_REQUEST["message"];
        $_SESSION["count"] += 1;
      }
      else
        $msg = $_SESSION["user"] . "1||start";
      if($_SESSION["count"] < 10 and $_SESSION["no_more"] != True){
        socket_write($s, $msg, strlen($msg));
        $ans = socket_read($s, 1024);
        if ($ans == "Thank you for participating in this survey!")
          $_SESSION["no_more"] = True;
        $_SESSION["c"] = $ans . "<br>\n";
        if($_SESSION["c"] == "")
        {
        	echo "Press submit to begin!";
        }
        else
        {
         	echo $_SESSION["c"];
        }
        socket_close($s);
    //}

?>
<br>
<!--<label>User Input<br>-->
<input type="hidden" name="question" value="<?php echo htmlspecialchars($_SESSION["c"]);?>">
TickTock:<input type="text" name="message" cols="48" rows="8"></label></p>
<?php
      }
    }

    if($_SESSION["count"] < 10 and $_SESSION["no_more"] != True)
    {
      echo "<input type=\"submit\" name=\"sendfeedback\" value=\"Send Message\"></p>";
    }
    else
      echo "Thank you for participating. Now you can go back to submit your task.<br>\n";
?>
</div>
</div>
</form>
