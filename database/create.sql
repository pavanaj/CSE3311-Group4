-- Create Tables & Constraints
    
DROP TABLE IF EXISTS Checkout;
DROP TABLE IF EXISTS Accounts;
DROP TABLE IF EXISTS Assets;
DROP TABLE IF EXISTS Custodians;

CREATE TABLE Custodians (
    EmpID CHAR(10) NOT NULL,
    CustName VARCHAR(20) NOT NULL,
    Email VARCHAR(50) NOT NULL,
    CustBldg VARCHAR(10),
    CustRoom VARCHAR(10),
    PRIMARY KEY (EmpID)
);

CREATE TABLE Assets (
    TagNo CHAR(6) NOT NULL,
    SerialNo VARCHAR(20),
    Description VARCHAR(100),
    Type VARCHAR(20),
    CustodianID CHAR(10),
    AquisitionDate DATE,
    AssBldg VARCHAR(10),
    AssRoom VARCHAR(10),
    Status VARCHAR(40),
    PRIMARY KEY (TagNo),
    FOREIGN KEY (CustodianID)
        REFERENCES Custodians (EmpID)
        ON UPDATE CASCADE
);

CREATE TABLE Checkout (
    TagNo CHAR(6) NOT NULL,
    UTAID CHAR(10) NOT NULL,
    Name VARCHAR(20) NOT NULL,
    Email VARCHAR(30),
    CheckOut DATE,
    ReturnDate DATE,
    CheckIn DATE,
    PRIMARY KEY (UTAID),
    FOREIGN KEY (TagNo)
        REFERENCES Assets (TagNo)
        ON UPDATE CASCADE
);

CREATE TABLE Accounts (
    TagNo CHAR(6) NOT NULL,
    Cost DOUBLE,
    SoureOfFunds CHAR(30),
    ReportNo VARCHAR(30),
    ReportDate DATE,
    PRIMARY KEY (TagNo),
    FOREIGN KEY (TagNo)
        REFERENCES Assets (TagNo)
        ON UPDATE CASCADE
);
