-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Dec 22, 2022 at 06:59 PM
-- Server version: 5.7.36
-- PHP Version: 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `uas_pwm`
--

-- --------------------------------------------------------

--
-- Table structure for table `produk`
--

DROP TABLE IF EXISTS `produk`;
CREATE TABLE IF NOT EXISTS `produk` (
  `id_prd` varchar(200) NOT NULL,
  `prdName` varchar(200) NOT NULL,
  `qty` int(200) NOT NULL,
  `Category` varchar(200) NOT NULL,
  `price` int(200) NOT NULL,
  PRIMARY KEY (`id_prd`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `produk`
--

INSERT INTO `produk` (`id_prd`, `prdName`, `qty`, `Category`, `price`) VALUES
('01', 'monitor', 20, 'electronic', 30000),
('02', 'skirt', 12, 'clothes', 20000),
('03', 'guitar', 15, 'music', 40000);

-- --------------------------------------------------------

--
-- Table structure for table `transaksi`
--

DROP TABLE IF EXISTS `transaksi`;
CREATE TABLE IF NOT EXISTS `transaksi` (
  `invoiceID` varchar(200) NOT NULL,
  `date` varchar(200) NOT NULL,
  `name` varchar(200) NOT NULL,
  `total` int(200) NOT NULL,
  `diskon` int(200) NOT NULL,
  `grand total` int(200) NOT NULL,
  PRIMARY KEY (`invoiceID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `transaksi`
--

INSERT INTO `transaksi` (`invoiceID`, `date`, `name`, `total`, `diskon`, `grand total`) VALUES
('01', '01 November 2022', 'caca', 100000, 20, 80000),
('02', '11 December 2022', 'epen', 100000, 30, 70000),
('03', '28 December 2022', 'jasonnn', 100000, 10, 90000);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
