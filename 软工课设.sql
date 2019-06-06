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

 Date: 06/06/2019 00:32:58
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

-- ----------------------------
-- Table structure for user_bought_history
-- ----------------------------
DROP TABLE IF EXISTS `user_bought_history`;
CREATE TABLE `user_bought_history`  (
  `user_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `bought_date` int(11) NOT NULL,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `item_id`(`item_id`) USING BTREE,
  INDEX `bought_date`(`bought_date`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Fixed;

SET FOREIGN_KEY_CHECKS = 1;
