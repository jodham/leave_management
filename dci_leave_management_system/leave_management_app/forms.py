from django.contrib.auth.models import User

from .models import Employee, Leave_application
from django import forms
from django.contrib.auth.forms import UserCreationForm


class EmployeeCreationForm(forms.ModelForm):
    employee_email = forms.EmailField()

    class Meta:
        model = Employee
        fields = ['user', 'emp_personal_no', 'employee_firstname', 'employee_lastname',
                  'employee_email', 'employee_department_id',
                  'employee_designation', 'employee_gender', 'employee_category']

    def __init__(self, *args, **kwargs):
        super(EmployeeCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['user', 'emp_personal_no', 'employee_firstname', 'employee_lastname',
                          'employee_email', 'employee_department_id',
                          'employee_designation', 'employee_gender', 'employee_category']:
            self.fields[fieldname].help_text = None


class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = Leave_application
        fields = ['Applicant', 'leave_type',
                  'leave_application_date', 'leave_starting_date', 'leave_end_date']


class accountCreation(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(accountCreation, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1']:
            self.fields[fieldname].help_text = None