import hashlib

from QuanLyChuyenBay import db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float, Enum
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from QuanLyChuyenBay import app
from enum import Enum as UserEnum
from enum import Enum as HangVeEnum
from enum import Enum as Sex
from flask_login import UserMixin
import math


class UserRole(UserEnum):
    ADMIN = 1
    STAFF = 2
    USER = 3


class Sex(Sex):
    Nam = 1
    Nu = 2


class LoaiHangVe(HangVeEnum):
    HangVe1 = 1
    HangVe2 = 2


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class MayBay(BaseModel):
    loai_may_bay = Column(String(50), nullable=False)
    TinhTrangRanh = Column(Boolean, default=True)
    so_luong_cho_ngoi = Column(Integer, nullable=False)
    chuyen_bay = relationship('LichChuyenBay', backref='MayBay', lazy=True)

    def __str__(self):
        return self.loai_may_bay


class SanBay(BaseModel):
    ten_san_bay = Column(String(50), nullable=False)
    dia_diem = Column(String(50), nullable=False)
    tinh_trang_con_trong = Column(Boolean, default=True)
    #   lich_chuyen_bay = relationship('LichChuyenBay',backref = 'SanBay',lazy = False)
    ten_san_bay = Column(String(50), nullable=False)
    dia_diem = Column(String(50), nullable=False)
    tinh_trang_con_trong = Column(Boolean, default=True)

    # san_bay_trung_gian = relationship('SanbayTrungGian', backref='san_bay_id', lazy=True)

    # lich_chuyen_bay = relationship('LichChuyenBay',backref = 'SanBay',lazy = False)
    # chuyen_bay = relationship = relationship('ChuyenBay',backref = 'SanBay', lazy = False)
    def __str__(self):
        return self.ten_san_bay


class ChuyenBay(BaseModel):
    ten_chuyen_bay = Column(String(50), nullable=False)
    san_bay_di_id = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    san_bay_den_id = Column(Integer, ForeignKey(SanBay.id), nullable=False)

    san_bay_di = relationship('SanBay', foreign_keys=[san_bay_di_id])
    san_bay_den = relationship('SanBay', foreign_keys=[san_bay_den_id], overlaps="san_bay_di")
    # may_bay = relationship('MayBay', foreign_keys=[may_bay_id],overlaps="MayBay,chuyen_bay")

    trang_thai = Column(Boolean, default=True)
    lich_chuyen_bay = relationship("LichChuyenBay", backref="ChuyenBay", lazy=True)

    def __str__(self):
        return str(self.lich_chuyen_bay)

    def __str__(self):
        return self.ten_chuyen_bay


class LichChuyenBay(BaseModel):
    chuyen_bay_id = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)
    may_bay_id = Column(Integer, ForeignKey(MayBay.id), nullable=False)
    ngay_gio = Column(DateTime, default=datetime.now())
    thoi_gian_bay = Column(Float, nullable=False)
    so_luong_hang_ve_1 = Column(Integer, nullable=False)
    so_luong_hang_ve_2 = Column(Integer, nullable=False)
    image = Column(String(200))
    san_bay_trung_gian = relationship('SanBay', secondary='san_bay_trung_gian', lazy='subquery',
                                      backref=backref('lich_chuyen_bay', lazy=True))
    trang_thai_cho_ngoi = Column(Boolean, default=True)
    price = Column(Float, nullable=False)
    trang_thai_cho_ngoi = Column(Boolean, default=True)
    price = Column(Float, nullable=False)
    ticketdetails = relationship('TicketDetail', backref='lich_chuyen_bay', lazy=True)

    def gio(self):
        return str(math.floor(self.thoi_gian_bay)) + 'h' + str(
            round(self.thoi_gian_bay - math.floor(self.thoi_gian_bay), 3) * 60) + 'p'

    def _int__(self):
        return self.chuyen_bay_id


san_bay_trung_gian = db.Table('san_bay_trung_gian',
                              Column('lich_chuyen_bay_id', Integer, ForeignKey(LichChuyenBay.id), primary_key=True),
                              Column('san_bay', Integer, ForeignKey(SanBay.id), primary_key=True),
                              Column('thoi_gian_dung', Float, nullable=False, default=2),
                              Column('ghi_chu', String(200)))


# class SanbayTrungGian(BaseModel):
#     lich_chuyen_bay = Column(Integer, ForeignKey(LichChuyenBay.id), nullable=False)
#     san_bay = Column(Integer, ForeignKey(SanBay.id), nullable=False)
#     thoi_gian_dung = Column(Float,nullable = False)
#     ghichu = Column(String(200),default = 'Không')
#     def gio(self):
#         return  str(math.floor(self.thoi_gian_dung))+'h'+str(round(self.thoi_gian_dung -math.floor(self.thoi_gian_dung),3)*60)+'p'


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    avatar = Column(String(200), nullable=False)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    id_ticket = relationship('Ticket', backref='userid', lazy=True)

    def __str__(self):
        return self.name

    def isAdmin(self):
        if self.user_role == UserRole.ADMIN:
            return True
        return False

    def isStaff(self):
        if self.user_role == UserRole.STAFF:
            return True
        return False

    def isUser(self):
        if self.user_role == UserRole.USER:
            return True
        return False


class Customer(BaseModel):
    name = Column(String(50), nullable=False)
    sex = Column(Enum(Sex), default=Sex.Nam)
    phone = Column(String(11), nullable=False)
    address = Column(String(50), nullable=False)
    email = Column(String(50), nullable=True)
    CMND = Column(String(12), nullable=False)
    ticket_id = relationship('Ticket', backref='customerid', lazy=True)

    def __str__(self):
        return self.name


class Ticket(BaseModel):
    id_user = Column(Integer, ForeignKey(User.id), nullable=False)
    # id_kh = Column(Integer, ForeignKey(User.id), nullable=False)
    so_ghe = Column(String(50), nullable=False)
    hang_ve = Column(Enum(LoaiHangVe), default=LoaiHangVe.HangVe1)
    details = relationship('TicketDetail', backref='Ticket', lazy=True)
    customer = Column(Integer, ForeignKey(Customer.id), nullable=True)

    # kh = relationship('User', foreign_keys=[id_kh])

    def hangVe(self):
        if self.hang_ve == LoaiHangVe.HangVe1:
            return "Hạng vé 1"
        if self.hang_ve == LoaiHangVe.HangVe2:
            return "Hạng vé 2"
        pass


# dat ve chuyen bay?
class TicketDetail(BaseModel):
    lich_chuyen_bay_id = Column(Integer, ForeignKey(LichChuyenBay.id), nullable=False)
    id_ve = Column(Integer, ForeignKey(Ticket.id), nullable=False)
    price = Column(Float, default=0)
    created_day = Column(DateTime, default=datetime.now())


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Thêm dữ liệu mẫu cho MayBay (Máy bay)
        m1 = MayBay(loai_may_bay='AIRBUS A330', so_luong_cho_ngoi=272)
        m2 = MayBay(loai_may_bay='AIRBUS A350', so_luong_cho_ngoi=350)
        m3 = MayBay(loai_may_bay='BOEING 787', so_luong_cho_ngoi=215)
        db.session.add_all([m1, m2, m3])
        db.session.commit()


        # Thêm dữ liệu mẫu cho SanBay (Sân bay)
        sb1 = SanBay(ten_san_bay="Nội Bài", dia_diem='Hà Nội')
        sb2 = SanBay(ten_san_bay='Tân Sơn Nhất', dia_diem='TPHCM')
        db.session.add_all([sb1, sb2])
        db.session.commit()


        # Thêm dữ liệu mẫu cho ChuyenBay (Chuyến bay)
        cb1 = ChuyenBay(ten_chuyen_bay="Hà Nội - TPHCM", san_bay_di=sb1, san_bay_den=sb2)
        db.session.add(cb1)
        db.session.commit()


        # Thêm dữ liệu mẫu cho LichChuyenBay (Lịch chuyến bay)
        lcb1 = LichChuyenBay(chuyen_bay_id=1, may_bay_id=1, ngay_gio=datetime(2024, 5, 20, 8, 0),
                             thoi_gian_bay=2.5, so_luong_hang_ve_1=150, so_luong_hang_ve_2=100, price=200)
        db.session.add(lcb1)
        db.session.commit()


        # Thêm dữ liệu mẫu cho Customer (Khách hàng)
        customer1 = Customer(name="John Doe", sex='Nam', phone="0123456789",
                             address="123 Main Street", email="john@example.com", CMND="123456789012")
        db.session.add(customer1)
        db.session.commit()


        # Thêm dữ liệu mẫu cho User (Người dùng)
        password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        user1 = User(name="Admin",
                     username="admin",
                     password=password,
                     avatar="https://res.cloudinary.com/dbqaequqv/image/upload/v1715784409/kbtas85leobdl5uskbvi.png",
                     user_role=UserRole.ADMIN)

        user2 = User(name="Staff",
                     username="staff",
                     password=password,
                     avatar="https://res.cloudinary.com/dbqaequqv/image/upload/v1715784409/kbtas85leobdl5uskbvi.png",
                     user_role=UserRole.STAFF)
        db.session.commit()
        db.session.add_all([user1, user2])
        db.session.commit()


        # Tạo một vé và gán id_user cho vé
        ticket1 = Ticket(id_user=1, so_ghe="A1", hang_ve='HangVe1', customer=1)
        db.session.add(ticket1)
        db.session.commit()


        # Thêm dữ liệu mẫu cho TicketDetail (Chi tiết vé)
        ticket_detail1 = TicketDetail(lich_chuyen_bay=lcb1, id_ve=1, price=200)
        db.session.add(ticket_detail1)
        db.session.commit()


        # Lưu dữ liệu vào cơ sở dữ liệu
        db.session.commit()




