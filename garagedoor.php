<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
* {
  box-sizing: border-box;
}

.row::after {
  content: "";
  clear: both;
  display: table;
}

[class*="col-"] {
  float: left;
  padding: 15px;
}

.col-1 {width: 8.33%;}
.col-2 {width: 16.66%;}
.col-3 {width: 25%;}
.col-4 {width: 33.33%;}
.col-5 {width: 41.66%;}
.col-6 {width: 50%;}
.col-7 {width: 58.33%;}
.col-8 {width: 66.66%;}
.col-9 {width: 75%;}
.col-10 {width: 83.33%;}
.col-11 {width: 91.66%;}
.col-12 {width: 100%;}

html {
  font-family: "Lucida Sans", sans-serif;
}

.header {
  background-color: #9933cc;
  color: #ffffff;
  padding: 15px;
}

.row {
  list-style-type: none;
  margin: 0;
  padding: 0;
}

.row {
  padding: 8px;
  margin-bottom: 7px;
  background-color: #33b5e5;
  color: #ffffff;
  box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
}

.row :hover {
  background-color: #0099cc;
}

</style>
</head>
<body>

<div class="header">
  <h1>Trevor's Garage Door Main Page</h1>
</div>

<div class="row">
<?php
if(isset($_POST['button2'])) {
  # echo "Remote Operation Disabled";
  $myfile = fopen("disabledoor.txt", "w") or die("Unable to open!");
  fclose($myfile);
  chmod("disabledoor.txt",0777);  # Allow the Python app to delete it
}
if(isset($_POST['button3'])) {
  # echo "Remote Operation Enabled";
  unlink("disabledoor.txt");
}
?>
  <div class="col-3 menu">
  <p1>Control</p1>
    <form method="post">
      <input type="submit" name="button2" value="Disable"/>
      <br>
      <br>
      <input type="submit" name="button3" value="Enable"/>
    </form>
  </div>

  <div class="col-9">
    <h1>Garage Door Activation</h1>
    <p>Press button to activate the Garage Door</p>
    <p>Optionally Enable / Disable remote control of the Garage Door</p>

<?php
  //whether ip is from share internet
     if (!empty($_SERVER['HTTP_CLIENT_IP']))   
      {
        $ip_address = $_SERVER['HTTP_CLIENT_IP'];
      }
    //whether ip is from proxy
     elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR']))  
      {
        $ip_address = $_SERVER['HTTP_X_FORWARDED_FOR'];
      }
    //whether ip is from remote address
     else
      {
        $ip_address = $_SERVER['REMOTE_ADDR'];
      }

      if(isset($_POST['button1'])) {
        # echo "This is Button1 that is selected";
        $myfile = fopen("activatedoor.txt", "w") or die("Unable to open!");
        fwrite($myfile, $ip_address);
        fclose($myfile);
        chmod("activatedoor.txt",0777);  # Allow the Python app to delete it
        header("location: garagedoor.php");  # This line stops the POST occurring on a page refresh !!
        }
      
?>
<form method="post">
  <input type="submit" name="button1" value="Activate Door"/>
</form>

</div>
</div>

</body>

<?php
  $myfile = "disabledoor.txt";
  if (file_exists($myfile)) {
    echo "<p style='color:red;'>" . "Garage Door Remote Control Disabled" . "</p>";
  }
  $myfile = "notauthorised.txt";
  if (file_exists($myfile)) {
    echo "<p style='color:red;'>" . "NOT AUTHORISED" . "</p>";
  }
  // The function will refresh the page 
  // in every 1 second
  header("refresh: 1");
?>
<?php
  echo "<p style='color:blue;'>" . nl2br(file_get_contents( "garagetemp.txt" )); // get the contents, and echo it out.
?>
</html>