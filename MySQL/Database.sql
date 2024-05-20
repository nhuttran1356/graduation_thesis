-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 13, 2024 at 02:03 PM
-- Server version: 10.4.25-MariaDB
-- PHP Version: 7.4.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `clean_machine`
--

-- --------------------------------------------------------

--
-- Table structure for table `sensor_reading`
--

CREATE TABLE `sensor_reading` (
  `id` int(11) NOT NULL,
  `temperature` float DEFAULT NULL,
  `water_level` float DEFAULT NULL,
  `water_level_2` float DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_name` varchar(20) DEFAULT NULL,
  `password` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_name`, `password`) VALUES
('admin', '123456'),
('minhnhut', '1234'),
('minhnhut', '1234');


--
-- Indexes for table `sensor_reading`
--
ALTER TABLE `sensor_reading`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables

-- AUTO_INCREMENT for table `sensor_reading`

