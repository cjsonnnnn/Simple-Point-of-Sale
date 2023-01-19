-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Dec 29, 2022 at 11:28 AM
-- Server version: 5.7.36
-- PHP Version: 8.0.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `spos`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
CREATE TABLE IF NOT EXISTS `admin` (
  `id` varchar(9) NOT NULL,
  `password` varchar(9) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `password`) VALUES
('admA', 'pwAA');

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

DROP TABLE IF EXISTS `cart`;
CREATE TABLE IF NOT EXISTS `cart` (
  `id` varchar(18) NOT NULL,
  `date` varchar(27) NOT NULL,
  `total_qty` int(11) NOT NULL,
  `discount` int(11) NOT NULL,
  `price` int(11) NOT NULL,
  `grand_price` int(11) NOT NULL,
  `username` varchar(9) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `username` (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`id`, `date`, `total_qty`, `discount`, `price`, `grand_price`, `username`) VALUES
('ca-1', '29/12/2022', 0, 36, 0, 0, 'cusA'),
('ca-2', '20221227232531', 0, 36, 0, 0, 'cusB');

-- --------------------------------------------------------

--
-- Table structure for table `cart_product`
--

DROP TABLE IF EXISTS `cart_product`;
CREATE TABLE IF NOT EXISTS `cart_product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` varchar(18) NOT NULL,
  `cart_id` varchar(18) NOT NULL,
  `qty` int(11) NOT NULL,
  `subtotal` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  KEY `cart_id` (`cart_id`)
) ENGINE=MyISAM AUTO_INCREMENT=118 DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
CREATE TABLE IF NOT EXISTS `category` (
  `id` varchar(18) NOT NULL,
  `name` varchar(27) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`id`, `name`) VALUES
('ctg-1', 'Technology'),
('ctg-2', 'Camera'),
('ctg-3', 'Microphone'),
('ctg-4', 'Guitar');

-- --------------------------------------------------------

--
-- Table structure for table `category_product`
--

DROP TABLE IF EXISTS `category_product`;
CREATE TABLE IF NOT EXISTS `category_product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` varchar(18) NOT NULL,
  `category_id` varchar(18) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  KEY `category_id` (`category_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `category_product`
--

INSERT INTO `category_product` (`id`, `product_id`, `category_id`) VALUES
(1, 'prd-1', 'ctg-1'),
(2, 'prd-1', 'ctg-2'),
(3, 'prd-2', 'ctg-1'),
(4, 'prd-2', 'ctg-3');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
CREATE TABLE IF NOT EXISTS `customer` (
  `username` varchar(9) NOT NULL,
  `password` varchar(9) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`username`, `password`) VALUES
('cusA', 'pwCA'),
('cusB', 'pwCB');

-- --------------------------------------------------------

--
-- Table structure for table `invoice`
--

DROP TABLE IF EXISTS `invoice`;
CREATE TABLE IF NOT EXISTS `invoice` (
  `id` varchar(18) NOT NULL,
  `date` varchar(27) NOT NULL,
  `total_qty` int(11) NOT NULL,
  `total_price` int(11) NOT NULL,
  `username` varchar(9) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `username` (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `invoice`
--

INSERT INTO `invoice` (`id`, `date`, `total_qty`, `total_price`, `username`) VALUES
('inv-20221228023927', '28/12/2022', 9, 14400000, 'cusA'),
('inv-20221228034644', '28/12/2022', 6, 9216000, 'cusA'),
('inv-20221228074954', '28/12/2022', 6, 9216000, 'cusA'),
('inv-1228083313185', '28/12/2022', 7, 10368000, 'cusA'),
('inv-1228083614815', '28/12/2022', 9, 12672000, 'cusA'),
('inv-1228195825051', '28/12/2022', 13, 19584000, 'cusA'),
('inv-1229181237623', '29/12/2022', 6, 9792000, 'cusA');

-- --------------------------------------------------------

--
-- Table structure for table `invoice_product`
--

DROP TABLE IF EXISTS `invoice_product`;
CREATE TABLE IF NOT EXISTS `invoice_product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` varchar(18) NOT NULL,
  `invoice_id` varchar(18) NOT NULL,
  `qty` int(11) NOT NULL,
  `subtotal` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  KEY `invoice_id` (`invoice_id`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `invoice_product`
--

INSERT INTO `invoice_product` (`id`, `product_id`, `invoice_id`, `qty`, `subtotal`) VALUES
(1, 'prd-2', 'inv-20221228023927', 2, 3600000),
(2, 'prd-1', 'inv-20221228023927', 7, 18900000),
(3, 'prd-2', 'inv-20221228034644', 2, 3600000),
(4, 'prd-1', 'inv-20221228034644', 4, 10800000),
(5, 'prd-2', 'inv-20221228074954', 2, 3600000),
(6, 'prd-1', 'inv-20221228074954', 4, 10800000),
(7, 'prd-2', 'inv-1228083313185', 3, 5400000),
(8, 'prd-1', 'inv-1228083313185', 4, 10800000),
(9, 'prd-2', 'inv-1228083614815', 5, 9000000),
(10, 'prd-1', 'inv-1228083614815', 4, 10800000),
(11, 'prd-2', 'inv-1228195825051', 5, 9000000),
(12, 'prd-1', 'inv-1228195825051', 8, 21600000),
(13, 'prd-2', 'inv-1229181237623', 1, 1800000),
(14, 'prd-1', 'inv-1229181237623', 5, 13500000);

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
CREATE TABLE IF NOT EXISTS `product` (
  `id` varchar(18) NOT NULL,
  `name` varchar(54) NOT NULL,
  `price` int(11) NOT NULL,
  `img_link` varchar(999) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`id`, `name`, `price`, `img_link`) VALUES
('prd-1', 'Sony X1', 2700000, 'https://tinyurl.com/h5mzuukd'),
('prd-2', 'Shure Microphone', 1800000, 'https://tinyurl.com/mr36xp8h');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
