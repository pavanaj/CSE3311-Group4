from flask import render_template, request, redirect
import csv
from Asset_Management_App import app, db, models

#Routes for base page of web app
@app.route('/')
@app.route('/index.html')
def index():
    return render_template("index.html") #Template to use for base page

#Route for page to view accounting information
@app.route('/acct.html', methods=['GET','POST'])
def view_accounting():
    if request.method == 'POST':
        if request.form['Action'] == "View":
            tagNo = request.form.get('tagno', None)
            serial = request.form.get('serialno', None)
            cur = db.engine.execute("select Assets.TagNo, SerialNo, Type, Description, SoureOfFunds, ReportNo, Status,"
                                    " Cost, CustodianID from Assets JOIN Accounts ON Assets.TagNo=Accounts.TagNo"
                                    " WHERE Assets.TagNo = \"" + tagNo + '\" OR SerialNo = \"' + serial + '\"')
            entries = cur.fetchall()
            return render_template("acct.html", entries=entries)

        if request.form['Action'] == "View All":
            cur = db.engine.execute('select Assets.TagNo, SerialNo, Type, Description, SoureOfFunds, ReportNo, Status,'
                                    ' Cost, CustodianID from Assets JOIN Accounts ON Assets.TagNo=Accounts.TagNo')
            entries = cur.fetchall()
            return render_template("acct.html", entries=entries)
        if request.form['Action'] == "Excel":
            cur = db.engine.execute('select * from Accounts')
            entries = cur.fetchall()
            with open('Accounts.csv', 'w') as out:
                printFile = csv.writer(out)
                printFile.writerow(['Tag No', 'Cost', 'Fund Source', 'Report Number', 'Report Date'])
                for entry in entries:
                    printFile.writerow(entry)
            return render_template("acct.html")
    return render_template("acct.html") #Template to use for viewing account information

#Route for page for custodian lookup
@app.route('/allcust.html', methods=['GET','POST'])
def custodian_lookup():
    if request.method == 'POST':
        if request.form['Action'] == "Look Up":
            custID = request.form.get('empid', None)
            custName = request.form.get('name', None)
            cur = db.engine.execute('select * from Custodians where EmpID = ' +custID+ ' OR CustName = "'+custName+'"')
            entries = cur.fetchall()
            return render_template('allcust.html', entries=entries)

        if request.form['Action'] == "View All":
            cur = db.engine.execute('select * from Custodians')
            entries = cur.fetchall()
            return render_template('allcust.html', entries=entries)

        if request.form['Action'] == "Excel":
            cur = db.engine.execute('select * from Custodians')
            entries = cur.fetchall()
            with open('Custodians.csv', 'w') as out:
                printFile = csv.writer(out)
                printFile.writerow(['Custodian ID', 'Name', 'Email', 'Building', 'Room'])
                for entry in entries:
                    printFile.writerow(entry)
            return render_template("allcust.html")
    return render_template("allcust.html") #Template for use viewing custodian information

#Route for page for checking in a checked out asset
@app.route('/checkin.html', methods=['GET','POST'])
def asset_checkin():
    if request.method == 'POST':                    #Checks for method from template
        tagNo = request.form.get("tagno", False)    #Gets tag number for asset if exists
        serialNo = request.form.get("serialno", False)  #Gets serial number for asset if exists
        checkIn = request.form.get("date", False)       #Gets check in date from form

        new = models.Checkout.query.filter((models.Checkout.tagNo == tagNo) | (models.Checkout.serNo == serialNo)).\
        first() #Find tuple with tag number of serial number of asset being checked in and updates
        new.checkin = checkIn
        db.session.commit()            #Commit transaction to database
    return render_template("checkin.html")  #Template for checking in an asset

#Route for page to check out an asset
@app.route('/checkout.html', methods=['GET','POST'])
def asset_checkout():
    if request.method == 'POST':    #Checks for method from template
        tagNo = request.form.get("tagno", False)    #Gets tag number for asset if it exists
        empID = request.form.get("empid", False)    #Gets UTAID for person checking out asset
        memName = request.form.get("name", False)   #Gets name of person checking out asset
        email = request.form.get("email", False)    #Gets email of person checking out asset
        outDate = request.form.get("outdate", False)    #Gets checkout date for asset
        inDate = request.form.get("indate", False)      #Gets checkin date for asset

        newCheckout = models.Checkout(tagNo, empID, memName, email, outDate, inDate, None) #Creates new checkout tuple
        db.session.add(newCheckout)     #Adds new tuple to database
        db.session.commit()             #Commits changes to database

    return render_template("checkout.html") #Template for checking out an asset

#Route for asset lookup page
@app.route('/lookup.html', methods=['GET', 'POST'])
def asset_lookup():
    if request.method == 'POST':                #Checks for method from template
        if request.form['Action'] == "Look Up":
            tag = request.form.get("tagno", None)   #Gets tag number for asset to lookup
            serial = request.form.get("serialno", None) #Gets serial number for asset to lookup
            cur = db.engine.execute('select TagNo, SerialNo, Type, Description, AssBldg, AssRoom, CustodianID, CustName'
                                    ' from Assets JOIN Custodians ON CustodianID = EmpID'
                                    ' where TagNo = "' + tag + '" OR SerialNo = "' + serial + '" ')
            entries = cur.fetchall()
            return render_template('lookup.html', entries=entries)
        if request.form['Action'] == "View All":
            cur = db.engine.execute('select TagNo, SerialNo, Type, Description, AssBldg, AssRoom, CustodianID, CustName'
                                    ' from Assets JOIN Custodians ON CustodianID = EmpID')
            entries = cur.fetchall()
            return render_template('lookup.html', entries=entries)
        if request.form['Action'] == "Excel":
            cur = db.engine.execute('select * from Assets')
            entries = cur.fetchall()
            with open('Assets.csv', 'w') as out:
                printFile = csv.writer(out)
                printFile.writerow(['Tag No.', 'Serial No', 'Description', 'Type', 'Custodian ID', 'Acquisition Date','Building', 'Room', 'Status'])
                for entry in entries:
                    printFile.writerow(entry)
            return render_template("lookup.html")
    return render_template("lookup.html")   #Returning to template with input

#Route for new asset page
@app.route('/newasset.html', methods=['GET', 'POST'])
def new_asset():
    if request.method == 'POST': #Checks for method from template
        tagNo = request.form.get("tagno", False)    #Gets tag number for new asset
        serialNo = request.form.get("serialno", False)  #Gets serial number for new asset
        type = request.form.get("type", False)          #Gets asset type for new asset
        date = request.form.get("date", False)          #Gets acquisition date for new asset
        description = request.form.get("description", False)    #Gets description of new asset
        building = request.form.get("building", False)          #Gets building for new asset
        room = request.form.get("room", False)                  #Gets room for new asset

        empID = request.form.get("empid", False)                #Gets ID for new custodian using new asset
        name = request.form.get("name", False)                  #Gets name for new custodian using new asset
        buildingCust = request.form.get("buildingCust", False)  #Gets building name for new custodian using new asset
        roomCust = request.form.get("roomCust", False)  #Gets room number for new custodian using new asset
        email = request.form.get("email", False)        #Gets email for new custodian using new asset

        cost = request.form.get("cost", False)          #Gets cost for new accounting entry for new asset
        funds = request.form.get("funds", False)        #Gets funds for new accounting entry for new asset
        status = request.form.get("status", False)      #Gets status for new accounting entry for new asset
        reportNum = None                                #Sets report value to null, by default no police reports

        #Creates object for new asset
        newAsset = models.Assets(tagNo = tagNo, serialNo = serialNo, description = description, type = type, custID = empID,
        acqDate = date, bldg = building, room = room, status = status)
        #Creates object for new custodian
        newCust = models.Custodian(empID = empID, custName = name, email = email, building = buildingCust, room = roomCust)
        #Creates object for new accounting entry
        newAccount = models.Accounts(tagNo = tagNo, cost = cost, fundSource = funds, reportNum = reportNum, reportDate = None)


        db.session.add(newAsset)    #Add new asset
        db.session.add(newAccount)  #Add new accounting entry
        if((email != False) and (name != False) and (buildingCust != False) and (roomCust != False)):
            db.session.add(newCust) #Add new custodian if user did not leave any necessary fields blank
        db.session.commit()         #Commit new transactions

    return render_template("newasset.html")     #Template for new asset creation

#Route for new custodian creation
@app.route('/newcust.html', methods=['GET', 'POST'])
def new_custodian():
    if(request.method == 'POST'):   #Checks form for method
        custid = request.form['empid']  #Gets ID for new custodian
        name = request.form['name']     #Gets name for new custodian
        buildingcust = request.form['building'] #Gets building for new custodian
        roomcust = request.form['room']         #Gets room number for new custodian
        custmail = request.form['email']        #Gets email for new custodian

        newCust = models.Custodian(custid, name, custmail, buildingcust, roomcust)  #Creates object for new custodian
        db.session.add(newCust) #Adds new custodian to database
        db.session.commit()     #Commit changes

    return render_template("newcust.html")  #Template for new custodian creation

@app.route('/oldasset.html', methods=['GET', 'POST'])
def old_asset():
    if request.method == 'POST':
        tagNo = request.form.get('tagno', None)
        serialNo = request.form.get('serialno', None)
        type = request.form.get('type', None)
        date = request.form.get('date', None)
        description = request.form.get('description', None)
        build = request.form.get('building', None)
        room = request.form.get('room', None)
        custID = request.form.get('empid', None)

        cost = request.form.get('cost', None)
        funds = request.form.get('funds', None)
        status = request.form.get('status', None)
        reportNum = None
        reportDate = None

        newAsset = models.Assets(tagNo=tagNo,  serialNo=serialNo, description=description, type=type,
                                 custID=custID, acqDate=date, bldg=build, room=room, status=status)
        newAccount = models.Accounts(tagNo=tagNo,cost=cost,fundSource=funds, reportNum=reportNum, reportDate=reportDate)
        db.session.add(newAsset)
        db.session.add(newAccount)
        db.session.commit()

        return render_template("oldasset.html")
    return render_template("oldasset.html")
#Route for police report recording
@app.route('/report.html', methods=['GET', 'POST'])
def asset_report():
    if request.method == 'POST':
        tagNo = request.form.get('tagno', None)
        serialNo = request.form.get('serialno')
        status = request.form.get('type')
        repNo = request.form.get('report')
        repDate = request.form.get('date')

        editAccount = models.Accounts.query.filter(models.Accounts.tagNo == tagNo)
        editAsset = models.Assets.query.filter((models.Assets.tagNo == tagNo) | (models.Assets.serialNo == serialNo))
        editAsset.status = status
        editAccount.reportNum = repNo
        editAccount.reportDate = repDate

        db.session.commit()
    return render_template("report.html")   #Template for filing new report

#Route for updating accounting info
@app.route('/updateacct.html', methods=['GET', 'POST'])
def update_accounting():
    if request.method == 'POST':
        if request.form['Action'] == "Update":
            oldTag = request.form.get('oldtagno', None)

            updatedAcct = models.Accounts.query.filter((models.Accounts.tagNo == oldTag)).first()
            upStat = models.Assets.query.filter((models.Assets.tagNo == oldTag)).first()
            result = {'tag':updatedAcct.tagNo, 'cost': updatedAcct.cost, 'funds': updatedAcct.fundSource,
                      'stat':upStat.status
            }

            return render_template("updateacct.html", **result)
        if request.form['Action'] == "Submit":
            tag = request.form.get('newtag', None)
            cost = request.form.get('cost', None)
            funds = request.form.get('funds', None)
            stats = request.form.get('status', None)

            newAsset = models.Assets.query.filter((models.Assets.tagNo==tag))
            newAccount = models.Accounts.query.filter((models.Accounts.tagNo == tag))
            newAccount.cost = cost
            newAccount.fundSource = funds
            newAsset.status = stats

            db.session.commit()

            return redirect("updateacct.html")
        if request.form['Action'] == "Clear":
            return redirect("updateacct.html")
    return render_template("updateacct.html")   #Template for updating accounting info

#Route for updating asset info
@app.route('/updateasset.html', methods=['GET', 'POST'])
def update_asset():
    if request.method == 'POST':
        if request.form['Action'] == "Update":
            oldTag = request.form.get('oldtagno', None)
            oldSer = request.form.get('oldserialno', None)

            updatedAsset = models.Assets.query.filter((models.Assets.tagNo == oldTag) |
                       (models.Assets.serialNo == oldSer)).first()
            result = {'tag': updatedAsset.tagNo, 'serial': updatedAsset.serialNo, 'desc': updatedAsset.description,
                    'type': updatedAsset.type, 'cust': updatedAsset.custID, 'acq': updatedAsset.acqDate,
                    'build': updatedAsset.bldg, 'room': updatedAsset.room
            }
            print(updatedAsset.acqDate)
            if(result['acq'] is None):
                result['acq'] = "0000-00-00"
            return render_template("updateasset.html", **result)
        if request.form['Action'] == "Submit":
            tag = request.form.get('newtag', None)
            ser = request.form.get('newserialno', None)
            cat = request.form.get('type', None)
            acqDate = request.form.get('date', None)
            desc = request.form.get('description', None)
            build = request.form.get('building', None)
            room = request.form.get('room', None)
            id = request.form.get('empid', None)
            print(acqDate)

            new = models.Assets.query.filter((models.Assets.tagNo == tag)).first()
            new.serialNo = ser
            new.type = cat
            new.acqDate  = acqDate
            new.description = desc
            new.bldg = build
            new.room = room
            new.custID = id

            db.session.commit()

            return render_template("updateasset.html")
        if request.form['Action'] == "Clear":
            return redirect("updateasset.html")

    return render_template("updateasset.html")  #Template for updating asset info

#Route for updating custodian info
@app.route('/updatecust.html', methods=['GET', 'POST'])
def update_custodian():
    if request.method == 'POST':
        if request.form['Action'] == "Update":
            oldID = request.form.get('oldempid', None)
            oldName = request.form.get('oldname', None)

            updatedCust = models.Custodian.query.filter((models.Custodian.empID == oldID) | (models.Custodian.\
            empID == oldName)).first()

            result = {'id': updatedCust.empID, 'name': updatedCust.custName, 'email':updatedCust.email,
                      'build':updatedCust.building, 'room': updatedCust.room
            }
            return render_template("updatecust.html", **result)
        if request.form['Action'] == "Submit":
            id = request.form.get('newid', None)
            name = request.form.get('newname', None)
            build = request.form.get('building', None)
            room = request.form.get('room', None)
            email = request.form.get('email', None)

            new = models.Custodian.query.filter((models.Custodian.empID == id) ).first()

            new.empID = id
            new.custName = name
            new.email = email
            new.building = build
            new.room = room

            db.session.commit()

            return render_template("updatecust.html")
        if request.form['Action'] == "Clear":
            return redirect("updatecust.html")
    return render_template("updatecust.html")   #Template for updating custodian info

#Route for viewing checkout information
@app.route('/viewcheck.html', methods=['GET', 'POST'])
def view_checked_out():
    if request.method == 'POST':
        if request.form['Action'] == "View":
            tag = request.form.get('tagno')
            serial = request.form.get('serialno')

            cur = db.engine.execute('select Assets.TagNo, Assets.SerialNo, CustodianID, CustName, UTAID, Name, CheckOut, ReturnDate'
                                    ' from Assets JOIN Custodians ON CustodianID=EmpID '
                                    ' JOIN Checkout ON Assets.TagNo=Checkout.TagNo'
                                    ' WHERE Assets.TagNo = "'+ tag + '" OR Assets.SerialNo = "'+serial+'"')
            entries = cur.fetchall()
            return render_template('viewcheck.html', entries=entries)

        if request.form['Action'] == "View All":
            cur = db.engine.execute('select Assets.TagNo, Assets.SerialNo, CustodianID, CustName, UTAID, Name, CheckOut, ReturnDate'
                                    ' from Assets JOIN Custodians ON CustodianID=EmpID '
                                    ' JOIN Checkout ON Assets.TagNo=Checkout.TagNo')
            entries = cur.fetchall()
            return render_template('viewcheck.html', entries=entries)
        if request.form['Action'] == "Excel":
            cur = db.engine.execute('select * from Checkout')
            entries = cur.fetchall()
            with open('Checkout.csv', 'w') as out:
                printFile = csv.writer(out)
                printFile.writerow(['Tag No', 'Serial No', 'UTA ID', 'Name', 'Email', 'Checkout Date',
                                          'Return Date', 'Checkin Date'])
                for entry in entries:
                    printFile.writerow(entry)
            return render_template("viewcheck.html")
    return render_template("viewcheck.html")   #Template for viewing checkout information

#Route for viewing custodian info
@app.route('/viewcust.html', methods=['GET', 'POST'])
def view_cust_assets():
    if(request.method == 'POST'):
        custID = request.form.get('empid', None)
        custName = request.form.get('name', None)
        cur = db.engine.execute('select TagNo, SerialNo, Type, Description, AssBldg, AssRoom from Assets '
                                'where CustodianID = ' + custID)
        entries = cur.fetchall()
        return render_template('viewcust.html', entries=entries)
    return render_template("viewcust.html")    #Template for viewing custodian info

#Route for WIP page
@app.route('/work.html', methods=['GET', 'POST'])
def maintenance_error():
    return render_template("work.html")    #Template for WIP page

