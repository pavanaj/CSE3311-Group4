-- Iteration #1 AMA Database Prototype

-- CSE 3311
-- 2/19/2018
-- Prof. Christoph Csallner
-- Team 4:
	-- Pavanaj Biyani
	-- Kevin Williams
	-- Ethan Duff
    
DROP TABLE IF EXISTS Checkout;
DROP TABLE IF EXISTS Accounts;
DROP TABLE IF EXISTS Assets;
DROP TABLE IF EXISTS Custodians;

CREATE TABLE Custodians (
    EmpID CHAR(10) NOT NULL,
    CustName VARCHAR(20) NOT NULL,
    Email VARCHAR(30) NOT NULL,
    Bldg VARCHAR(10),
    Room VARCHAR(10),
    PRIMARY KEY (EmpID)
);

CREATE TABLE Assets (
    TagNo CHAR(6) NOT NULL,
    SerialNo VARCHAR(20) NOT NULL,
    Description VARCHAR(50),
    Category VARCHAR(20),
    CustodianID CHAR(10),
    AquisitionDate DATE,
    Bldg VARCHAR(10),
    Room VARCHAR(10),
    Status VARCHAR(20),
    PRIMARY KEY (TagNo),
    FOREIGN KEY (CustodianID)
        REFERENCES Custodians (EmpID)
        ON UPDATE CASCADE
);

CREATE TABLE Checkout (
    UTAID CHAR(10) NOT NULL,
    Name VARCHAR(20) NOT NULL,
    TagNo CHAR(6) NOT NULL,
    CustodianID CHAR(10),
    Email VARCHAR(30),
    CheckOut DATE,
    CheckIn DATE,
    PRIMARY KEY (UTAID),
    FOREIGN KEY (CustodianID)
        REFERENCES Custodians (EmpID)
        ON UPDATE CASCADE,
    FOREIGN KEY (TagNo)
        REFERENCES Assets (TagNo)
        ON UPDATE CASCADE
);

CREATE TABLE Accounts (
    TagNo CHAR(6) NOT NULL,
    Cost DOUBLE,
    SoureOfFunds CHAR(20),
    ReportNo VARCHAR(20),
    AcquisitionDate DATE,
    PRIMARY KEY (TagNo),
    FOREIGN KEY (TagNo)
        REFERENCES Assets (TagNo)
        ON UPDATE CASCADE
);
