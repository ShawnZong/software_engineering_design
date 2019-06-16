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

 Date: 16/06/2019 12:18:10
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for dim_items
-- ----------------------------
DROP TABLE IF EXISTS `dim_items`;
CREATE TABLE `dim_items`  (
  `item_id` int(11) NOT NULL,
  `item_belong` int(11) NOT NULL,
  `item_title` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  PRIMARY KEY (`item_id`) USING BTREE,
  INDEX `item_id`(`item_id`) USING BTREE,
  INDEX `item_belong`(`item_belong`) USING BTREE,
  FULLTEXT INDEX `item_title`(`item_title`)
) ENGINE = MyISAM CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
