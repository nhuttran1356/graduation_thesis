<!-- <?php
        include("connection.php");
        include("login.php")
        ?>
    
<html>
    <head>
        <title>Login</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" type="text/css" href="style.php">
    </head>
    <body>
        
        <div id="form">
            <h1>Clean Machine IOT</h1>
            <form name="form" action="login.php" onsubmit="return isvalid()" method="POST">
                <label>Username: </label>
                <input type="text" id="user" name="user"></br></br>
                <label>Password: </label>
                <input type="password" id="pass" name="pass"></br></br>
                <input type="submit" id="btn" value="Login" name = "submit"/>
            </form>
        </div>
        <script>
            function isvalid(){
                var user = document.form.user.value;
                var pass = document.form.pass.value;
                if(user.length=="" && pass.length==""){
                    alert(" Username and password field is empty!!!");
                    return false;
                }
                else if(user.length==""){
                    alert(" Username field is empty!!!");
                    return false;
                }
                else if(pass.length==""){
                    alert(" Password field is empty!!!");
                    return false;
                }
                
            }
        </script>
    </body>
</html> 
 -->

<?php
include("connection.php");
include("login.php");
?>
<html>

<head>
    <title>Login</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- <link rel="stylesheet" type="text/css" href="style_1.php"> -->
    

    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <title>Login Form | CodingLab</title> 
    <link rel="stylesheet" href="style_1.php">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.2/css/all.min.css"/>


    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f2eade;
        }

        .navbar {
            overflow: hidden;
            background-color: #d6d0d0;
            color: #a14949;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 20px;
            font-weight: bold;
        }

        .navbar a {
            float: left;
            display: block;
            color: white;
            text-align: center;
            padding: 14px 20px;
            text-decoration: none;
        }

        .navbar a:hover {
            background-color: #ddd;
            color: black;
        }

        .navbar-brand {
            font-size: 24px;
            margin: 0;
            padding: 0;
            display: flex;
            align-items: center;
        }

        .navbar-brand img {
            max-width: 60px;
            max-height: 60px;
            margin-right: 20px;
        }
    </style>
</head>

<body>

    <!-- Navbar -->
    <div class="navbar">
        <span class="navbar-brand">
            <img src="Logo-DH-Su-Pham-Ky-Thuat-TP-Ho-Chi-Minh-HCMUTE.jpg" alt="Logo">
            Ho Chi Minh University Of Technology And Education - Mechatronics
        </span>
        <!-- Thêm các liên kết khác tại đây -->
    </div>

    <div class="container">
      <div class="wrapper">
      
        <div class="title"><span>IOT Webserver</span></div>
        <form action="login.php" onsubmit="return isvalid()" method="POST">
        <div class="row">
            <i class="fas fa-user"></i>
            <input type="text" id ="user"  name="user" placeholder="Username" required>
          </div>
          <div class="row">
            <i class="fas fa-lock"></i>
            <input type="password" id = "pass" name="pass" placeholder="Password" required>
          </div>

          <div class="row button">
            <input type="submit" id="btn" name="submit" value="Login">
          </div>
        </form>
      </div>
    </div>

    <!-- <div id="form">
        <h1></h1>
        <form name="form" action="login.php" onsubmit="return isvalid()" method="POST">
            <label for="user">Username: </label>
            <input type="text" id="user" name="user" required><br><br>
            <label for="pass">Password: </label>
            <input type="password" id="pass" name="pass" required><br><br>
            <input type="submit" id="btn" value="Login" name="submit">
        </form>
    </div> -->

    <script>
        function isvalid() {
            var user = document.form.user.value;
            var pass = document.form.pass.value;
            if (user.length === 0 && pass.length === 0) {
                alert("Username and password field is empty!!!");
                return false;
            } else if (user.length === 0) {
                alert("Username field is empty!!!");
                return false;
            } else if (pass.length === 0) {
                alert("Password field is empty!!!");
                return false;
            }
        }
    </script>

</body>

</html>