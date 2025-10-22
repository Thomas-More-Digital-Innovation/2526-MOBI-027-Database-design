CREATE DATABASE exoskeletons_test;
USE exoskeletons_test;

-- Create main Exo table
CREATE TABLE Exo (
    exoId INT PRIMARY KEY,
    exoName VARCHAR(255) NOT NULL,
    exoManufacturer VARCHAR(255),
    exoDescription TEXT,
    exoMaterial VARCHAR(100),
    exoOneTwoSided VARCHAR(50),
    exoActivePassive VARCHAR(50),
    INDEX idx_manufacturer (exoManufacturer),
    INDEX idx_material (exoMaterial)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create Aim table
CREATE TABLE Aim (
    aimId INT PRIMARY KEY,
    aimName VARCHAR(255) NOT NULL,
    aimNameEn VARCHAR(255),
    aimDescription TEXT,
    aimIsSelectable CHAR(1),
    INDEX idx_name (aimName)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create StructureKinematicName table
CREATE TABLE StructureKinematicName (
    structureKinematicNameId INT PRIMARY KEY,
    structureKinematicNameName VARCHAR(255) NOT NULL,
    structureKinematicNameNameEn VARCHAR(255),
    structureKinematicNameIsSelectable CHAR(1),
    INDEX idx_name (structureKinematicNameName)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create ExoProperty table
CREATE TABLE ExoProperty (
    exoPropertyId INT AUTO_INCREMENT PRIMARY KEY,
    exoPropertyName VARCHAR(255) NOT NULL UNIQUE,
    INDEX idx_name (exoPropertyName)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create Dof (Degree of Freedom) table
CREATE TABLE Dof (
    dofId INT PRIMARY KEY,
    dofName VARCHAR(255) NOT NULL,
    namePos VARCHAR(255),
    nameNeg VARCHAR(255),
    dofDirection VARCHAR(50),
    INDEX idx_name (dofName)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create HAS_AIM relationship table (for Aim)
CREATE TABLE HAS_AIM (
    id INT AUTO_INCREMENT PRIMARY KEY,
    exoId INT NOT NULL,
    aimId INT NOT NULL,
    aimCategory VARCHAR(100),
    FOREIGN KEY (exoId) REFERENCES Exo(exoId) ON DELETE CASCADE,
    FOREIGN KEY (aimId) REFERENCES Aim(aimId) ON DELETE CASCADE,
    UNIQUE KEY unique_exo_aim (exoId, aimId, aimCategory),
    INDEX idx_exo (exoId),
    INDEX idx_aim (aimId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create HAS_AIM_Structure relationship table (for StructureKinematicName)
CREATE TABLE HAS_AIM_Structure (
    id INT AUTO_INCREMENT PRIMARY KEY,
    exoId INT NOT NULL,
    structureKinematicNameId INT NOT NULL,
    structureKinematicNameCategory VARCHAR(100),
    FOREIGN KEY (exoId) REFERENCES Exo(exoId) ON DELETE CASCADE,
    FOREIGN KEY (structureKinematicNameId) REFERENCES StructureKinematicName(structureKinematicNameId) ON DELETE CASCADE,
    UNIQUE KEY unique_exo_structure (exoId, structureKinematicNameId, structureKinematicNameCategory),
    INDEX idx_exo (exoId),
    INDEX idx_structure (structureKinematicNameId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create HAS_PROPERTY relationship table
CREATE TABLE HAS_PROPERTY (
    id INT AUTO_INCREMENT PRIMARY KEY,
    exoId INT NOT NULL,
    exoPropertyId INT NOT NULL,
    exoPropertyValue VARCHAR(255),
    FOREIGN KEY (exoId) REFERENCES Exo(exoId) ON DELETE CASCADE,
    FOREIGN KEY (exoPropertyId) REFERENCES ExoProperty(exoPropertyId) ON DELETE CASCADE,
    UNIQUE KEY unique_exo_property (exoId, exoPropertyId),
    INDEX idx_exo (exoId),
    INDEX idx_property (exoPropertyId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create ASSISTS_IN relationship table
CREATE TABLE ASSISTS_IN (
    id INT AUTO_INCREMENT PRIMARY KEY,
    exoId INT NOT NULL,
    dofId INT NOT NULL,
    aim VARCHAR(50),
    direction INT,
    rangeAdjustable VARCHAR(50),
    sizeAdjustable VARCHAR(50),
    lowerBoundMinAngle INT,
    lowerBoundMaxAngle INT,
    upperBoundMinAngle INT,
    upperBoundMaxAngle INT,
    FOREIGN KEY (exoId) REFERENCES Exo(exoId) ON DELETE CASCADE,
    FOREIGN KEY (dofId) REFERENCES Dof(dofId) ON DELETE CASCADE,
    UNIQUE KEY unique_exo_dof (exoId, dofId),
    INDEX idx_exo (exoId),
    INDEX idx_dof (dofId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create JointT (Joint Type) table
CREATE TABLE JointT (
    jointTId INT PRIMARY KEY,
    jointTName VARCHAR(255) NOT NULL,
    INDEX idx_name (jointTName)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create HAS_DOF relationship table (JointT to Dof)
CREATE TABLE HAS_DOF (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jointTId INT NOT NULL,
    dofId INT NOT NULL,
    FOREIGN KEY (jointTId) REFERENCES JointT(jointTId) ON DELETE CASCADE,
    FOREIGN KEY (dofId) REFERENCES Dof(dofId) ON DELETE CASCADE,
    UNIQUE KEY unique_joint_dof (jointTId, dofId),
    INDEX idx_joint (jointTId),
    INDEX idx_dof (dofId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create DOESNT_GO_WITH relationship table
CREATE TABLE DOESNT_GO_WITH (
    id INT AUTO_INCREMENT PRIMARY KEY,
    exoId INT NOT NULL,
    structureKinematicNameId INT NOT NULL,
    FOREIGN KEY (exoId) REFERENCES Exo(exoId) ON DELETE CASCADE,
    FOREIGN KEY (structureKinematicNameId) REFERENCES StructureKinematicName(structureKinematicNameId) ON DELETE CASCADE,
    UNIQUE KEY unique_exo_structure (exoId, structureKinematicNameId),
    INDEX idx_exo (exoId),
    INDEX idx_structure (structureKinematicNameId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create HAS_AS_MAIN_DOF relationship table
CREATE TABLE HAS_AS_MAIN_DOF (
    id INT AUTO_INCREMENT PRIMARY KEY,
    exoId INT NOT NULL,
    dofId INT NOT NULL,
    FOREIGN KEY (exoId) REFERENCES Exo(exoId) ON DELETE CASCADE,
    FOREIGN KEY (dofId) REFERENCES Dof(dofId) ON DELETE CASCADE,
    UNIQUE KEY unique_exo_dof (exoId, dofId),
    INDEX idx_exo (exoId),
    INDEX idx_dof (dofId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create GIVES_RESISTANCE_IN relationship table
CREATE TABLE GIVES_RESISTANCE_IN (
    id INT AUTO_INCREMENT PRIMARY KEY,
    exoId INT NOT NULL,
    dofId INT NOT NULL,
    aim VARCHAR(50),
    direction INT,
    rangeAdjustable VARCHAR(50),
    sizeAdjustable VARCHAR(50),
    lowerBoundMinAngle INT,
    lowerBoundMaxAngle INT,
    upperBoundMinAngle INT,
    upperBoundMaxAngle INT,
    FOREIGN KEY (exoId) REFERENCES Exo(exoId) ON DELETE CASCADE,
    FOREIGN KEY (dofId) REFERENCES Dof(dofId) ON DELETE CASCADE,
    UNIQUE KEY unique_exo_dof_resistance (exoId, dofId),
    INDEX idx_exo (exoId),
    INDEX idx_dof (dofId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create AimType table
CREATE TABLE AimType (
    aimTypeId INT AUTO_INCREMENT PRIMARY KEY,
    aimTypeName VARCHAR(255) NOT NULL,
    aimTypeNameEn VARCHAR(255),
    aimTypeIsSelectable CHAR(1),
    UNIQUE KEY unique_aim_type_name (aimTypeName),
    INDEX idx_name (aimTypeName)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create HAS_AIMTYPE relationship table
CREATE TABLE HAS_AIMTYPE (
    id INT AUTO_INCREMENT PRIMARY KEY,
    aimId INT NOT NULL,
    aimTypeId INT NOT NULL,
    FOREIGN KEY (aimId) REFERENCES Aim(aimId) ON DELETE CASCADE,
    FOREIGN KEY (aimTypeId) REFERENCES AimType(aimTypeId) ON DELETE CASCADE,
    UNIQUE KEY unique_aim_aimtype (aimId, aimTypeId),
    INDEX idx_aim (aimId),
    INDEX idx_aimtype (aimTypeId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create Part table
CREATE TABLE Part (
    partId INT PRIMARY KEY,
    partName VARCHAR(255) NOT NULL,
    partType VARCHAR(50),
    INDEX idx_name (partName),
    INDEX idx_type (partType)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create IS_CONNECTED_WITH relationship table (JointT to Part)
CREATE TABLE IS_CONNECTED_WITH (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jointTId INT NOT NULL,
    partId INT NOT NULL,
    FOREIGN KEY (jointTId) REFERENCES JointT(jointTId) ON DELETE CASCADE,
    FOREIGN KEY (partId) REFERENCES Part(partId) ON DELETE CASCADE,
    UNIQUE KEY unique_joint_part (jointTId, partId),
    INDEX idx_joint (jointTId),
    INDEX idx_part (partId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create LIMITS_IN relationship table
CREATE TABLE LIMITS_IN (
    id INT AUTO_INCREMENT PRIMARY KEY,
    exoId INT NOT NULL,
    dofId INT NOT NULL,
    aim VARCHAR(50),
    direction INT,
    adjustable VARCHAR(50),
    minAngle INT,
    maxAngle INT,
    FOREIGN KEY (exoId) REFERENCES Exo(exoId) ON DELETE CASCADE,
    FOREIGN KEY (dofId) REFERENCES Dof(dofId) ON DELETE CASCADE,
    UNIQUE KEY unique_exo_dof_limits (exoId, dofId),
    INDEX idx_exo (exoId),
    INDEX idx_dof (dofId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create StructureKinematicNameType table
CREATE TABLE StructureKinematicNameType (
    structureKinematicNameTypeId INT AUTO_INCREMENT PRIMARY KEY,
    structureKinematicNameTypeName VARCHAR(255) NOT NULL,
    structureKinematicNameTypeNameEn VARCHAR(255),
    structureKinematicNameTypeIsSelectable CHAR(1),
    UNIQUE KEY unique_skn_type_name (structureKinematicNameTypeName),
    INDEX idx_name (structureKinematicNameTypeName)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create HAS_SKNTYPE relationship table
CREATE TABLE HAS_SKNTYPE (
    id INT AUTO_INCREMENT PRIMARY KEY,
    structureKinematicNameId INT NOT NULL,
    structureKinematicNameTypeId INT NOT NULL,
    FOREIGN KEY (structureKinematicNameId) REFERENCES StructureKinematicName(structureKinematicNameId) ON DELETE CASCADE,
    FOREIGN KEY (structureKinematicNameTypeId) REFERENCES StructureKinematicNameType(structureKinematicNameTypeId) ON DELETE CASCADE,
    UNIQUE KEY unique_skn_skntype (structureKinematicNameId, structureKinematicNameTypeId),
    INDEX idx_skn (structureKinematicNameId),
    INDEX idx_skntype (structureKinematicNameTypeId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create TRANSFERS_FORCES_FROM relationship table
CREATE TABLE TRANSFERS_FORCES_FROM (
    id INT AUTO_INCREMENT PRIMARY KEY,
    exoId INT NOT NULL,
    partId INT NOT NULL,
    FOREIGN KEY (exoId) REFERENCES Exo(exoId) ON DELETE CASCADE,
    FOREIGN KEY (partId) REFERENCES Part(partId) ON DELETE CASCADE,
    UNIQUE KEY unique_exo_part_from (exoId, partId),
    INDEX idx_exo (exoId),
    INDEX idx_part (partId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create TRANSFERS_FORCES_TO relationship table
CREATE TABLE TRANSFERS_FORCES_TO (
    id INT AUTO_INCREMENT PRIMARY KEY,
    exoId INT NOT NULL,
    partId INT NOT NULL,
    FOREIGN KEY (exoId) REFERENCES Exo(exoId) ON DELETE CASCADE,
    FOREIGN KEY (partId) REFERENCES Part(partId) ON DELETE CASCADE,
    UNIQUE KEY unique_exo_part_to (exoId, partId),
    INDEX idx_exo (exoId),
    INDEX idx_part (partId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;