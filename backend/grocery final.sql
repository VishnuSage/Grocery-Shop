-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 26, 2023 at 01:14 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `grocery`
--

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `cid` int(11) NOT NULL,
  `cname` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`cid`, `cname`) VALUES
(1, 'Fruits'),
(2, 'Vegetables'),
(3, 'dairy');

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE `login` (
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `usertype` varchar(10) NOT NULL DEFAULT 'user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`username`, `password`, `usertype`) VALUES
('a', '123', 'user'),
('a1@gmail.com', '123', 'user'),
('a2@gmail.com', '111', 'user'),
('a@gmail.com', '123', 'user'),
('aa', 'aa', 'admin'),
('aa@gmail.com', '123', 'user'),
('aswin', '123', 'user'),
('aswin@gmail.com', '123', 'user');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` float NOT NULL,
  `order_date` date DEFAULT curdate(),
  `status` varchar(100) NOT NULL,
  `username` varchar(100) NOT NULL,
  `orderid` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `item_id`, `quantity`, `price`, `order_date`, `status`, `username`, `orderid`) VALUES
(33, 7, 1, 80, '2023-01-25', 'Declined', 'a', ''),
(34, 6, 1, 130, '2023-01-25', '', 'a@gmail.com', ''),
(35, 13, 1, 40, '2023-01-25', '', 'a@gmail.com', ''),
(37, 7, 1, 80, '2023-01-25', 'Accepted', 'a', ''),
(40, 5, 1, 100, '2023-02-04', '', 'a', ''),
(46, 5, 2, 100, '2023-02-06', 'Accepted', 'a', ''),
(47, 7, 1, 80, '2023-02-06', 'Accepted', 'a', ''),
(48, 5, 1, 100, '2023-02-06', 'Declined', 'a', ''),
(49, 7, 1, 80, '2023-02-06', '', 'a', ''),
(50, 11, 1, 50, '2023-02-06', '', 'a', ''),
(51, 12, 1, 60, '2023-02-06', '', 'a', ''),
(52, 4, 2, 120, '2023-02-06', 'Accepted', 'a', ''),
(53, 4, 1, 120, '2023-02-06', 'Declined', 'a', ''),
(66, 11, 2, 50, '2023-02-19', '', 'a', '_Olv5w'),
(67, 10, 1, 40, '2023-02-19', '', 'a', '_Olv5w'),
(68, 4, 1, 120, '2023-02-19', '', 'a', '71wLNA'),
(69, 5, 1, 100, '2023-02-19', '', 'a', '71wLNA'),
(70, 7, 1, 80, '2023-02-19', '', 'a', 'Eo7wpw'),
(71, 8, 1, 50, '2023-02-19', '', 'a', '6H0_nQ'),
(75, 7, 2, 80, '2023-02-19', '', 'a', 'gwY0LA'),
(76, 8, 1, 50, '2023-02-19', '', 'a', 'gwY0LA'),
(77, 5, 1, 100, '2023-02-20', '', 'a', 'H08iIg'),
(78, 5, 1, 100, '2023-02-20', '', 'a', 'lnrUVg'),
(79, 8, 1, 50, '2023-02-20', '', 'a', 'lnrUVg'),
(80, 4, 1, 120, '2023-02-20', '', 'a', '2G0ArQ');

-- --------------------------------------------------------

--
-- Table structure for table `shipping`
--

CREATE TABLE `shipping` (
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(10) NOT NULL,
  `address` varchar(100) NOT NULL,
  `state` varchar(100) NOT NULL,
  `district` varchar(100) NOT NULL,
  `zip` int(11) NOT NULL,
  `ordid` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `shipping`
--

INSERT INTO `shipping` (`name`, `email`, `phone`, `address`, `state`, `district`, `zip`, `ordid`) VALUES
('sdsd', 'a@gmail.com', '213', 'sd', 'zsffs', 'sdf', 13, 'gwY0LA'),
('sdsd', 'A@gmail.com', '213', 'sd', 'zsffs', 'sdf', 13, 'H08iIg'),
('sdsd', 'a@gmail.com', '213', 'sd', 'zsffs', 'sdf', 13, 'lnrUVg'),
('sdsd', 'adsfewfw', '213', 'sd', 'zsffs', 'sdf', 13, '2G0ArQ');

-- --------------------------------------------------------

--
-- Table structure for table `stock`
--

CREATE TABLE `stock` (
  `itemid` int(11) NOT NULL,
  `iname` varchar(100) NOT NULL,
  `category` int(11) NOT NULL,
  `price` int(11) NOT NULL,
  `Quantity` int(11) NOT NULL,
  `Description` varchar(500) NOT NULL,
  `image` varchar(800) NOT NULL,
  `pstatus` varchar(100) NOT NULL DEFAULT 'ACTIVE'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `stock`
--

INSERT INTO `stock` (`itemid`, `iname`, `category`, `price`, `Quantity`, `Description`, `image`, `pstatus`) VALUES
(4, 'Apple', 1, 120, 12, 'Fresh', 'product-img-5.jpg', 'ACTIVE'),
(5, 'Lemon', 1, 100, 6, 'Sweet', 'product-img-3.jpg', 'ACTIVE'),
(6, 'Orange', 1, 130, 9, 'fresh and sweet', 'orange.jpg', 'INACTIVE'),
(7, 'Grapes', 1, 80, 2, 'fresh', 'grapes.jpg', 'ACTIVE'),
(8, 'Watermelon', 1, 50, 8, 'Juicy', 'watermelon.jpg', 'ACTIVE'),
(9, 'Mango', 1, 100, 8, 'Sweet', 'Mango.jpg', 'ACTIVE'),
(10, 'Tomato', 2, 40, 5, 'Fresh', 'tomato.jpg', 'ACTIVE'),
(11, 'Potato', 2, 50, 6, 'fresh', 'potato.jpg', 'ACTIVE'),
(12, 'Carrot', 2, 60, 6, 'Fresh', 'carrot.jpg', 'ACTIVE'),
(13, 'Onion', 2, 40, 4, 'Fresh', 'onion.jpg', 'ACTIVE');

-- --------------------------------------------------------

--
-- Table structure for table `supplier`
--

CREATE TABLE `supplier` (
  `sid` int(11) NOT NULL,
  `sname` varchar(100) NOT NULL,
  `contact` int(11) NOT NULL,
  `address` varchar(200) NOT NULL,
  `sstatus` varchar(100) NOT NULL DEFAULT 'ACTIVE'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `supplier`
--

INSERT INTO `supplier` (`sid`, `sname`, `contact`, `address`, `sstatus`) VALUES
(1, 'Aswin', 5786822, 'hjgjk', 'ACTIVE'),
(2, 'Vishnu', 8507022, 'sjkyflgk', 'ACTIVE'),
(3, 'Aljo', 967764563, 'jfuglik', 'ACTIVE'),
(4, 'Janak', 6608609, 'uyfuyui', 'ACTIVE'),
(6, 'aron', 454313, 'gjhjhvbmnn', 'ACTIVE');

-- --------------------------------------------------------

--
-- Table structure for table `userdetails`
--

CREATE TABLE `userdetails` (
  `username` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `address` varchar(200) NOT NULL,
  `phone` int(11) NOT NULL,
  `pin` int(11) NOT NULL,
  `state` varchar(100) NOT NULL,
  `district` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `userdetails`
--

INSERT INTO `userdetails` (`username`, `name`, `address`, `phone`, `pin`, `state`, `district`) VALUES
('a', 'sdsd', 'sd', 213, 13, 'zsffs', 'sdf'),
('a2@gmail.com', 'aaa', 'aaa', 11, 11, 'aa', 'aa'),
('a@gmail.com', 'sss', 'ss', 111, 111, 'ss', 'ss'),
('aswin', 'aswin', 'aa', 222, 22, 'aa', 'aa'),
('aswin@gmail.com', 'Aswin', 'aaaa', 12345, 12345, 'ssss', 'ssss');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`cid`);

--
-- Indexes for table `login`
--
ALTER TABLE `login`
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `stock`
--
ALTER TABLE `stock`
  ADD PRIMARY KEY (`itemid`);

--
-- Indexes for table `supplier`
--
ALTER TABLE `supplier`
  ADD PRIMARY KEY (`sid`);

--
-- Indexes for table `userdetails`
--
ALTER TABLE `userdetails`
  ADD PRIMARY KEY (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `category`
--
ALTER TABLE `category`
  MODIFY `cid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=81;

--
-- AUTO_INCREMENT for table `stock`
--
ALTER TABLE `stock`
  MODIFY `itemid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `supplier`
--
ALTER TABLE `supplier`
  MODIFY `sid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
