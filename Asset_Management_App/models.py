from Asset_Management_App import db

class  Custodian(db.Model):
    __tablename__='Custodians'
    empID = db.Column("EmpID", db.String(10), unique=False, nullable=False, primary_key=True)
    custName = db.Column("CustName", db.String(20), unique=False, nullable=False)
    email = db.Column("Email", db.String(50), unique=False, nullable=False)
    building = db.Column("CustBldg", db.String(10), unique=False,  nullable=True)
    room = db.Column("CustRoom", db.String(10), unique=False, nullable=True)

    def __repr__(self):
        return 'Employee: %s' % self.empID

    def __init__(self, empID, custName, email, building, room):
        self.empID = empID
        self.custName = custName
        self.email = email
        self.building = building
        self.room = room

class Assets(db.Model):
    __tablename__='Assets'
    tagNo = db.Column("TagNo", db.String(6), unique=False, nullable=False, primary_key=True)
    serialNo = db.Column("SerialNo", db.String(20), unique=False, nullable=True)
    description = db.Column("Description", db.String(100), unique=False, nullable=True)
    type = db.Column("Type", db.String(20), unique=False, nullable=True)
    custID = db.Column("CustodianID", db.String(10), unique=False, nullable=True)
    acqDate = db.Column("AquisitionDate", db.Date, unique=False, nullable=True)
    bldg = db.Column("AssBldg", db.String(10), unique=False, nullable=True)
    room = db.Column("AssRoom", db.String(10), unique=False, nullable=True)
    status = db.Column("Status", db.String(40), unique=False, nullable=True)

    #custodian = db.relationship('Custodians', foreign_keys='custID')
    def __repr__(self):
        return 'Asset: %s' % self.tagNo
    def __init__(self, tagNo, serialNo, description, type, custID, acqDate, bldg, room, status):
        self.tagNo = tagNo
        self.serialNo = serialNo
        self.description = description
        self.type = type
        self.custID = custID
        self.acqDate = acqDate
        self.bldg = bldg
        self.room = room
        self.status = status

class Checkout(db.Model):
        __tablename__='Checkout'
        tagNo = db.Column("TagNo",  db.String(6), unique=False, nullable=False)
        serNo = db.Column("SerNo", db.String(20), unique=False, nullable=True)
        UTAID = db.Column("UTAID", db.String(10), unique=False, nullable=False, primary_key=True)
        name = db.Column("Name", db.String(20), unique=False, nullable=True)
        email = db.Column("Email", db.String(30), unique=False, nullable=True)
        checkout = db.Column("CheckOut", db.Date, unique=False, nullable=True)
        returnDate = db.Column("ReturnDate", db.Date, unique=False, nullable=True)
        checkin = db.Column("CheckIn", db.Date, unique=False, nullable=True)

        #asset = db.relationship('Assets', foreign_keys='TagNo')
        def __repr__(self):
            return 'Checkout: %s' % self.UTAID

        def __init__(self, tagNo, serNo, UTAID, name, email, checkout, returnDate, checkin):
            self.tagNo = tagNo
            self.serNo = serNo
            self.UTAID = UTAID
            self.name = name
            self.email = email
            self.checkout = checkout
            self.returnDate = returnDate
            self.checkin = checkin

class Accounts(db.Model):
    __tablename__='Accounts'
    tagNo = db.Column("TagNo", db.String(6), unique=False, nullable=False, primary_key=True)
    cost = db.Column("Cost", db.FLOAT, unique=False, nullable=True)
    fundSource = db.Column("SoureOfFunds", db.String(30), unique=False, nullable=True)
    reportNum = db.Column("ReportNo", db.String(30), unique=False, nullable=True)
    reportDate = db.Column("ReportDate", db.Date, unique=False, nullable=True)

    #asset = db.relationship('Assets', foreign_keys='TagNo')
    def __repr__(self):
        return 'Accounts: %s' % self.tagNo

    def __init__(self, tagNo, cost, fundSource, reportNum, reportDate):
        self.tagNo = tagNo
        self.cost = cost
        self.fundSource = fundSource
        self.reportNum = reportNum
        self.reportDate = reportDate

