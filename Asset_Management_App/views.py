from flask import render_template
from flask import request
from sqlalchemy import create_engine

from Asset_Management_App import app
from Asset_Management_App import db
from Asset_Management_App import models

#ngine = create_engine("mysql://admin:password@localhost/AssetManagement")

@app.route('/')
@app.route('/index.html')
def index():
    return render_template("index.html")

@app.route('/acct.html', methods=['GET','POST'])
def view_accounting():
    return render_template("acct.html")

@app.route('/allcust.html', methods=['GET','POST'])
def custodian_lookup():
    return render_template("allcust.html")

@app.route('/checkin.html', methods=['GET','POST'])
def asset_checkin():
    if request.method == 'POST':
        tagNo = request.form.get("tagno", False)
        serialNo = request.form.get("serialno", False)
        checkIn = request.form.get("date", False)

        db.session.query().filter(models.Checkout.tagNo == tagNo or models.Checkout.serialNo == serialNo).\
        update({"checkin": checkIn})
        db.session.commit
    return render_template("checkin.html")

@app.route('/checkout.html', methods=['GET','POST'])
def asset_checkout():
    if request.method == 'POST':
        tagNo = request.form.get("tagno", False)
        empID = request.form.get("empid", False)
        memName = request.form.get("name", False)
        email = request.form.get("email", False)
        outDate = request.form.get("outdate", False)
        inDate = request.form.get("indate", False)

        newCheckout = models.Checkout(tagNo, empID, memName, email, outDate, inDate, None)
        db.session.add(newCheckout)
        db.session.commit()

    return render_template("checkout.html")

@app.route('/lookup.html', methods=['GET', 'POST'])
def asset_lookup():
    if request.method == 'POST':
        tag = request.form.get("tagno", None)
        serial = request.form.get("serialno", None)
        queryVal = models.Assets.query.filter((models.Assets.tagNo == tag) | (models.Assets.serialNo == serial)).first()
        print(queryVal)

    return render_template("lookup.html")

@app.route('/newasset.html', methods=['GET', 'POST'])
def new_asset():
    if request.method == 'POST':
        tagNo = request.form.get("tagno", False)
        serialNo = request.form.get("serialno", False)
        type = request.form.get("type", False)
        date = request.form.get("date", False)
        description = request.form.get("description", False)
        building = request.form.get("building", False)
        room = request.form.get("room", False)

        empID = request.form.get("empid", False)
        name = request.form.get("name", False)
        buildingCust = request.form.get("buildingCust", False)
        roomCust = request.form.get("roomCust", False)
        email = request.form.get("email", False)

        cost = request.form.get("cost", False)
        funds = request.form.get("funds", False)
        status = request.form.get("status", False)
        reportNum = None

        newAsset = models.Assets(tagNo = tagNo, serialNo = serialNo, description = description, type = type, custID = empID,
        acqDate = date, bldg = building, room = room, status = status)
        newCust = models.Custodian(empID = empID, custName = name, email = email, building = buildingCust, room = roomCust)
        newAccount = models.Accounts(tagNo = tagNo, cost = cost, fundSource = funds, reportNum = reportNum, reportDate = None)

        db.session.add(newAsset)
        db.session.add(newAccount)
        if((email != False) and (name != False) and (buildingCust != False) and (roomCust != False)):
            db.session.add(newCust)
        db.session.commit()

    return render_template("newasset.html")

@app.route('/newcust.html', methods=['GET', 'POST'])
def new_custodian():
    if(request.method == 'POST'):
        custid = request.form['empid']
        name = request.form['name']
        buildingcust = request.form['building']
        roomcust = request.form['room']
        custmail = request.form['email']

        newCust = models.Custodian(custid, name, custmail, buildingcust, roomcust)
        db.session.add(newCust)
        db.session.commit()

    return render_template("newcust.html")

@app.route('/report.html', methods=['GET', 'POST'])
def asset_report():
    return render_template("report.html")

@app.route('/updateacct.html', methods=['GET', 'POST'])
def update_accounting():
    return render_template("updateacct.html")

@app.route('/updateasset.html', methods=['GET', 'POST'])
def update_asset():
    return render_template("updateasset.html")

@app.route('/updatecust.html', methods=['GET', 'POST'])
def update_custodian():
    return render_template("updatecust.html")

@app.route('/viewcheck.html', methods=['GET', 'POST'])
def view_checked_out():
    return render_template("viewcheck.html")

@app.route('/viewcust.html', methods=['GET', 'POST'])
def view_cust_assets():
    return render_template("viewcust.html")

@app.route('/work.html', methods=['GET', 'POST'])
def maintenance_error():
    return render_template("work.html")

