CREATE DATABASE IF NOT EXISTS `todolist`;
USE `todolist`;

CREATE TABLE IF NOT EXISTS `users` (
  `Username` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '유저ID',
  `Email` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '이메일',
  `FullName` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '전체 이름',
  `Disabled` tinyint(1) DEFAULT '0' COMMENT '사용자 활성화 여부 (0: enable, 1: disable)',
  `Password` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '비밀번호',
  `Permission` tinyint(1) NOT NULL DEFAULT '0' COMMENT '유저 권한 (0: GUEST, 1: NORMAL, 2: ADMIN)',
  PRIMARY KEY (`Username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `users` (`Username`, `Email`, `FullName`, `Disabled`, `Password`, `Permission`) VALUES ('tester', 'nexters@kakao.com', 'Deo Kim', 0, '$2b$12$uxeFffwSDVXQ7O3r7c1zJu/dMixGyXqLPq9gmumG1PYANzGpjBnYy', 1);
