-- phpMyAdmin SQL Dump
-- version 4.3.8deb0.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Gegenereerd op: 27 sep 2015 om 22:19
-- Serverversie: 5.6.19-0ubuntu0.14.04.1
-- PHP-versie: 5.5.9-1ubuntu4.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `yjmpd`
--

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `tracks`
--

CREATE TABLE IF NOT EXISTS `tracks` (
  `id` int(11) NOT NULL,
  `genre` varchar(100) DEFAULT NULL,
  `trackUrl` varchar(200) NOT NULL,
  `trackName` varchar(100) DEFAULT NULL,
  `artistName` varchar(100) DEFAULT NULL,
  `albumName` varchar(100) DEFAULT NULL,
  `albumArtist` varchar(100) DEFAULT NULL,
  `trackNumber` int(11) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `duration` time DEFAULT NULL,
  `playCount` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB AUTO_INCREMENT=8135 DEFAULT CHARSET=latin1;

--
-- Indexen voor geëxporteerde tabellen
--

--
-- Indexen voor tabel `tracks`
--
ALTER TABLE `tracks`
  ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `trackUrl` (`trackUrl`);

--
-- AUTO_INCREMENT voor geëxporteerde tabellen
--

--
-- AUTO_INCREMENT voor een tabel `tracks`
--
ALTER TABLE `tracks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=8135;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
