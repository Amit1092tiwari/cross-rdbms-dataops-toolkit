-- ============================================================================
-- Script: demo_hr_01_create_database.sql
-- Description: Creates and initializes the Demo_HR sample database for MySQL
--              data validation test suite and demo scenarios.
-- Engine: MySQL 5.7+ / 8.0+
-- ============================================================================

CREATE DATABASE IF NOT EXISTS Demo_HR
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE Demo_HR;
