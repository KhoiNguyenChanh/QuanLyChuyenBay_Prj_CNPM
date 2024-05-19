from flask import redirect, request
from flask_login import current_user, logout_user
from QuanLyChuyenBay.models import MayBay, SanBay, LichChuyenBay, ChuyenBay, UserRole, User
from QuanLyChuyenBay import db, app, dao
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from datetime import datetime


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class AirportView(AuthenticatedModelView):
    column_searchable_list = ['ten_san_bay', 'dia_diem']
    column_filters = ['ten_san_bay', 'dia_diem']
    can_view_details = True
    can_export = True
    column_labels = {
        'ten_san_bay': 'Tên sân bay',
        'dia_diem': 'Địa điểm',
        'tinh_trang_con_trong': 'Tình trạng còn trống'
    }
    # column_exclude_list =


class PlaneView(AuthenticatedModelView):
    column_searchable_list = ['loai_may_bay', 'so_luong_cho_ngoi']
    column_filters = ['loai_may_bay', 'so_luong_cho_ngoi']
    can_view_details = True
    can_export = True
    column_labels = {
        'loai_may_bay': 'Loại máy bay',
        'so_luong_cho_ngoi': 'Số lượng chỗ ngồi',
        'TinhTrangRanh': 'Tình trạng rãnh'
    }
    # column_exclude_list =


class FlightView(AuthenticatedModelView):
    column_searchable_list = ['ten_chuyen_bay']
    column_filters = ['ten_chuyen_bay']
    can_view_details = True
    can_export = True
    column_labels = {
        'san_bay_di_id': 'Sân bay đi',
        'san_bay_den_id': 'Sân bay đến',
        'san_bay_di': 'Sân bay đi',
        'san_bay_den': 'Sân bay đến',
        'ten_chuyen_bay': 'Tên chuyến bay',
        'trang_thai': 'Trạng thái',
        'loai_may_bay': 'Máy bay'
    }

    column_select_related_list = ("san_bay_di",)
    # column_exclude_list = ['may_bay_id']


class FlightScheduleView(AuthenticatedModelView):
    column_searchable_list = ['so_luong_hang_ve_1', 'so_luong_hang_ve_2', 'price', MayBay.loai_may_bay,
                              ChuyenBay.ten_chuyen_bay, 'ngay_gio']
    column_filters = ['so_luong_hang_ve_1', 'so_luong_hang_ve_2', 'price']
    can_view_details = True
    # can_view_details = True
    can_export = True
    column_exclude_list = ['image']
    column_labels = {
        'san_bay_trung_gian': 'Sân bay trung gian',
        'ngay_gio': 'Ngày giờ',
        'thoi_gian_bay': 'Thời gian bay',
        'so_luong_hang_ve_1': 'Số lượng hạng vé 1',
        'so_luong_hang_ve_2': 'Số lượng hạng vé 2',
        'price': 'Giá vé',
        'trang_thai_cho_ngoi': 'Trạng thái chỗ ngồi',
    }


class LogoutView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


class StatsView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        total = []
        chuyenbay = dao.load_chuyen_bay()
        stats = dao.stats_revenue(kw=request.args.get('kw'), month=request.args.get('month'))
        month_stats = dao.flight_month_stats(year=request.args.get('year', datetime.now().year))
        for s in stats:
            if s[2]:
                total.append(s[2])
            else:
                total.append(0)
        tong_doanh_thu = sum(total)
        return self.render('admin/stats.html', stats=stats, cb=chuyenbay,
                           tong_doanh_thu=tong_doanh_thu, month_stats=month_stats, month=request.args.get('month'))


class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        stats = dao.count_flight_by_flightSchedule()
        return self.render('admin/index.html', stats=stats)


admin = Admin(app=app, name='QUẢN TRỊ HỆ THỐNG CHUYẾN BAY', template_mode='bootstrap4', index_view=MyAdminView())
admin.add_view(PlaneView(MayBay, db.session, name='Máy bay'))
admin.add_view(AirportView(SanBay, db.session, name='Sân Bay'))
admin.add_view(FlightView(ChuyenBay, db.session, name='Chuyến bay'))
admin.add_view(FlightScheduleView(LichChuyenBay, db.session, name='Lịch chuyến bay'))
admin.add_view(StatsView(name='Thống kê'))
admin.add_view(LogoutView(name='Đăng xuất'))
