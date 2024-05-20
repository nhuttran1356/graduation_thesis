<?php
// Kết nối đến cơ sở dữ liệu MySQL
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "clean_machine";

// Tạo kết nối
$conn = new mysqli($servername, $username, $password, $dbname);

// Kiểm tra kết nối
if ($conn->connect_error) {
    die("Kết nối đến cơ sở dữ liệu thất bại: " . $conn->connect_error);
}

// Truy vấn dữ liệu từ cơ sở dữ liệu
$sql = "SELECT temperature, water_level, water_level_2, timestamp FROM sensor_reading";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // Thiết lập header của file CSV
    header('Content-Type: text/csv');
    header('Content-Disposition: attachment; filename="data_export.csv"');

    // Mở file để ghi dữ liệu
    $output = fopen('php://output', 'w');

    // Ghi header của file CSV
    fputcsv($output, array('Temperature', 'Water Level 1', 'Water Level 2', 'Timestamp'));

    // Ghi dữ liệu từ kết quả truy vấn vào file CSV
    while ($row = $result->fetch_assoc()) {
        fputcsv($output, $row);
    }

    // Đóng file
    fclose($output);
} else {
    echo "Không có dữ liệu để xuất ra file CSV.";
}

// Đóng kết nối cơ sở dữ liệu
$conn->close();
?>
