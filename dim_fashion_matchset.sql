/*
 Navicat Premium Data Transfer

 Source Server         : mydb
 Source Server Type    : MySQL
 Source Server Version : 50721
 Source Host           : localhost:3306
 Source Schema         : softwareengineering

 Target Server Type    : MySQL
 Target Server Version : 50721
 File Encoding         : 65001

 Date: 16/06/2019 12:18:00
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for dim_fashion_matchset
-- ----------------------------
DROP TABLE IF EXISTS `dim_fashion_matchset`;
CREATE TABLE `dim_fashion_matchset`  (
  `match_id` int(11) NOT NULL,
  `match_items` longtext CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL,
  PRIMARY KEY (`match_id`) USING BTREE,
  FULLTEXT INDEX `match_items`(`match_items`)
) ENGINE = MyISAM CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
