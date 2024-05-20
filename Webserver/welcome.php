<?php include('connection.php');

?>
<!DOCTYPE html>
<html>

<head>
    <title>Temperature and Water Level Graph</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>

<body>
    <style>
        body {
            text-align: center;
            /* Căn giữa nội dung trên trang */
            font-family: Arial, sans-serif;
            /* Chọn font chữ phù hợp */
            margin: 0;
            padding: 0;
        }

        h1 {
            font-size: 28px;
            /* Kích thước font chữ cho tiêu đề */
            color: #333;
            /* Màu chữ */
        }

        .chart-container {
            display: inline-block;
            width: 45%;
            /* Điều chỉnh chiều rộng của từng biểu đồ */
            margin: 10px;
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

        /* CSS để tùy chỉnh giao diện cho nút */
        .btn {
                padding: 10px 20px;
                /* Điều chỉnh padding cho nút */
                font-size: 16px;
                /* Kích thước font chữ */
                background-color: #4CAF50;
                /* Màu nền */
                color: white;
                /* Màu chữ */
                border: none;
                /* Loại bỏ viền */
                border-radius: 4px;
                /* Bo tròn viền nút */
                cursor: pointer;
                /* Biểu tượng chuột khi di chuyển qua nút */
                transition: background-color 0.3s;
                /* Hiệu ứng thay đổi màu nền khi hover */
            }

            /* Hiệu ứng khi hover */
            .btn:hover {
                background-color: #45a049;
                /* Màu nền khi hover */
            }
    </style>
    <div class="navbar">
        <span class="navbar-brand">
            <img src="Logo-DH-Su-Pham-Ky-Thuat-TP-Ho-Chi-Minh-HCMUTE.jpg" alt="Logo">
            Ho Chi Minh University Of Technology And Education - Mechatronics
        </span>
        <!-- Thêm các liên kết khác tại đây -->
    </div>
    <h1>Temperature and Water Level Graph</h1>
    <div>
        <div class="chart-container">
            <canvas id="temperatureChart"></canvas>
        </div>
        <div class="chart-container">
            <canvas id="waterLevelChart"></canvas>
        </div>
        <div class="chart-container">
            <canvas id="waterLevel2Chart"></canvas>
        </div>
    </div>
    <button id="exportButton" class="btn">Export Data</button>


    <script>
        const temperatureChart = new Chart(document.getElementById('temperatureChart').getContext('2d'), {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Temperature',
                    data: [],
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });

        const waterLevelChart = new Chart(document.getElementById('waterLevelChart').getContext('2d'), {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Water Level 1',
                    data: [],
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });

        const waterLevel2Chart = new Chart(document.getElementById('waterLevel2Chart').getContext('2d'), {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Water Level 2',
                    data: [],
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });

        // JavaScript để lắng nghe dữ liệu từ SSE và cập nhật biểu đồ
        if (typeof(EventSource) !== 'undefined') {
            const source = new EventSource('test_2.php');

            source.addEventListener('message', function(event) {
                const data = JSON.parse(event.data);

                // Cập nhật labels và data của biểu đồ nhiệt độ
                temperatureChart.data.labels.push(data.timestamp);
                temperatureChart.data.datasets[0].data.push(parseFloat(data.temperature));
                temperatureChart.update();

                // Cập nhật labels và data của biểu đồ mức nước 1
                waterLevelChart.data.labels.push(data.timestamp);
                waterLevelChart.data.datasets[0].data.push(parseFloat(data.water_level));
                waterLevelChart.update();

                // Cập nhật labels và data của biểu đồ mức nước 2
                waterLevel2Chart.data.labels.push(data.timestamp);
                waterLevel2Chart.data.datasets[0].data.push(parseFloat(data.water_level_2));
                waterLevel2Chart.update();
            }, false);
        } else {
            console.log('Trình duyệt không hỗ trợ Server-Sent Events.');
        }


        document.getElementById('exportButton').addEventListener('click', function() {
            fetch('export_data.php', {
                    method: 'POST'
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Có lỗi khi xuất dữ liệu ra CSV');
                    }
                    return response.blob();
                })
                .then(blob => {
                    const url = window.URL.createObjectURL(new Blob([blob]));
                    const link = document.createElement('a');
                    link.href = url;
                    link.setAttribute('download', 'data_export.csv');
                    document.body.appendChild(link);
                    link.click();
                    link.parentNode.removeChild(link);
                })
                .catch(error => {
                    console.error('Lỗi khi xuất dữ liệu ra CSV:', error);
                });
        });
    </script>
</body>

</html>