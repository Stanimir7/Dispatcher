-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema dispatcher
-- -----------------------------------------------------
-- Primary Schema for Dispatcher Application

-- -----------------------------------------------------
-- Schema dispatcher
--
-- Primary Schema for Dispatcher Application
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `dispatcher` DEFAULT CHARACTER SET utf8 ;
USE `dispatcher` ;

-- -----------------------------------------------------
-- Table `dispatcher`.`Business`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dispatcher`.`Business` (
  `idBusiness` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `BusName` VARCHAR(128) NULL,
  `DefaultAddress` VARCHAR(256) NULL,
  `DefaultPhone` CHAR(15) NULL,
  `MerchantID` CHAR(32) NOT NULL COMMENT 'Clover-given ID of the merchant',
  PRIMARY KEY (`idBusiness`),
  UNIQUE INDEX `idBusiness_UNIQUE` (`idBusiness` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dispatcher`.`Driver`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dispatcher`.`Driver` (
  `idDriver` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `DriverName` VARCHAR(64) NULL,
  `PhoneNumber` CHAR(15) NOT NULL,
  PRIMARY KEY (`idDriver`),
  UNIQUE INDEX `idDriver_UNIQUE` (`idDriver` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dispatcher`.`Job`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dispatcher`.`Job` (
  `idJob` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `BusContactPhone` CHAR(15) NULL COMMENT 'Business Contact Phone',
  `FromLoc` VARCHAR(256) NULL COMMENT 'The start location',
  `ToLoc` VARCHAR(256) NULL,
  `JobTitle` VARCHAR(64) NULL,
  `JobDesc` VARCHAR(256) NULL,
  `JobStatus` ENUM('pending', 'claimed', 'complete', 'canceled') NOT NULL DEFAULT 'pending' COMMENT 'canceled here implies business canceled the job',
  `fk_idBusiness` INT UNSIGNED NOT NULL,
  `JobCreateTime` DATETIME NOT NULL,
  `JobCloseTime` DATETIME NULL,
  PRIMARY KEY (`idJob`),
  UNIQUE INDEX `idJob_UNIQUE` (`idJob` ASC),
  INDEX `fk_idBusiness_idx` (`fk_idBusiness` ASC),
  CONSTRAINT `fk_idBusiness_Job`
    FOREIGN KEY (`fk_idBusiness`)
    REFERENCES `dispatcher`.`Business` (`idBusiness`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dispatcher`.`BusinessDriver`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dispatcher`.`BusinessDriver` (
  `idBusinessDriver` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `HireDate` DATE NULL,
  `HireStatus` ENUM('pending', 'hired', 'blocked') NOT NULL DEFAULT 'pending',
  `fk_idBusiness` INT UNSIGNED NOT NULL,
  `fk_idDriver` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`idBusinessDriver`),
  INDEX `fk_idBusiness_idx` (`fk_idBusiness` ASC),
  INDEX `fk_idDriver_idx` (`fk_idDriver` ASC),
  UNIQUE INDEX `idBusinessDriver_UNIQUE` (`idBusinessDriver` ASC),
  CONSTRAINT `fk_idBusiness_BusinessDriver`
    FOREIGN KEY (`fk_idBusiness`)
    REFERENCES `dispatcher`.`Business` (`idBusiness`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_idDriver_BusinessDriver`
    FOREIGN KEY (`fk_idDriver`)
    REFERENCES `dispatcher`.`Driver` (`idDriver`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dispatcher`.`JobDriver`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dispatcher`.`JobDriver` (
  `idJobDriver` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `fk_idJob` INT UNSIGNED NOT NULL COMMENT 'The Business that has created the Job',
  `fk_idDriver` INT UNSIGNED NOT NULL COMMENT 'The Driver that has claimed the job',
  `DriverStatus` ENUM('claimed', 'complete', 'canceled') NOT NULL DEFAULT 'claimed' COMMENT 'For auditing purposes; \"how many Jobs has this Driver canceled?\" Canceled here implies driver canceled',
  `DriverClaimTime` DATETIME NOT NULL,
  `DriverCloseTime` DATETIME NULL,
  PRIMARY KEY (`idJobDriver`),
  INDEX `fk_idDriver_idx` (`fk_idDriver` ASC),
  INDEX `fk_idJob_idx` (`fk_idJob` ASC),
  CONSTRAINT `fk_idJob_JobDriver`
    FOREIGN KEY (`fk_idJob`)
    REFERENCES `dispatcher`.`Job` (`idJob`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_idDriver_JobDriver`
    FOREIGN KEY (`fk_idDriver`)
    REFERENCES `dispatcher`.`Driver` (`idDriver`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

USE `dispatcher` ;

-- -----------------------------------------------------
-- procedure create_job
-- -----------------------------------------------------

DELIMITER $$
USE `dispatcher`$$
CREATE DEFINER='root'@'localhost' PROCEDURE `create_job`(
	IN p_merch_id CHAR(32),
    IN p_title VARCHAR(64),
    IN p_desc VARCHAR(256),
    IN p_from_loc VARCHAR(256),
    IN p_to_loc VARCHAR(256),
    IN p_bus_phone CHAR(15)
)
BEGIN
	DECLARE busID INT;
    SELECT idBusiness INTO busID FROM dispatcher.Business WHERE MerchantID = p_merch_id;
    
    
    if ( busID IS NULL ) THEN
     
		select 'error' AS 'status', 'Invalid merchant ID' AS 'message';
        
    ELSE
     
		insert into Job
        (
            BusContactPhone,
            FromLoc,
            ToLoc,
            JobTitle,
            JobDesc,
            JobStatus,
			fk_idBusiness,
            JobCreateTime
        )
        values
        (
            p_bus_phone,
            p_from_loc,
            p_to_loc,
            p_title,
            p_desc,
            'pending',
            busID,
            NOW()

        );
        
		SELECT dispatcher.Driver.PhoneNumber 
        FROM dispatcher.Driver 
        WHERE dispatcher.Driver.idDriver IN (
				SELECT BusinessDriver.fk_idDriver 
                FROM dispatcher.BusinessDriver 
                WHERE BusinessDriver.fk_idBusiness = busID AND 
                BusinessDriver.HireStatus = 'hired')
		;
     
    END IF;
END$$

DELIMITER ;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

