from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),

    path('create/employee', EmployeeRegistration, name='EmployeeRegistration'),

    path('employee/list', EmployeeListView.as_view(), name='employee_list'),
    path('employee/detail/<int:pk>', EmployeeDetailView.as_view(), name='employee_detail'),
    path('employee/update/<int:pk>', EmployeeUpdateView.as_view(), name='employee_update'),
    path('employee/account/', createuseraccount, name='useraccount'),
    path('employee/profile', user_profile_details, name="profile"),
    path('employee/<int:id>', deactivate_employee, name='deactivateEmployee'),
    path('employee/activate/<int:id>', activate_employee, name='activateEmployee'),

    path('leave/create', LeaveCreateView.as_view(), name='leave_create'),
    path('leave/list', LeaveListView.as_view(), name='leave_list'),
    path('leave/detail/<int:pk>', LeaveDetailView.as_view(), name='leave_detail'),
    path('leave/update/<int:pk>', LeaveUpdateView.as_view(), name='leave_update'),
    path('leave/status/<int:pk>', leaveStatusView, name='leave_status'),


    path('department/create/', DepartmentCreateView.as_view(), name='department_create'),
    path('department/list', DepartmentListView.as_view(), name='department_list'),
    path('department/detail/<int:pk>', DepartmentDetailView.as_view(), name='department_detail'),

    path('application/list', ApplicationListview.as_view(), name='current_year_applications'),
    path('application/create/<int:id>', create_leave_application, name='create_application'),
    path('application/previous/list', PreviousLeaveApplications.as_view(), name='previous_year_applications'),
    path('application/all/list', AllLeaveApplications.as_view(), name='all_leave_applications'),
    path('application/detail/<int:pk>', LeaveApplicationDeatail.as_view(), name='leave_application_detail'),
    path('application/form/<int:pk>', applicationform, name='application_form'),

    path('employee/search', searchEmployeeView, name='search_employee'),
    path('search/employee', search, name='search'),

    path('reports/', reports, name='reports'),
    path('employee/report/<int:id>', employee_report, name='employee_report'),
    path('reports/custom/', custom_report, name="custom_report"),
   # path('reports/usage/', usage_report, name='usage_report'),

    path('users/', UsersListView.as_view(), name='available_users'),
    path('user/login', login_view, name='login'),
    path('user/logout', logout_view, name='logout')
]
