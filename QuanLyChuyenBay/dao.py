import json
import math
import re
import uuid

import requests
from flask import request
from flask_sqlalchemy.session import Session
from QuanLyChuyenBay.models import MayBay, ChuyenBay, LichChuyenBay, SanBay, User, Ticket, UserRole, TicketDetail, \
    Customer, san_bay_trung_gian
from QuanLyChuyenBay import db
import datetime
from flask_login import current_user
import hashlib
from sqlalchemy import func
from sqlalchemy.sql import extract
from datetime import datetime
import hmac


def load_san_bay():
    return SanBay.query.all()


def load_may_bay():
    return MayBay.query.all()


def load_chuyen_bay():
    return ChuyenBay.query.all()


def load_lich_may_bay(Tu=None, Den=None, Ngay=None):
    query = LichChuyenBay.query
    sb = load_san_bay()
    cb = load_chuyen_bay()
    list_di = []
    list_den = []
    if Tu:
        for sanbay in sb:
            if Tu.lower() in sanbay.dia_diem.lower():
                for C in cb:
                    if sanbay.id == C.san_bay_di_id:
                        list_di.append(C.id)
        query = query.filter(LichChuyenBay.chuyen_bay_id.in_(list_di))
    if Den:
        for sanbay in sb:
            if Den.lower() in sanbay.dia_diem.lower():
                for C in cb:
                    if sanbay.id == C.san_bay_den_id:
                        list_den.append(C.id)
        query = query.filter(LichChuyenBay.chuyen_bay_id.in_(list_den))
        # query = query.filter(SanBay.dia_diem.contains(Den))
    if Ngay:
        query = query.filter(LichChuyenBay.ngay_gio == Ngay)
    return query.all()


def load_ve():
    return Ticket.query.all()


def load_sbtg(id_lich_chuyen_bay):
    query = san_bay_trung_gian.select().where(
        san_bay_trung_gian.c.lich_chuyen_bay_id == id_lich_chuyen_bay
    )
    result = db.engine.execute(query)
    return result


def load_user_role():
    return UserRole.query.all()


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def register(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, username=username.strip(), password=password, avatar=avatar)
    db.session.add(u)
    db.session.commit()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_chuyen_bay_by_id(chuyen_bay_id):
    return ChuyenBay.query.get(chuyen_bay_id)


def get_san_bay_by_id(san_bay_id):
    return SanBay.query.get(san_bay_id)


def get_may_bay_by_id(may_bay_id):
    return MayBay.query.get(may_bay_id)


def chi_tiet_chuyen_bay(lich_chuyen_bay_id):
    return LichChuyenBay.query.get(lich_chuyen_bay_id)


def checkIfDuplicates(listOfElems):
    setOfElems = set()
    for elem in listOfElems:
        if elem in setOfElems:
            return True
        else:
            setOfElems.add(elem)
    return False


def save_ticket_now(sove, id_chuyen_bay):
    hangve = []
    sex = []
    name = []
    address = []
    phone = []
    email = []
    CMND = []
    l = chi_tiet_chuyen_bay(lich_chuyen_bay_id=id_chuyen_bay)
    for i in range(sove):
        hangve.append(request.form['hangve' + str(i)])
        sex.append(request.form['sex' + str(i)])
        name.append(request.form['name' + str(i)])
        phone.append(request.form['phone_num' + str(i)])
        address.append(request.form['address' + str(i)])
        email.append(request.form['email' + str(i)])
        CMND.append(request.form['CMND' + str(i)])
    for i in range(sove):
        cus = Customer(name=name[i], sex=sex[i], phone=phone[i], address=address[i], email=email[i], CMND=CMND[i])
        db.session.add(cus)
        t = Ticket(userid=current_user, hang_ve=hangve[i], customerid=cus, so_ghe=i)
        db.session.add(t)
        if hangve[i] == '2':
            d = TicketDetail(price=(l.price * 4), lich_chuyen_bay_id=int(l.id), Ticket=t)
        else:
            d = TicketDetail(price=l.price, lich_chuyen_bay_id=int(l.id), Ticket=t)
        db.session.add(d)
    try:
        db.session.commit()
    except:
        return False
    else:
        return True


def save_ticket(cart, sove):
    if cart:
        hangve = []
        sex = []
        name = []
        address = []
        phone = []
        email = []
        CMND = []
        ticket = []
        dem = 0
        for i in range(sove):
            hangve.append(request.form['hangve' + str(i)])
            sex.append(request.form['sex' + str(i)])
            name.append(request.form['name' + str(i)])
            phone.append(request.form['phone_num' + str(i)])
            address.append(request.form['address' + str(i)])
            email.append(request.form['email' + str(i)])
            CMND.append(request.form['CMND' + str(i)])
        for i in range(sove):
            cus = Customer(name=name[i], sex=sex[i], phone=phone[i], address=address[i], email=email[i], CMND=CMND[i])
            db.session.add(cus)
            t = Ticket(userid=current_user, hang_ve=hangve[i], customerid=cus, so_ghe=i)
            ticket.append(t)
            db.session.add(t)
        for c in cart.values():
            for i in range(c['quantity']):
                if hangve[dem] == '2':
                    d = TicketDetail(price=(c['price'] * 4), lich_chuyen_bay_id=int(c['id']), Ticket=ticket[dem])
                else:
                    d = TicketDetail(price=c['price'], lich_chuyen_bay_id=int(c['id']), Ticket=ticket[dem])
                dem = dem + 1
                db.session.add(d)
        try:
            db.session.commit()
        except Exception as e:
            return e
        else:
            return True


def count_flight_by_flightSchedule():
    return db.session.query(ChuyenBay.id, ChuyenBay.ten_chuyen_bay, func.count(LichChuyenBay.id)) \
        .join(LichChuyenBay, LichChuyenBay.chuyen_bay_id.__eq__(ChuyenBay.id), isouter=True) \
        .group_by(ChuyenBay.id).all()


def stats_revenue(kw=None, month=None):
    query = db.session.query(LichChuyenBay.id, LichChuyenBay.chuyen_bay_id, func.sum(TicketDetail.price),
                             func.count(TicketDetail.lich_chuyen_bay_id)) \
        .join(TicketDetail, TicketDetail.lich_chuyen_bay_id.__eq__(LichChuyenBay.id), isouter=True)
    if kw:
        c = db.session.query(ChuyenBay.id).filter(ChuyenBay.ten_chuyen_bay.contains(kw))
        query = query.filter(LichChuyenBay.chuyen_bay_id.in_(c))

    if month:
        query = query.filter(extract('month', TicketDetail.created_day) == month)

    return query.group_by(LichChuyenBay.id).order_by(LichChuyenBay.id).all()


def flight_month_stats(year):
    return db.session.query(extract('month', TicketDetail.created_day), func.sum(TicketDetail.price)) \
        .join(LichChuyenBay, LichChuyenBay.id.__eq__(TicketDetail.lich_chuyen_bay_id)) \
        .filter(extract('year', TicketDetail.created_day) == year) \
        .group_by(extract('month', TicketDetail.created_day)).all()


def no_accent_vietnamese(s):
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    return s


def MoMo(amount):
    # endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
    # partnerCode = "MOMO"
    # accessKey = "F8BBA842ECF85"
    # secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
    # orderInfo = "khach hang " + no_accent_vietnamese(current_user.name) + " thanh toan tien ve ngay " + str(datetime.now().day) + "/" + str(
    #     datetime.now().month) + "/" + str(
    #     datetime.now().year)
    # redirectUrl = "http://127.0.0.1:5000/"
    # ipnUrl = "http://127.0.0.1:5000/"
    # amount = amount
    # orderId = str(uuid.uuid4())
    # requestId = str(uuid.uuid4())
    # requestType = "captureWallet"
    # extraData = ""  # pass empty value or Encode base64 JsonString
    # rawSignature = "accessKey=" + accessKey + "&amount=" + amount + "&extraData=" + extraData + "&ipnUrl=" + ipnUrl + "&orderId=" + orderId + "&orderInfo=" + orderInfo + "&partnerCode=" + partnerCode + "&redirectUrl=" + redirectUrl + "&requestId=" + requestId + "&requestType=" + requestType
    # print(rawSignature)
    # h = hmac.new(bytes(secretKey, 'ascii'), bytes(rawSignature, 'ascii'), hashlib.sha256)
    # signature = h.hexdigest()
    # data = {
    #     'partnerCode': partnerCode,
    #     'partnerName': "Test",
    #     'storeId': "MomoTestStore",
    #     'requestId': requestId,
    #     'amount': amount,
    #     'orderId': orderId,
    #     'orderInfo': orderInfo,
    #     'redirectUrl': redirectUrl,
    #     'ipnUrl': ipnUrl,
    #     'lang': "vi",
    #     'extraData': extraData,
    #     'requestType': requestType,
    #     'signature': signature
    # }
    # data = json.dumps(data)
    #
    # clen = len(data)
    # response = requests.post(endpoint, data=data,
    #                          headers={'Content-Type': 'application/json', 'Content-Length': str(clen)})
    # return response.json()['payUrl']
    pass


def gio(gio):
    return str(math.floor(gio)) + 'h' + str(
        round(gio - math.floor(gio), 3) * 60) + 'p'


def ticket_of_user(id=None):
    query = Ticket.query
    if id:
        query = query.filter(Ticket.id_user == id)
    return query.all()


def get_ticket_detail(veid=None):
    return TicketDetail.query.get(veid)


def get_customer(cusId=None):
    return Customer.query.get(cusId)


if __name__ == '__main__':
    from QuanLyChuyenBay import app

    with app.app_context():
        query = ChuyenBay.query
        print(datetime.date(LichChuyenBay.query.get(1).ngay_gio).month)
