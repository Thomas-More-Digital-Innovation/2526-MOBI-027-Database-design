CREATE DATABASE IF NOT EXISTS Jobtakels;
USE Jobtakels;

-- Disable foreign key checks to allow dropping tables in any order
SET FOREIGN_KEY_CHECKS = 0;

-- Drop tables if they exist
DROP TABLE IF EXISTS HAS_PROPERTY;
DROP TABLE IF EXISTS HAS_AIM;
DROP TABLE IF EXISTS GIVES_POSTURAL_SUPPORT_IN;
DROP TABLE IF EXISTS TRANSFERS_FORCES_FROM;
DROP TABLE IF EXISTS TRANSFERS_FORCES_TO;
DROP TABLE IF EXISTS ExoProperty;
DROP TABLE IF EXISTS Exo;
DROP TABLE IF EXISTS Part;
DROP TABLE IF EXISTS StructureKinematicName;
DROP TABLE IF EXISTS Dof;

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

-- Create tables in correct order

CREATE TABLE Dof (
    dofId INT PRIMARY KEY,
    nameNeg VARCHAR(255),
    dofDirection VARCHAR(255),
    namePos VARCHAR(255),
    dofName VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Exo (
    exoId INT PRIMARY KEY,
    exoDescription VARCHAR(255),
    exoMaterial VARCHAR(255),
    exoOneTwoSided VARCHAR(255),
    exoActivePassive VARCHAR(255),
    exoName VARCHAR(255),
    exoManufacturer VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE ExoProperty (
    exoPropertyId INT PRIMARY KEY,
    exoPropertyName VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Part (
    partId INT PRIMARY KEY,
    partName VARCHAR(255),
    partType VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE StructureKinematicName (
    sknId INT PRIMARY KEY,
    sknName VARCHAR(255),
    sknNameEn VARCHAR(255),
    sknIsSelectable VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Intermediate tables with surrogate IDs

CREATE TABLE HAS_PROPERTY (
    id INT PRIMARY KEY AUTO_INCREMENT,
    exoId INT,
    exoPropertyId INT,
    exoPropertyValue VARCHAR(255),
    FOREIGN KEY (exoId) REFERENCES Exo(exoId),
    FOREIGN KEY (exoPropertyId) REFERENCES ExoProperty(exoPropertyId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE HAS_AIM (
    id INT PRIMARY KEY AUTO_INCREMENT,
    exoId INT,
    sknId INT,
    sknCategory VARCHAR(255),
    structureKinematicNameCategory VARCHAR(255),
    FOREIGN KEY (exoId) REFERENCES Exo(exoId),
    FOREIGN KEY (sknId) REFERENCES StructureKinematicName(sknId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE GIVES_POSTURAL_SUPPORT_IN (
    id INT PRIMARY KEY AUTO_INCREMENT,
    exoId INT,
    dofId INT,
    aim VARCHAR(255),
    adjustable VARCHAR(255),
    mechanism VARCHAR(255),
    `direction` INT,
    FOREIGN KEY (exoId) REFERENCES Exo(exoId),
    FOREIGN KEY (dofId) REFERENCES Dof(dofId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE TRANSFERS_FORCES_FROM (
    id INT PRIMARY KEY AUTO_INCREMENT,
    exoId INT,
    partId INT,
    FOREIGN KEY (exoId) REFERENCES Exo(exoId),
    FOREIGN KEY (partId) REFERENCES Part(partId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE TRANSFERS_FORCES_TO (
    id INT PRIMARY KEY AUTO_INCREMENT,
    exoId INT,
    partId INT,
    FOREIGN KEY (exoId) REFERENCES Exo(exoId),
    FOREIGN KEY (partId) REFERENCES Part(partId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
