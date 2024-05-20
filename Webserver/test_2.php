<?php
header('Content-Type: text/event-stream');
header('Cache-Control: no-cache');

// Kết nối cơ sở dữ liệu
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "clean_machine";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Kết nối đến cơ sở dữ liệu thất bại: " . $conn->connect_error);
}

echo "retry: 10000\n"; // Thời gian chờ để gửi lại kết nối (10 giây)

while (true) {
    // Truy vấn dữ liệu từ bảng sensor_reading trong cơ sở dữ liệu
    $sql = "SELECT temperature, water_level, water_level_2, timestamp FROM sensor_reading ORDER BY timestamp DESC LIMIT 1";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        $data = array(
            "temperature" => $row["temperature"],
            "water_level" => $row["water_level"],
            "water_level_2" => $row["water_level_2"],
            "timestamp" => $row["timestamp"]
        );
        echo "data: " . json_encode($data) . "\n\n"; // Gửi dữ liệu JSON cho client
        ob_flush();
        flush();
    }

    sleep(3); // Thời gian chờ giữa các lần kiểm tra dữ liệu mới
}
?>
