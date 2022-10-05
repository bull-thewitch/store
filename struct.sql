SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

DROP TABLE IF EXISTS `pr_cat`;
CREATE TABLE IF NOT EXISTS `pr_cat` (
  `pr_id` int(10) UNSIGNED NOT NULL,
  `cat_id` int(10) UNSIGNED NOT NULL,
  KEY `index_pr` (`pr_id`),
  KEY `index_cat` (`cat_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `ord_pr`;
CREATE TABLE IF NOT EXISTS `ord_pr` (
  `ord_id` int(10) UNSIGNED NOT NULL,
  `pr_id` int(10) UNSIGNED NOT NULL,
  `qty` int(10) UNSIGNED NOT NULL,
  KEY `index_ord` (`ord_id`),
  KEY `index_pr` (`pr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `category`;
CREATE TABLE IF NOT EXISTS `category` (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL CHECK (`name` <> ''),
  `parent_id` int(10) UNSIGNED DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_parent` (`parent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `order`;
CREATE TABLE IF NOT EXISTS `order` (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `total` decimal(8,2) UNSIGNED NOT NULL,
  `date` date NOT NULL,
  `done` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `product`;
CREATE TABLE IF NOT EXISTS `product` (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL CHECK (`name` <> ''),
  `descr` text NOT NULL,
  `qty` int(10) UNSIGNED NOT NULL,
  `price` decimal(6,2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


ALTER TABLE `category`
  ADD CONSTRAINT `category_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `category` (`id`);

ALTER TABLE `ord_pr`
  ADD CONSTRAINT `ord_pr_ibfk_1` FOREIGN KEY (`ord_id`) REFERENCES `order` (`id`),
  ADD CONSTRAINT `ord_pr_ibfk_2` FOREIGN KEY (`pr_id`) REFERENCES `product` (`id`);

ALTER TABLE `pr_cat`
  ADD CONSTRAINT `pr_cat_ibfk_1` FOREIGN KEY (`pr_id`) REFERENCES `product` (`id`),
  ADD CONSTRAINT `pr_cat_ibfk_2` FOREIGN KEY (`cat_id`) REFERENCES `category` (`id`);