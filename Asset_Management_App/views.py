from flask import render_template, request

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
        tagNo = request.form.get('tagno', None)
        serial = request.form.get('serialno', None)
        queryVal = models.Accounts.query.filter((models.Accounts.tagNo == tagNo)).first()
        queryVal2 = models.Assets.query.filter((models.Assets.tagNo == tagNo) | (models.Assets.serialNo == serial)). \
            first()
        result = {'tag': queryVal.tagNo, 'cost': queryVal.cost, 'serialNo': queryVal2.serialNo, 'cat': queryVal2.type,
                  'desc': queryVal2.description, 'build': queryVal2.bldg, 'room': queryVal2.room,
                  'stat': queryVal2.status, 'cust': queryVal2.custID
        }
        return render_template("acct.html", **result)
    return render_template("acct.html") #Template to use for viewing account information

#Route for page for custodian lookup
@app.route('/allcust.html', methods=['GET','POST'])
def custodian_lookup():
    if request.method == 'POST':
        if request.form.post['Action']:
            custID = request.form.get('empid', None)
            custName = request.form.get('name', None)
            queryVal = models.Custodian.query.filter((models.Custodian.empID == custID) | (models.Custodian.custName ==
            custName)).first()
            result = {'empID': queryVal.empID, 'name': queryVal.custName, 'email': queryVal.email,
                    'build': queryVal.building, 'room': queryVal.room
            }
        return render_template("allcust.html", **result)
    return render_template("allcust.html") #Template for use viewing custodian information

#Route for page for checking in a checked out asset
@app.route('/checkin.html', methods=['GET','POST'])
def asset_checkin():
    if request.method == 'POST':                    #Checks for method from template
        tagNo = request.form.get("tagno", False)    #Gets tag number for asset if exists
        serialNo = request.form.get("serialno", False)  #Gets serial number for asset if exists
        checkIn = request.form.get("date", False)       #Gets check in date from form

        db.session.query().filter(models.Checkout.tagNo == tagNo or models.Checkout.serialNo == serialNo).\
        update({"checkin": checkIn}) #Find tuple with tag number of serial number of asset being checked in and updates
        db.session.commit            #Commit transaction to database
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
            #Assigns tuple found in query to a variable
            queryVal = models.Assets.query.filter((models.Assets.tagNo == tag) | (models.Assets.serialNo == serial)).\
            first()
            result = {'tag': queryVal.tagNo, 'serial': queryVal.serialNo, 'cat': queryVal.type, 'desc': queryVal.description,
                    'cust': queryVal.custID, 'acq': queryVal.acqDate, 'build': queryVal.bldg, 'room': queryVal.room,
                    'stat': queryVal.status
            }   #Creating structure to pass back to html form
            return render_template("lookup.html", **result)
        #if request.form['Action'] == "View All":


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

#Route for police report recording
@app.route('/report.html', methods=['GET', 'POST'])
def asset_report():
    return render_template("report.html")   #Template for filing new report

#Route for updating accounting info
@app.route('/updateacct.html', methods=['GET', 'POST'])
def update_accounting():
    return render_template("updateacct.html")   #Template for updating accounting info

#Route for updating asset info
@app.route('/updateasset.html', methods=['GET', 'POST'])
def update_asset():
    return render_template("updateasset.html")  #Template for updating asset info

#Route for updating custodian info
@app.route('/updatecust.html', methods=['GET', 'POST'])
def update_custodian():
    return render_template("updatecust.html")   #Template for updating custodian info

#Route for viewing checkout information
@app.route('/viewcheck.html', methods=['GET', 'POST'])
def view_checked_out():
    return render_template("viewcheck.html")   #Template for viewing checkout information

#Route for viewing custodian info
@app.route('/viewcust.html', methods=['GET', 'POST'])
def view_cust_assets():
    if(request.method == 'POST'):
        custID = request.form.get('empid', None)
        custName = request.form.get('name', None)
    return render_template("viewcust.html")    #Template for viewing custodian info

#Route for WIP page
@app.route('/work.html', methods=['GET', 'POST'])
def maintenance_error():
    return render_template("work.html")    #Template for WIP page

