from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.db.models import Q
from .models import *
from django.contrib import messages
from .forms import EmployeeCreationForm, LeaveApplicationForm, accountCreation
from datetime import date, datetime, timedelta
from time import strftime
import holidays

annual_leave_max_days_for_civilian_and_below_ip_employees = 30
annual_leave_max_days_for_employees_above_ip = 36


# Create your views here.
def home(request):
    template_name = 'leave_management_app/index.html'
    return render(request, template_name)


@login_required(login_url='login')
def dashboard(request):
    template_name = 'leave_management_app/dashboard.html'
    employees_count = Employee.objects.all().count()
    leaves_count = Leave_type.objects.all().count()
    applications_count = Leave_application.objects.filter(financial_year=current_financial_year).count()
    departments_count = Department.objects.all().count()
    context = {'employees_count': employees_count, 'leaves_count': leaves_count,
               'applications_count': applications_count,
               'departments_count': departments_count}
    return render(request, template_name, context)


def EmployeeRegistration(request):
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeCreationForm()
    return render(request, 'accounts/employee_register.html', {'form': form})


# --------------------------listview-----------------------
class EmployeeListView(ListView):
    model = Employee
    context_object_name = 'employees'
    ordering = '-date_created'
    template_name = 'employee_list.html'
    paginate_by = 10


class LeaveListView(ListView):
    model = Leave_type
    context_object_name = 'leaves'
    template_name = 'leave_type_list.html'

class UsersListView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'leave_management_app/user_list.html'

class DepartmentListView(ListView):
    model = Department
    context_object_name = 'departments'
    template_name = 'department_list'
    paginate_by = 8


class ApplicationListview(ListView):
    model = Leave_application
    context_object_name = 'applications'
    ordering = '-leave_application_date'
    template_name = 'leave_application_list'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(financial_year=current_financial_year)


class PreviousLeaveApplications(ListView):
    model = Leave_application
    context_object_name = 'applications'
    ordering = '-leave_application_date'
    template_name = 'previous_leave_application.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(financial_year=previous_financial_year)


class AllLeaveApplications(ListView):
    model = Leave_application
    context_object_name = 'applications'
    ordering = '-leave_application_date'
    template_name = 'all_leave_application.html'
    paginate_by = 10


# --------------------------------DetailView---------------------#
class EmployeeDetailView(DetailView):
    model = Employee


class LeaveDetailView(DetailView):
    model = Leave_type


class DepartmentDetailView(DetailView):
    model = Department


class LeaveApplicationDeatail(DetailView):
    model = Leave_application


# ---------------------------------Updateview--------------------#
class EmployeeUpdateView(UpdateView):
    model = Employee
    fields = ['emp_personal_no', 'employee_firstname', 'employee_lastname',
              'employee_email', 'employee_department_id',
              'employee_designation', 'employee_gender', 'employee_category']

    def form_valid(self, form):
        return super(EmployeeUpdateView, self).form_valid(form)


class LeaveUpdateView(UpdateView):
    model = Leave_type
    fields = ['leave_type_name', 'leave_duration', 'leave_type_description']


def employeeDeactivate(request, pk):
    employee = Employee.objects.filter(emp_personal_no=pk)
    if employee.is_active:
        employee.is_active = False
        return redirect('employee_list')
    templatename = 'leave_management_app/activate_employee.html'
    context = {'employee': employee}
    return render(request, templatename, context)


# -------------------------------Createview---------------------#
class LeaveCreateView(CreateView):
    model = Leave_type
    fields = ['leave_type_name', 'leave_duration', 'leave_type_description']

    def form_valid(self, form):
        return super(LeaveCreateView, self).form_valid(form)


class DepartmentCreateView(CreateView):
    model = Department
    fields = ['department_name', 'branch_id']

    def form_valid(self, form):
        return super(DepartmentCreateView, self).form_valid(form)


def searchEmployeeView(request):
    template_name = 'leave_management_app/search_employee.html'
    employee = Employee.objects.all()
    context = {'employee': employee}
    return render(request, template_name, context)


def search(request):
    if request.method == 'POST':
        searched_employee = request.POST['pfno']
        employee = Employee.objects.filter(
            Q(emp_personal_no__contains=searched_employee) | Q(employee_firstname__contains=searched_employee))
        templatename = 'leave_management_app/search.html'
        context = {'searched_employee': searched_employee, 'employee': employee}
        return render(request, templatename, context)
    else:
        templatename = 'leave_management_app/search.html'
        return render(request, templatename, {})


def applicationform(request, pk):
    application = Leave_application.objects.get(id=pk)
    employee_no = application.Applicant_id
    employee = Employee.objects.get(emp_personal_no=employee_no)
    print(employee.employee_lastname)
    templatename = 'leave_management_app/applicationform.html'
    context = {'application': application, 'employee': employee}
    return render(request, templatename, context)


# -------------------------------financial year----------------------start---------->
# -------------------------------financial year----------------------start---------->
# finding current financial year
Todaydate = date.today()
currentyear = strftime("%Y")
todaysdate = date.today()
intcurrentyear = int(currentyear)
intnextyear = intcurrentyear + 1
timelimit = date(intcurrentyear, 7, 31)

if Todaydate > timelimit:
    baseyear = intcurrentyear
    upperyear = baseyear + 1
    stringbaseyear = str(baseyear)
    stringupperyear = str(upperyear)
    strings = [stringbaseyear, stringupperyear]
    current_financial_year = '-'.join(strings)

elif Todaydate <= timelimit:
    baseyear = intcurrentyear - 1
    upperyear = intcurrentyear
    stringbaseyear = str(baseyear)
    stringupperyear = str(upperyear)
    strings = [stringbaseyear, stringupperyear]
    current_financial_year = '-'.join(strings)

# finding previous financial year
if todaysdate > timelimit:
    previous_year_base_year = int(currentyear) - 1
    previous_upper_year = currentyear

    strings = [str(previous_year_base_year), previous_upper_year]
    previous_financial_year = '-'.join(strings)

elif todaysdate <= timelimit:
    previous_year_upper_year = int(currentyear) - 1
    previous_year_base_year = previous_year_upper_year - 1

    strings = [str(previous_year_base_year), str(previous_year_upper_year)]
    previous_financial_year = '-'.join(strings)


# --------------------------------------financial year----------------end-------------->
# --------------------------------------financial year----------------end-------------->

# ------------------------calculating_leave_eligible_days---------------start---------------->

# ------------------------calculating_leave_eligible_days-------------------end------------>
def create_leave_application(request, id):
    leave_objects = Leave_type.objects.all()
    employee = Employee.objects.all()
    emp = Employee.objects.get(emp_personal_no=id)
    year = current_financial_year
    previous_financialyear = previous_financial_year
    if emp.employee_category == "Aip":
        maximum_annual_leave_days = annual_leave_max_days_for_employees_above_ip
    else:
        maximum_annual_leave_days = annual_leave_max_days_for_civilian_and_below_ip_employees

    # ------------------------------------previous-year-application--days----------------------->
    previous_year_applications = Leave_application.objects.filter(Q(Applicant_id=id),
                                                                  Q(financial_year=previous_financial_year))

    total_days_applied_previous_year = sum([x.no_of_days_applied for x in previous_year_applications])

    # --------------------------------------previous--year--days-carried--forward---------------------->
    if total_days_applied_previous_year == 0:
        total_days_carried_forward = maximum_annual_leave_days * 0.5
    else:
        total_days_carried_forward = maximum_annual_leave_days - total_days_applied_previous_year

    # --------------------------------------current--year--application-days---------------------------->
    employee_current_year_applications = Leave_application.objects.filter(Q(Applicant_id=id),
                                                                          Q(financial_year=current_financial_year))
    total_current_year_applied_days = sum([i.no_of_days_applied for i in employee_current_year_applications])

    # -------------------annual-leave-eligible-days----------------------------------------------------->
    annual_leave_eligible_days = sum([(maximum_annual_leave_days - total_current_year_applied_days),
                                      total_days_carried_forward])

    # ----------------------leave-application-form---------------------------------------------------->
    if request.method == 'POST':
        # -----------------------avoiding-weekends-and-holidays-to-get-leave-end-date------------------------>
        days_applied_to_add = request.POST.get('days_applied')
        business_days_to_add = int(days_applied_to_add)
        startdate = request.POST.get('startdate')
        date_frmt_start = datetime.strptime(startdate, "%Y-%m-%d")

        while business_days_to_add > 0:
            date_frmt_start += timedelta(days=1)
            weekday = date_frmt_start.weekday()
            if weekday >= 5 or weekday in holidays.KE().items():  # sunday = 6
                continue
            business_days_to_add -= 1
        remaining_leave_days = int(annual_leave_eligible_days) - int(days_applied_to_add)
        print(remaining_leave_days)
        applicant_id = request.POST.get('application_id')
        financial_yr = request.POST.get('financial_yr')
        leave_id = request.POST.get('leave_id')
        days_applied = request.POST.get('days_applied')
        enddate = request.POST.get('enddate')
        start_date = request.POST.get('startdate')

        leave_start_date_format = datetime.strptime(start_date, "%Y-%m-%d")

        if int(days_applied) > int(annual_leave_eligible_days):
            template_name = 'leave_management_app/leave_application_form.html'
            error = messages.warning(request, 'days applied greater than eligible days: try fewer days')
            context = {'error': error, 'employee': employee, 'emp': emp,
                       'year': year, 'leave_objects': leave_objects,
                       'days_applied': days_applied, 'start_date': start_date}
            return render(request, template_name, context)
        elif leave_start_date_format < datetime.today():
            template_name = 'leave_management_app/leave_application_form.html'
            error = messages.warning(request, 'invalid date!! enter date beyond today')
            context = {'error': error, 'employee': employee, 'emp': emp, 'year': year, 'leave_objects': leave_objects,
                       'days_applied': days_applied, 'start_date': start_date}
            return render(request, template_name, context)

        for yr in range(intcurrentyear, intnextyear):

            if leave_start_date_format.weekday() >= 5 or leave_start_date_format in holidays.KE(years=yr).items():
                template_name = 'leave_management_app/leave_application_form.html'
                error = messages.warning(request, 'chosen start date is weekend/holiday choose a weekday that is not '
                                                  'a holiday')
                context = {'error': error, 'employee': employee, 'emp': emp, 'year': year,
                           'leave_objects': leave_objects,
                           'days_applied': days_applied, 'start_date': start_date}
                return render(request, template_name, context)
        else:

            application = Leave_application()
            application.Applicant_id = applicant_id
            application.financial_year = financial_yr
            application.no_of_days_applied = days_applied
            application.leave_type_id = leave_id
            application.remaining_leave_days = remaining_leave_days
            application.leave_starting_date = start_date
            application.leave_end_date = date_frmt_start
            application.save()
            return redirect('current_year_applications')

    context = {'employee': employee, 'emp': emp, 'year': year, 'leave_objects': leave_objects,
               'previous_financialyear': previous_financialyear,
               'total_days_applied_previous_year': total_days_applied_previous_year,
               'employee_current_year_applications': employee_current_year_applications,
               'employee_previous_year_applications': previous_year_applications,
               'total_days_carried_forward': total_days_carried_forward,
               'total_current_year_applied_days': total_current_year_applied_days,
               'annual_leave_eligible_days': annual_leave_eligible_days}
    template_name = 'leave_management_app/leave_application_form.html'

    return render(request, template_name, context)


def leaveStatusView(request, pk):
    leave_objects = Leave_type.objects.all()
    employee = Employee.objects.all()
    emp = Employee.objects.get(emp_personal_no=pk)
    year = current_financial_year
    previous_financialyear = previous_financial_year

    # -----------------------------------------CHECKING EMPLOYEE CATEGORY MAX ANNUAL LEAVE DAYS----------->
    if emp.employee_category == "Aip":
        maximum_annual_leave_days = annual_leave_max_days_for_employees_above_ip
    else:
        maximum_annual_leave_days = annual_leave_max_days_for_civilian_and_below_ip_employees

    # ------------------------------------previous-year-application--days----------------------->
    previous_year_applications = Leave_application.objects.filter(Q(Applicant_id=pk),
                                                                  Q(financial_year=previous_financial_year))

    total_days_applied_previous_year = sum([x.no_of_days_applied for x in previous_year_applications])

    # --------------------------------------previous--year--days-carried--forward---------------------->
    if total_days_applied_previous_year == 0:
        total_days_carried_forward = maximum_annual_leave_days * 0.5
    else:
        total_days_carried_forward = maximum_annual_leave_days - total_days_applied_previous_year

    # --------------------------------------current--year--application-days---------------------------->
    employee_current_year_applications = Leave_application.objects.filter(Q(Applicant_id=pk),
                                                                          Q(financial_year=current_financial_year))
    total_current_year_applied_days = sum([i.no_of_days_applied for i in employee_current_year_applications])

    # -------------------annual-leave-eligible-days----------------------------------------------------->
    annual_leave_eligible_days = sum([(maximum_annual_leave_days - total_current_year_applied_days),
                                      total_days_carried_forward])
    templatename = "leave_management_app/leavestatus.html"
    context = {'employee': employee, 'emp': emp, 'year': year, 'leave_objects': leave_objects,
               'previous_financialyear': previous_financialyear,
               'total_days_applied_previous_year': total_days_applied_previous_year,
               'employee_current_year_applications': employee_current_year_applications,
               'previous_year_applications': previous_year_applications,
               'total_days_carried_forward': total_days_carried_forward,
               'total_current_year_applied_days': total_current_year_applied_days,
               'annual_leave_eligible_days': annual_leave_eligible_days}

    return render(request, templatename, context)


def createuseraccount(request):
    if request.method == 'POST':
        form = accountCreation(request.POST)
        if form.is_valid():
            username = request.GET.get('username')
            form.save()
            messages.success(request, 'Account created successfully')

            return redirect('dashboard')
    else:
        form = accountCreation()
    templatename = 'leave_management_app/useraccount.html'
    context = {'form': form}
    return render(request, templatename, context)


# --------------------------login---------------------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error = messages.warning(request, f'wrong username or password retry!!!')
            context = {'error': error}
            return render(request, 'accounts/login.html', context)
    else:
        return render(request, 'accounts/login.html')


# ------------------------logout view----------------------------------------------
def logout_view(request):
    logout(request)
    return redirect('home')


# -------------------------------profile------------------------------------------
@login_required(login_url='login')
def user_profile_details(request):
    values = Employee.objects.filter(Q(user=request.user))
    print(values)
    context = {'values': values}
    return render(request, 'accounts/profile.html', context)


# -----------------------------activate/deactivate----employee--------------------

def deactivate_employee(request, id):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect('home')
    employee = get_object_or_404(Employee, emp_personal_no=id)
    employee.is_active = False
    employee.save()
    messages.success(request, 'Employee is deactivated', extra_tags='alert alert-warning alert-dismissible show')
    return redirect('employee_list')


def activate_employee(request, id):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect('home')
    employee = get_object_or_404(Employee, emp_personal_no=id)
    employee.is_active = True
    employee.save()
    messages.success(request, 'Employee is activated', extra_tags='alert alert-success alert-dismissible show')
    return redirect('employee_list')

    # --------------------------------system reports-------------------------------------------


def reports(request):
    templatename = 'leave_management_app/reports.html'
    return render(request, templatename)


def employee_report(request, id):
    templatename = 'leave_management_app/employee_report.html'
    employee = Employee.objects.get(emp_personal_no=id)
    leave_objects = Leave_application.objects.filter(Q(Applicant_id=id))
    total_applications = leave_objects.all().count()
    organisation = Organisation.objects.all()
    context = {'employee': employee, 'leave_objects': leave_objects, 'organisation': organisation,
               'total_applications': total_applications}
    return render(request, templatename, context)

def custom_report(request):
    templatename = 'leave_management_app/custom_report.html'
    organisation = Organisation.objects.all()

    leave_objects = Leave_type.objects.all()
    leaves_total = leave_objects.count()

    leave_applications = Leave_application.objects.all()

    leave_application_total = leave_applications.count()

    employee = Employee.objects.all()
    active_employees = employee.filter(Q(is_active='True'))
    inactive_employees = employee.filter(Q(is_active='False'))

    total_aboveIp_employees = employee.filter(Q(employee_category='IP&Above')).count()
    total_belowIP_employees = employee.filter(Q(employee_category='Below IP')).count()
    total_civilian_employees = employee.filter(Q(employee_category='Civilian')).count()

    total_active_employees = active_employees.count()
    total_inactive_employees = inactive_employees.count()

    departments = Department.objects.all()
    total_departments = departments.count()
    context = {'employee': employee, 'organisation': organisation,
               'leaves_total': leaves_total, 'leave_objects': leave_objects,
               'leave_applications': leave_applications, 'leave_application_total': leave_application_total,
               'total_active_employees': total_active_employees, 'active_employees': active_employees,
               'inactive_employees': inactive_employees, 'total_inactive_employees': total_inactive_employees,
               'total_aboveIp_employees': total_aboveIp_employees, 'total_belowIP_employees': total_belowIP_employees,
               'total_civilian_employees': total_civilian_employees, 'departments': departments,
               'total_departments': total_departments
                }
    return render(request, templatename, context)

# -----------------------usage report-------------------------------
# def usage_report(request):
#     templatename = 'leave_management_app/usage_report.html'
#     if request.method == 'POST':
#
#     context = {}
#     return render(request, templatename, context)
