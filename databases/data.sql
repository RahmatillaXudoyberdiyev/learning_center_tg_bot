-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: learning_center
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `branch`
--

DROP TABLE IF EXISTS `branch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `branch` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `info` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `branch`
--

LOCK TABLES `branch` WRITE;
/*!40000 ALTER TABLE `branch` DISABLE KEYS */;
INSERT INTO `branch` VALUES (1,'Minor','Minorda joylashgan'),(2,'Filial 1','Bu Toshkent shahridagi asosiy filial.'),(3,'Filial 2','Bu Samarqand shahridagi filial.'),(4,'Filial 3','Bu Buxoro shahridagi filial.'),(5,'Filial 4','Bu Andijon shahridagi filial.'),(6,'Filial 5','Bu Farg?ona shahridagi filial.');
/*!40000 ALTER TABLE `branch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `info` text NOT NULL,
  `branch_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_course_info` (`branch_id`),
  CONSTRAINT `fk_course_info` FOREIGN KEY (`branch_id`) REFERENCES `branch` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT INTO `course` VALUES (1,'Matematika','Matematika otiladi',1),(2,'Ingilis tili','Ingilis tilini organish',1),(3,'Matematika','Matematika asoslari kursi.',1),(4,'Fizika','Fizika fanidan chuqur bilimlar kursi.',1),(5,'Ingliz tili','Ingliz tilini boshlang?ich darajada o?rganish kursi.',2),(6,'Dasturlash asoslari','Python dasturlash tilini o?rganish kursi.',2),(7,'Tarix','O?zbekiston tarixi kursi.',3),(8,'Kimyo','Kimyo fanidan amaliy mashg?ulotlar kursi.',3),(9,'Biologiya','Biologiya fanidan chuqur bilimlar kursi.',4),(10,'Geografiya','Dunyo geografiyasi kursi.',4),(11,'Rus tili','Rus tilini boshlang?ich darajada o?rganish kursi.',5),(12,'Marketing','Zamonaviy marketing strategiyalari kursi.',5),(13,'Dizayn','Grafik dizayn asoslari kursi.',1),(14,'Sotsiologiya','Ijtimoiy munosabatlar va tahlil kursi.',2),(15,'Psixologiya','Shaxs psixologiyasi kursi.',3),(16,'Buxgalteriya','Buxgalteriya hisobi kursi.',4),(17,'Menejment','Biznesni boshqarish kursi.',5),(18,'Huquqshunoslik','Huquqiy bilimlar kursi.',1),(19,'Iqtisodiyot','Makroiqtisodiyot va mikroiqtisodiyot kursi.',2),(20,'Sun?iy intellekt','AI va ma?lumotlar tahlili kursi.',3),(21,'Tibbiyot','Tibbiyot asoslari kursi.',4),(22,'Pedagogika','Zamonaviy pedagogika usullari kursi.',5);
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(50) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `datetime` datetime NOT NULL,
  `username` varchar(50) NOT NULL,
  `t_id` int NOT NULL,
  `course_id` int NOT NULL,
  `branch_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `course_id` (`course_id`),
  KEY `branch_id` (`branch_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Ali Valiyev','+998901234567','2023-10-01 09:00:00','ali_valiyev',1001,1,1),(2,'Gulnora Xolmirzayeva','+998902345678','2023-10-01 10:00:00','gulnora_x',1002,2,1),(3,'Hasan Hasanov','+998903456789','2023-10-01 11:00:00','hasan_hasan',1003,3,2),(4,'Zarina Qodirova','+998904567890','2023-10-01 12:00:00','zarina_q',1004,4,2),(5,'Olim Olimov','+998905678901','2023-10-01 13:00:00','olim_o',1005,5,3),(6,'Dilnoza Yusupova','+998906789012','2023-10-01 14:00:00','dilnoza_y',1006,6,3),(7,'Javlon Jumayev','+998907890123','2023-10-01 15:00:00','javlon_j',1007,7,4),(8,'Malika Karimova','+998908901234','2023-10-01 16:00:00','malika_k',1008,8,4),(9,'Farhod Farhodov','+998909012345','2023-10-01 17:00:00','farhod_f',1009,9,5),(10,'Laylo Nurmatova','+998910123456','2023-10-01 18:00:00','laylo_n',1010,10,5),(11,'Sarvar Rajabov','+998911234567','2023-10-02 09:00:00','sarvar_r',1011,11,1),(12,'Dilbar Xasanova','+998912345678','2023-10-02 10:00:00','dilbar_x',1012,12,2),(13,'Shoxrux Shodiyev','+998913456789','2023-10-02 11:00:00','shoxrux_s',1013,13,3),(14,'Gulbahor Toshpulatova','+998914567890','2023-10-02 12:00:00','gulbahor_t',1014,14,4),(15,'Bahodir Bahodirov','+998915678901','2023-10-02 13:00:00','bahodir_b',1015,15,5),(16,'Nodira Nodirova','+998916789012','2023-10-02 14:00:00','nodira_n',1016,16,1),(17,'Rustam Rustamov','+998917890123','2023-10-02 15:00:00','rustam_r',1017,17,2),(18,'Sevara Ismoilova','+998918901234','2023-10-02 16:00:00','sevara_i',1018,18,3),(19,'Aziz Azizov','+998919012345','2023-10-02 17:00:00','aziz_a',1019,19,4),(20,'Yulduz Yuldasheva','+998920123456','2023-10-02 18:00:00','yulduz_y',1020,20,5),(21,'Kamol Kamolov','+998921234567','2023-10-03 09:00:00','kamol_k',1021,1,1),(22,'Dilfuza Rahimova','+998922345678','2023-10-03 10:00:00','dilfuza_r',1022,2,1),(23,'Sherzod Sherzodov','+998923456789','2023-10-03 11:00:00','sherzod_s',1023,3,2),(24,'Madina Madinabonu','+998924567890','2023-10-03 12:00:00','madina_m',1024,4,2),(25,'Islom Islomov','+998925678901','2023-10-03 13:00:00','islom_i',1025,5,3),(26,'Zuhra Zuhrova','+998926789012','2023-10-03 14:00:00','zuhra_z',1026,6,3),(27,'Jahongir Jahongirov','+998927890123','2023-10-03 15:00:00','jahongir_j',1027,7,4),(28,'Fotima Fotimova','+998928901234','2023-10-03 16:00:00','fotima_f',1028,8,4),(29,'Sardor Sardorov','+998929012345','2023-10-03 17:00:00','sardor_s',1029,9,5),(30,'Munisa Munisova','+998930123456','2023-10-03 18:00:00','munisa_m',1030,10,5),(31,'Akmal Akmalov','+998931234567','2023-10-04 09:00:00','akmal_a',1031,11,1),(32,'Dilnoza Dilnozabonu','+998932345678','2023-10-04 10:00:00','dilnoza_d',1032,12,2),(33,'Shavkat Shavkatov','+998933456789','2023-10-04 11:00:00','shavkat_s',1033,13,3),(34,'Gulnoza Gulnozabonu','+998934567890','2023-10-04 12:00:00','gulnoza_g',1034,14,4),(35,'Bobur Boburov','+998935678901','2023-10-04 13:00:00','bobur_b',1035,15,5),(36,'Nigora Nigorabonu','+998936789012','2023-10-04 14:00:00','nigora_n',1036,16,1),(37,'Ravshan Ravshanov','+998937890123','2023-10-04 15:00:00','ravshan_r',1037,17,2),(38,'Saida Saidabonu','+998938901234','2023-10-04 16:00:00','saida_s',1038,18,3),(39,'Tohir Tohirov','+998939012345','2023-10-04 17:00:00','tohir_t',1039,19,4),(40,'Xurshida Xurshidabonu','+998940123456','2023-10-04 18:00:00','xurshida_x',1040,20,5),(41,'Farida Faridabonu','+998941234567','2023-10-05 09:00:00','farida_f',1041,1,1),(42,'Ulugbek Ulugbekov','+998942345678','2023-10-05 10:00:00','ulugbek_u',1042,2,1),(43,'Zafar Zafarov','+998943456789','2023-10-05 11:00:00','zafar_z',1043,3,2),(44,'Muhayyo Muhayyobonu','+998944567890','2023-10-05 12:00:00','muhayyo_m',1044,4,2),(45,'Jamshid Jamshidov','+998945678901','2023-10-05 13:00:00','jamshid_j',1045,5,3),(46,'Dilshod Dilshodov','+998946789012','2023-10-05 14:00:00','dilshod_d',1046,6,3),(47,'Shahlo Shahlo','+998947890123','2023-10-05 15:00:00','shahlo_s',1047,7,4),(48,'Ibrohim Ibrohimov','+998948901234','2023-10-05 16:00:00','ibrohim_i',1048,8,4),(49,'Zilola Zilolabonu','+998949012345','2023-10-05 17:00:00','zilola_z',1049,9,5),(50,'Asad Asadov','+998950123456','2023-10-05 18:00:00','asad_a',1050,10,5),(51,'Lola Lolabonu','+998951234567','2023-10-06 09:00:00','lola_l',1051,11,1),(52,'Bekzod Bekzodov','+998952345678','2023-10-06 10:00:00','bekzod_b',1052,12,2),(53,'Shirin Shirinbonu','+998953456789','2023-10-06 11:00:00','shirin_s',1053,13,3),(54,'Jasur Jasurov','+998954567890','2023-10-06 12:00:00','jasur_j',1054,14,4),(55,'Mavluda Mavludabonu','+998955678901','2023-10-06 13:00:00','mavluda_m',1055,15,5),(56,'Rustamjon Rustamjonov','+998956789012','2023-10-06 14:00:00','rustamjon_r',1056,16,1),(57,'Dilafruz Dilafruz','+998957890123','2023-10-06 15:00:00','dilafruz_d',1057,17,2),(58,'Shohruh Shohruhov','+998958901234','2023-10-06 16:00:00','shohruh_s',1058,18,3),(59,'Gulmira Gulmira','+998959012345','2023-10-06 17:00:00','gulmira_g',1059,19,4),(60,'Farrux Farruxov','+998960123456','2023-10-06 18:00:00','farrux_f',1060,20,5),(61,'Nargiza Nargizabonu','+998961234567','2023-10-07 09:00:00','nargiza_n',1061,1,1),(62,'Sherali Sheraliev','+998962345678','2023-10-07 10:00:00','sherali_s',1062,2,1),(63,'Dilshoda Dilshoda','+998963456789','2023-10-07 11:00:00','dilshoda_d',1063,3,2),(64,'Murod Murodov','+998964567890','2023-10-07 12:00:00','murod_m',1064,4,2),(65,'Zarina Zarina','+998965678901','2023-10-07 13:00:00','zarina_z',1065,5,3),(66,'Shahzod Shahzodov','+998966789012','2023-10-07 14:00:00','shahzod_s',1066,6,3),(67,'Gulchehra Gulchehra','+998967890123','2023-10-07 15:00:00','gulchehra_g',1067,7,4),(68,'Jahongir Jahongirov','+998968901234','2023-10-07 16:00:00','jahongir_j',1068,8,4),(69,'Dilbar Dilbar','+998969012345','2023-10-07 17:00:00','dilbar_d',1069,9,5),(70,'Farhod Farhodov','+998970123456','2023-10-07 18:00:00','farhod_f',1070,10,5),(71,'Laylo Laylo','+998971234567','2023-10-08 09:00:00','laylo_l',1071,11,1),(72,'Sarvar Sarvarov','+998972345678','2023-10-08 10:00:00','sarvar_s',1072,12,2),(73,'Dilshod Dilshodov','+998973456789','2023-10-08 11:00:00','dilshod_d',1073,13,3),(74,'Gulnoza Gulnoza','+998974567890','2023-10-08 12:00:00','gulnoza_g',1074,14,4),(75,'Bahodir Bahodirov','+998975678901','2023-10-08 13:00:00','bahodir_b',1075,15,5),(76,'Nodira Nodira','+998976789012','2023-10-08 14:00:00','nodira_n',1076,16,1),(77,'Rustam Rustamov','+998977890123','2023-10-08 15:00:00','rustam_r',1077,17,2),(78,'Sevara Sevara','+998978901234','2023-10-08 16:00:00','sevara_s',1078,18,3),(79,'Aziz Azizov','+998979012345','2023-10-08 17:00:00','aziz_a',1079,19,4),(80,'Yulduz Yulduz','+998980123456','2023-10-08 18:00:00','yulduz_y',1080,20,5),(81,'Kamol Kamolov','+998981234567','2023-10-09 09:00:00','kamol_k',1081,1,1),(82,'Dilfuza Dilfuza','+998982345678','2023-10-09 10:00:00','dilfuza_d',1082,2,1),(83,'Sherzod Sherzodov','+998983456789','2023-10-09 11:00:00','sherzod_s',1083,3,2),(84,'Madina Madina','+998984567890','2023-10-09 12:00:00','madina_m',1084,4,2),(85,'Islom Islomov','+998985678901','2023-10-09 13:00:00','islom_i',1085,5,3),(86,'Zuhra Zuhra','+998986789012','2023-10-09 14:00:00','zuhra_z',1086,6,3),(87,'Jahongir Jahongirov','+998987890123','2023-10-09 15:00:00','jahongir_j',1087,7,4),(88,'Fotima Fotima','+998988901234','2023-10-09 16:00:00','fotima_f',1088,8,4),(89,'Sardor Sardorov','+998989012345','2023-10-09 17:00:00','sardor_s',1089,9,5),(90,'Munisa Munisa','+998990123456','2023-10-09 18:00:00','munisa_m',1090,10,5),(91,'Akmal Akmalov','+998991234567','2023-10-10 09:00:00','akmal_a',1091,11,1),(92,'Dilnoza Dilnoza','+998992345678','2023-10-10 10:00:00','dilnoza_d',1092,12,2),(93,'Shavkat Shavkatov','+998993456789','2023-10-10 11:00:00','shavkat_s',1093,13,3),(94,'Gulnoza Gulnoza','+998994567890','2023-10-10 12:00:00','gulnoza_g',1094,14,4),(95,'Bobur Boburov','+998995678901','2023-10-10 13:00:00','bobur_b',1095,15,5),(96,'Nigora Nigora','+998996789012','2023-10-10 14:00:00','nigora_n',1096,16,1),(97,'Ravshan Ravshanov','+998997890123','2023-10-10 15:00:00','ravshan_r',1097,17,2),(98,'Saida Saida','+998998901234','2023-10-10 16:00:00','saida_s',1098,18,3),(99,'Tohir Tohirov','+998999012345','2023-10-10 17:00:00','tohir_t',1099,19,4),(100,'Xurshida Xurshida','+998999123456','2023-10-10 18:00:00','xurshida_x',1100,20,5);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-31  7:29:31
