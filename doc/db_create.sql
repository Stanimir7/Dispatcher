-- MySQL Script generated by MySQL Workbench
-- Wed 15 Nov 2017 05:39:03 PM EST
-- Model: New Model    Version: 1.0
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
CREATE SCHEMA IF NOT EXISTS `dispatcher` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `dispatcher` ;

-- -----------------------------------------------------
-- Table `dispatcher`.`Business`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dispatcher`.`Business` (
  `idBusiness` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `BusName` VARCHAR(128) NULL,
  `DefaultAddress` VARCHAR(256) NULL,
  `DefaultPhone` CHAR(15) NULL,
  `MerchantID` VARCHAR(256) NOT NULL COMMENT 'Clover-given ID of the merchant',
  `BusinessURL` CHAR(10) NULL,
  PRIMARY KEY (`idBusiness`),
  UNIQUE INDEX `idBusiness_UNIQUE` (`idBusiness` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dispatcher`.`Driver`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dispatcher`.`Driver` (
  `idDriver` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `FirstName` VARCHAR(32) NULL,
  `LastName` VARCHAR(32) NULL,
  `PhoneNumber` CHAR(15) NOT NULL,
  `Enrolled` TINYINT(1) NOT NULL DEFAULT 1,
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
  `DriverStatus` ENUM('claimed', 'complete', 'canceled','business_closed') NOT NULL DEFAULT 'claimed' COMMENT 'For auditing purposes; \"how many Jobs has this Driver canceled?\" Canceled here implies driver canceled',
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


-- -----------------------------------------------------
-- Table `dispatcher`.`JobDriverURL`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dispatcher`.`JobDriverURL` (
  `idJobDriverURL` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `URL` CHAR(8) NOT NULL,
  `fk_idDriver` INT UNSIGNED NOT NULL,
  `fk_idJob` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`idJobDriverURL`),
  UNIQUE INDEX `URL_UNIQUE` (`URL` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dispatcher`.`DriverConfirmCode`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dispatcher`.`DriverConfirmCode` (
  `idDriverConfirmCode` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `fk_idDriver` INT UNSIGNED NOT NULL,
  `ConfirmCode` CHAR(6) NULL,
  `TIMESTAMP` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`idDriverConfirmCode`),
  UNIQUE INDEX `idDriverConfirmCode_UNIQUE` (`idDriverConfirmCode` ASC),
  INDEX `fk_DriverConfirmCode_Driver_idx` (`fk_idDriver` ASC),
  CONSTRAINT `fk_DriverConfirmCode_Driver`
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
CREATE PROCEDURE `create_job`(
	IN p_idBusiness INT,
    IN p_title VARCHAR(64),
    IN p_desc VARCHAR(256),
    IN p_from_loc VARCHAR(256),
    IN p_to_loc VARCHAR(256),
    IN p_bus_phone CHAR(15)
)
BEGIN
	DECLARE busID INT;
    SELECT idBusiness INTO busID FROM Business WHERE idBusiness = p_idBusiness;
    
    
    if ( busID IS NULL ) THEN
     
		select 'error' AS 'status', 'Invalid Business ID' AS 'message';
        
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
        
        IF ( SELECT NOT EXISTS (SELECT 1  
			FROM Driver 
			WHERE Driver.idDriver IN (
					SELECT BusinessDriver.fk_idDriver 
					FROM BusinessDriver 
					WHERE BusinessDriver.fk_idBusiness = busID AND 
					BusinessDriver.HireStatus = 'hired')
			) ) 
		THEN
			SELECT 'info' AS 'status', 'No drivers registered for this business. ' AS 'message';
        ELSE
			SELECT Driver.idDriver, Driver.PhoneNumber, LAST_INSERT_ID() AS 'idJob', 'success' AS 'status'  
			FROM Driver 
			WHERE Driver.idDriver IN (
					SELECT BusinessDriver.fk_idDriver 
					FROM BusinessDriver 
					WHERE BusinessDriver.fk_idBusiness = busID AND 
					BusinessDriver.HireStatus = 'hired')
			;
        END IF;
     
    END IF;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure new_business
-- -----------------------------------------------------

DELIMITER $$
USE `dispatcher`$$
CREATE PROCEDURE `new_business` (
	IN p_merch_id VARCHAR(256),
    IN p_name VARCHAR(128),
    IN p_address VARCHAR(256),
    IN p_phone CHAR(15),
    IN p_url CHAR(10)

)
BEGIN
	IF (SELECT EXISTS (SELECT 1 FROM Business WHERE MerchantID = p_merch_id)) THEN
		SELECT 'error' AS 'status', 'Merchant ID already exists' AS 'message';
    ELSE
		INSERT INTO Business
        (
			MerchantID,
            BusName,
            DefaultAddress,
            DefaultPhone,
            BusinessURL
        )
        VALUES
        (
			p_merch_id,
            p_name,
            p_address,
            p_phone,
            p_url
        );
		SELECT 'success' AS 'status';
    END IF;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure driver_claim_job
-- -----------------------------------------------------

DELIMITER $$
USE `dispatcher`$$
CREATE PROCEDURE `driver_claim_job` (
	IN p_idJob INT,
    IN p_idDriver INT
)
BEGIN
	IF ( SELECT EXISTS (SELECT 1 FROM JobDriver WHERE fk_idJob = p_idJob AND (DriverStatus = 'claimed' OR DriverStatus = 'completed')) ) THEN
        SELECT 'info' AS 'status', 'job_claimed' AS 'message';
    ELSEIF ( SELECT NOT EXISTS (SELECT 1 FROM Driver WHERE idDriver = p_idDriver ) ) THEN
		SELECT 'error' AS 'status', 'invalid_driver_id' AS 'message';
	ELSEIF ( SELECT NOT EXISTS (SELECT 1 FROM Job WHERE idJob = p_idJob ) ) THEN
		SELECT 'error' AS 'status', 'invalid_job_id' AS 'message';
    ELSEIF ( SELECT EXISTS (SELECT 1 FROM Job WHERE idJob = p_idJob AND JobStatus != 'pending' ) ) THEN
		SELECT 'info' AS 'status', 'job_not_available' AS 'message';
    ELSE
     
        INSERT INTO JobDriver
        (
            fk_idJob,
            fk_idDriver,
            DriverStatus,
            DriverClaimTime
        )
        VALUES
        (
            p_idJob,
            p_idDriver,
            'claimed',
            NOW()
        );
        
        
        UPDATE Job SET JobStatus = 'claimed' WHERE idJob = p_idJob;
        SELECT 'success' AS 'status';
     
    END IF;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure new_driver
-- -----------------------------------------------------

DELIMITER $$
USE `dispatcher`$$
CREATE PROCEDURE `new_driver` (
	IN p_firstName VARCHAR(32),
    IN p_lastName VARCHAR(32),
    IN p_phone CHAR(15)
	
)
BEGIN
	IF ( SELECT EXISTS (SELECT 1 FROM Driver WHERE PhoneNumber = p_phone AND Enrolled = TRUE) ) THEN
		SELECT 'error' AS 'status', 'Driver already registered' AS 'message';
	
    ELSEIF ( SELECT EXISTS (SELECT 1 FROM Driver WHERE PhoneNumber = p_phone AND Enrolled = FALSE) ) THEN
		UPDATE Driver SET FirstName = p_firstName, LastName = p_lastName, Enrolled = TRUE WHERE PhoneNumber = p_phone;
	
	
    ELSE
     
        INSERT INTO Driver
        (
            FirstName,
            LastName,
            PhoneNumber
        )
        VALUES
        (
            p_firstName,
            p_lastName,
            p_phone
        );
     
    END IF;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure driver_close_job
-- -----------------------------------------------------

DELIMITER $$
USE `dispatcher`$$
CREATE PROCEDURE `driver_close_job` (
	IN p_idDriver INT,
    IN p_idJob INT,
    IN p_status ENUM('complete', 'canceled')
)
BEGIN
	IF ( SELECT NOT EXISTS (SELECT 1 FROM JobDriver WHERE fk_idDriver = p_idDriver AND fk_idJob = p_idJob AND DriverStatus = 'claimed') ) THEN
        SELECT 'error' AS 'status', 'Invalid params' AS 'message';
    ELSE
		
        IF (p_status = 'complete') THEN
			UPDATE Job
            SET JobStatus = 'complete'
            WHERE idJob = p_idJob;
		ELSEIF (p_status = 'canceled') THEN
			UPDATE Job
            SET JobStatus = 'pending'
            WHERE idJob = p_idJob;
        END IF;
        
        UPDATE JobDriver
        SET DriverStatus = p_status,
			DriverCloseTime = NOW()
		WHERE fk_idJob = p_idJob AND fk_idDriver = p_idDriver;
	END IF;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure new_business_driver
-- -----------------------------------------------------

DELIMITER $$
USE `dispatcher`$$
CREATE PROCEDURE `new_business_driver` (
	IN p_idDriver INT,
    IN p_idBusiness INT

)
BEGIN
	IF (SELECT EXISTS (SELECT 1 FROM BusinessDriver WHERE fk_idDriver = p_idDriver AND fk_idBusiness = p_idBusiness)) THEN
		SELECT 'error' AS 'status', 'Business/Driver relationship already exists' AS 'message';
	ELSE
		INSERT INTO BusinessDriver
        (
            HireDate,
            HireStatus,
            fk_idBusiness,
            fk_idDriver

            
        )
        VALUES
        (
            CURDATE(),
            'pending',
            p_idBusiness,
            p_idDriver
        );
    END IF;

END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure mod_business_driver
-- -----------------------------------------------------

DELIMITER $$
USE `dispatcher`$$
CREATE PROCEDURE `mod_business_driver` (
	IN p_idDriver INT,
    IN p_idBusiness INT,
    IN p_status ENUM('pending', 'hired','blocked')

)
BEGIN
	IF (SELECT NOT EXISTS (SELECT 1 FROM BusinessDriver WHERE fk_idDriver = p_idDriver AND fk_idBusiness = p_idBusiness)) THEN
		SELECT 'error' AS 'status', 'Business/Driver relationship does not exist' AS 'message';
	ELSE
		UPDATE 	BusinessDriver
        SET	
				HireStatus = p_status
		WHERE 	fk_idDriver = p_idDriver AND 
				fk_idBusiness = p_idBusiness;
    END IF;

END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure get_driver
-- -----------------------------------------------------

DELIMITER $$
USE `dispatcher`$$
CREATE PROCEDURE `get_driver` (
	IN p_phone CHAR(15)
)
BEGIN
	DECLARE ID INT;
    SELECT idDriver INTO ID FROM Driver WHERE PhoneNumber = p_phone;
    
    
    if ( ID IS NULL ) THEN
     
		select 'error' AS 'status', 'Driver not registered' AS 'message';
        
    ELSE
		SELECT ID AS 'idDriver';
     
    END IF;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure new_confirm_code
-- -----------------------------------------------------

DELIMITER $$
USE `dispatcher`$$
CREATE PROCEDURE `new_confirm_code` (
	IN p_idDriver INT,
    IN p_code CHAR(6)
)
BEGIN
	IF ( (SELECT NOT EXISTS (SELECT 1 FROM Driver WHERE idDriver = p_idDriver )) OR (SELECT EXISTS (SELECT 1 FROM Driver WHERE idDriver = p_idDriver AND Enrolled = FALSE )) ) THEN
		SELECT 'error' AS 'status', 'Driver is not registered' AS 'message';
	    
    ELSE
		INSERT INTO DriverConfirmCode
        (
            fk_idDriver,
            ConfirmCode
        )
        VALUES
        (
            p_idDriver,
            p_code
        );
        SELECT LAST_INSERT_ID() AS 'key';
	END IF;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure check_confirm_code
-- -----------------------------------------------------

DELIMITER $$
USE `dispatcher`$$
CREATE PROCEDURE `check_confirm_code` (
	IN p_id INT,
    IN p_code CHAR(6)
)
BEGIN
	DECLARE ID INT;
    SELECT fk_idDriver INTO ID FROM DriverConfirmCode WHERE idDriverConfirmCode = p_id AND ConfirmCode = p_code;
    
    IF ( ID IS NULL ) THEN
		SELECT 'invalid' AS 'status';
	ELSE 
		SELECT 'success' AS 'status', ID AS 'idDriver';
	END IF;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure get_assoc_businesses
-- -----------------------------------------------------

DELIMITER $$
USE `dispatcher`$$
CREATE PROCEDURE `get_assoc_businesses` (
	IN p_idDriver INT
)
BEGIN
	SELECT 	d.*, b.BusName, h.HireDate, h.HireStatus, h.idBusinessDriver
    FROM	Driver d
			JOIN BusinessDriver h ON d.idDriver = h.fk_idDriver
            JOIN Business b ON h.fk_idBusiness = b.idBusiness
	WHERE d.idDriver = p_idDriver;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure delete_confirm_code
-- -----------------------------------------------------

DELIMITER $$
USE `dispatcher`$$
CREATE PROCEDURE `delete_confirm_code` (
	IN p_id INT
)
BEGIN
	DELETE FROM DriverConfirmCode WHERE idDriverConfirmCode = p_id;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure delete_driver
-- -----------------------------------------------------

DELIMITER $$
USE `dispatcher`$$
CREATE PROCEDURE `delete_driver` (
	IN p_drop BOOL,
    IN p_idDriver INT,
    IN p_idList TEXT
)
BEGIN
	IF (p_drop) THEN
		DELETE FROM BusinessDriver WHERE fk_idDriver = p_idDriver;
        UPDATE Driver SET Enrolled = FALSE WHERE idDriver = p_idDriver;
	ELSE
		DELETE FROM BusinessDriver 
        WHERE FIND_IN_SET(idBusinessDriver, p_idList) > 0;
    END IF;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure get_business
-- -----------------------------------------------------

DELIMITER $$
USE `dispatcher`$$
CREATE PROCEDURE `get_business` (
IN p_merch VARCHAR(256)
)
BEGIN
	IF (SELECT NOT EXISTS (SELECT 1 FROM Business WHERE MerchantID = p_merch)) THEN
		SELECT 'error' AS 'status', 'Business not registered. '  AS 'message';
	ELSE
		SELECT * FROM Business WHERE MerchantID = p_merch;
	END IF;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure new_job_driver_url
-- -----------------------------------------------------

DELIMITER $$
USE `dispatcher`$$
CREATE PROCEDURE `new_job_driver_url` (
	IN p_idDriver INT,
    IN p_idJob INT,
    IN p_URL CHAR(8)
)
BEGIN
	IF ( SELECT EXISTS (SELECT 1 FROM JobDriverURL WHERE fk_idDriver = p_idDriver AND fk_idJob = p_idJob) ) THEN
		SELECT 'error' AS 'status', 'URL already exists' AS 'message';
	ELSE
		INSERT JobDriverURL 
        (
			fk_idDriver,
            fk_idJob,
            URL
		)
        VALUES 
        (
			p_idDriver,
            p_idJob,
            p_URL
		);
        
        SELECT 'success' AS 'status';
        
    END IF;
END
$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure get_job_driver_from_url
-- -----------------------------------------------------

DELIMITER $$
USE `dispatcher`$$
CREATE PROCEDURE `get_job_driver_from_url` (
	IN p_URL CHAR(8)
)
BEGIN
	IF ( SELECT NOT EXISTS (SELECT 1 FROM JobDriverURL WHERE URL = p_URL) ) THEN
		SELECT 'error' AS 'status', 'URL does not exist' AS 'message';
	ELSE
    
		SELECT 	j.*, d.*, b.*
        FROM 	JobDriverURL jdu
				JOIN Job j ON j.idJob = jdu.fk_idJob
                JOIN Driver d ON d.idDriver = jdu.fk_idDriver
                JOIN Business b ON b.idBusiness = j.fk_idBusiness
        WHERE 	URL = p_URL;
    
    END IF;
END
$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure job_avail
-- -----------------------------------------------------

DELIMITER $$
USE `dispatcher`$$
CREATE PROCEDURE `job_avail` (
	IN p_idJob INT
)
BEGIN
	IF ( SELECT NOT EXISTS (SELECT 1 FROM Job WHERE idJob = p_idJob) ) THEN
		SELECT 'error' AS 'status', 'Job does not exist' AS 'message';
	ELSEIF ( SELECT EXISTS (SELECT 1 FROM Job WHERE idJob = p_idJob AND JobStatus = 'pending') ) THEN
		SELECT 'success' AS 'status', 'true' AS 'avail';
	ELSE
		SELECT 'success' AS 'status', 'false' AS 'avail';
	END IF;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure get_assoc_job_driver
-- -----------------------------------------------------

DELIMITER $$
USE `dispatcher`$$
CREATE PROCEDURE `get_assoc_job_driver` (
	IN p_idJob INT
)
BEGIN
DECLARE ID INT;
SELECT  jd.fk_idDriver INTO ID
FROM	JobDriver jd
WHERE 	jd.fk_idJob = p_idJob AND
		jd.DriverStatus = 'claimed';
        
	IF ( ID IS NULL ) THEN
     
		select 'error' AS 'status', 'No valid driver exists.' AS 'message';
        
    ELSE
        SELECT	'success' AS 'status', ID AS 'idDriver';
	END IF;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure get_assoc_drivers
-- -----------------------------------------------------

DELIMITER $$
USE `dispatcher`$$
CREATE PROCEDURE `get_assoc_drivers` (
	IN p_idBusiness INT
)
BEGIN
	SELECT 	d.*, b.*, h.*
    FROM	Business b
			JOIN BusinessDriver h ON h.fk_idBusiness = b.idBusiness
			JOIN Driver d ON d.idDriver = h.fk_idDriver
	WHERE b.idBusiness = p_idBusiness;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure get_url_from_driver_job
-- -----------------------------------------------------

DELIMITER $$
USE `dispatcher`$$
CREATE PROCEDURE `get_url_from_driver_job` (
	IN p_idDriver INT,
    IN p_idJob INT
)
BEGIN
	
	SELECT * FROM JobDriverURL WHERE fk_idDriver = p_idDriver AND fk_idJob = p_idJob;
	

END
$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure business_close_job
-- -----------------------------------------------------

DELIMITER $$
USE `dispatcher`$$
CREATE PROCEDURE `business_close_job` (
    IN p_idJob INT,
    IN p_status ENUM('complete', 'canceled')
)
BEGIN
	IF ( SELECT NOT EXISTS (SELECT 1 FROM Job WHERE idJob = p_idJob) ) THEN
        SELECT 'error' AS 'status', 'Invalid params' AS 'message';
    ELSE
		
        IF (p_status = 'complete') THEN
			UPDATE Job
            SET JobStatus = 'complete'
            WHERE idJob = p_idJob;
            
            UPDATE JobDriver
            SET DriverStatus = 'business_closed',
			    DriverCloseTime = NOW()
		    WHERE fk_idJob = p_idJob AND (DriverStatus != 'complete');
		ELSEIF (p_status = 'canceled') THEN
			UPDATE Job
            SET JobStatus = 'canceled'
            WHERE idJob = p_idJob;
            
            UPDATE JobDriver
            SET DriverStatus = 'business_closed',
			    DriverCloseTime = NOW()
		    WHERE fk_idJob = p_idJob AND (DriverStatus != 'complete');
        END IF;
        
        
	END IF;
END$$

DELIMITER ;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
