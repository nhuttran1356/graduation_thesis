<?php 
    $servername = "localhost";
    $username = "root";
    $password = "";
    $db_name = "clean_machine";  
    $conn = new mysqli($servername, $username, $password, $db_name);
    if($conn->connect_error){
        die("Connection failed".$conn->connect_error);
    }
    // echo "Ket noi thanh cong";
    if(isset($_POST["temperature"]) && isset($_POST["water1"]) && isset($_POST["water2"])){
        
    
    $t = $_POST["temperature"];
    $w = $_POST["water1"];
    $w2 = $_POST["water2"];

// echo "Temperature: " . $t . "<br>";
// echo "Water1: " . $w . "<br>";
// echo "Water2: " . $w2 . "<br>";

    
    $sql = "INSERT INTO sensor_reading (temperature, water_level, water_level_2) VALUES(".$t.", ".$w.", ".$w2.")";
    if (mysqli_query($conn, $sql)) {   
        echo "\nInsert data sucessfully";
    }else{
        echo "Error: ";
    }
}
    ?>