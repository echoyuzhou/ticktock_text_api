<form method="POST" action="rate.php" accept-charset="UTF-8">
    <link rel="stylesheet" href="/css/bootstrap.min.css">
    <link rel="stylesheet" href="/css/rate.css">
    <body>

        <div class="container">
            <?php
                ini_set('display_errors', 'On');
                error_reporting(E_ALL);

                session_start();
                if (array_key_exists("rs_count", $_SESSION) and ($_SESSION["rs_count"] >= 20 or (array_key_exists("rs_count", $_SESSION) and $_SESSION["rs_count"] == 19 and array_key_exists("score", $_REQUEST) and $_REQUEST["score"] != 0)))
                {
                    if ($_SESSION["rs_count"] == 19)
                    {
                        $s = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
                        $result = socket_connect($s, "localhost", 11432);
                        $msg = $_SESSION["rs_rowid"] . "|" . $_SESSION["rs_turkid"] . "|" . $_REQUEST["score"];
                        socket_write($s, $msg, strlen($msg));
                        $_SESSION["rs_count"]++;
                    }

            ?>
            <h1 class="display-1">You've finished! Thanks for helping us improve TickTock. Your number is 322.</h1>
            <?php
                } elseif ((array_key_exists("rs_turkid", $_SESSION) and array_key_exists("rs_count", $_SESSION)) or array_key_exists("turkid", $_REQUEST))
                {
                    if (array_key_exists("turkid", $_REQUEST))
                    {
                        $_SESSION["rs_turkid"] = $_REQUEST["turkid"];
                        $_SESSION["rs_count"] = 0;
                    }
                    if ((array_key_exists("score", $_REQUEST) and $_REQUEST["score"] != 0) or !array_key_exists("rs_question", $_SESSION))
                    {
                        $s = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
                        $result = socket_connect($s, "localhost", 11432);

                        $msg = "0|" . $_SESSION["rs_turkid"] . "|0";
                        if (array_key_exists("score", $_REQUEST))
                        {
                            $msg = $_SESSION["rs_rowid"] . "|" . $_SESSION["rs_turkid"] . "|" . $_REQUEST["score"];
                            $_SESSION["rs_count"]++;
                        }
                        socket_write($s, $msg, strlen($msg));

                        $receipt = socket_read($s, 1024);
                        if ($receipt == 0)
                        {
                            $_SESSION["rs_count"] = 20;
            ?>
            <h1 class="display-1">You've finished! Thanks for helping us improve TickTock</h1>
            <?php
                        } else {
                            $msg_arr = explode("|", $receipt);
                            $_SESSION["rs_rowid"] = $msg_arr[0];
                            $_SESSION["rs_question"] = $msg_arr[1];
                            $_SESSION["rs_answer"] = $msg_arr[2];
                            $_SESSION["rs_prevq"] = $msg_arr[3];
                            $_SESSION["rs_preva"] = $msg_arr[4];
                        }
                    }
                    if ($_SESSION["rs_count"] < 20)
                    {
            ?>
            <h1>Below is a snapshot of TickTock's conversation with a user. Please rate the appropriateness of TickTock's last response.</h1>
            <ul class="list-group">
                <li class="list-group-item">User: <?php echo($_SESSION["rs_prevq"]); ?></li>
                <li class="list-group-item">TickTock: <?php echo($_SESSION["rs_preva"]); ?></li>
                <li class="list-group-item">User: <?php echo($_SESSION["rs_question"]); ?></li>
                <li class="list-group-item">TickTock: <?php echo($_SESSION["rs_answer"]); ?></li>
            <div class="rowshift">
                <div class="rowshift">
                    <h3>How appropriate is this response?</h3>
                </div>
            </div>
            <div class="row">
                <div class="col-xs-2">
                    <p class="text-danger" style="font-size:20px; text-align:center">1 - Inappropriate</p>
                </div>
                <div class="col-xs-3">
                    <p class="text-warning" style="font-size:20px; text-align:center">2 - Somewhat appropriate</p>
                </div>
                <div class="col-xs-2">
                    <p class="text-success" style="font-size:20px; text-align:center">3 - Appropriate</p>
                </div>
            </div>
            <div class="row">
                <div class="col-xs-8">
                    <select class="form-control" name="score">
                    <option value="0">Select...</option>
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                    </select>
                </div>
                <div class="col-xs-4">
                    <button class="btn btn btn-primary btn-lg" type="submit">Submit</button>
                </div>
            </div>
            <?php
                    }
                } else {
            ?>
            <h1 class="signin-title">Welcome to the TickTock 2.0 rating task!</h1>
            <h2 class="form-signin-heading">Please enter your Turk ID to proceed</h2>
            <div class="form-signin">
                <label for="inputTurkID" class="sr-only">Turk ID</label>
                <input type="text" name="turkid" class="form-control" placeholder="Enter Turk ID" required autofocus>
                <button class="btn btn-lg btn-primary btn-block" type="submit">Submit</button>
            </div>
            <?php
                }
            ?>
        </div> <!-- /container -->
    </body>
</form>
