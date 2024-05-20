<?php
// Kết nối cơ sở dữ liệu
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "clean_machine";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Kết nối đến cơ sở dữ liệu thất bại: " . $conn->connect_error);
}


// Writing a mysql query to retrieve data  
$sql = "SELECT temperature, water_level, water_level_2, timestamp FROM sensor_reading";
$result = $conn->query($sql);
$dataPoints = array();
while ($row = $result->fetch_assoc()) {
    // Lấy dữ liệu từ các trường temperature, water_level, water_level_2 và timestamp
    $dataPoints[] = array(
        "temperature" => $row["temperature"],
        "water_level" => $row["water_level"],
        "water_level_2" => $row["water_level_2"],
        "timestamp" => $row["timestamp"]
    );
}

// Trả về dữ liệu dưới dạng JSON
header('Content-Type: application/json');
echo json_encode($dataPoints);


// Closing mysql connection 
$conn->close();
?>