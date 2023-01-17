from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import date
from time import strftime, gmtime

# Create your models here.
employee_category_list = [
    ('Civilian', 'Civilian'),
    ('Below IP', 'Below IP'),
    ('IP&Above', 'IP&Above'),
]

gender = [
    ('M', 'Male'),
    ('F', 'Female')
]

leave_category_list = [
    ('Annual', 'Annual Leave'),
    ('Paternity', 'Paternity Leave'),
    ('Maternity', 'Maternity Leave')
]


class Organisation(models.Model):
    organisation_name = models.CharField(max_length=150)
    organisation_address = models.CharField(max_length=50)
    organisation_email = models.EmailField()

    def __str__(self):
        return self.organisation_name


class Organisation_branch(models.Model):
    branch_name = models.CharField(max_length=50)
    organisation_id = models.ForeignKey(Organisation, on_delete=models.CASCADE)

    def __str__(self):
        return self.branch_name


class Department(models.Model):
    department_name = models.CharField(max_length=100)
    branch_id = models.ForeignKey(Organisation_branch, on_delete=models.CASCADE)

    def __str__(self):
        return self.department_name

    def get_absolute_url(self):
        return reverse('department_detail', kwargs={'pk': self.pk})


class Employee(models.Model):
    emp_personal_no = models.CharField(max_length=20, primary_key=True)
    employee_firstname = models.CharField(max_length=20)
    employee_lastname = models.CharField(max_length=20)
    employee_email = models.EmailField()
    employee_department_id = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    employee_designation = models.CharField(max_length=20)
    employee_gender = models.CharField(choices=gender, max_length=6)
    employee_category = models.CharField(choices=employee_category_list, max_length=10)
    date_created = models.DateTimeField(default=timezone.now)
    date_employed = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.fullname()

    def fullname(self):
        return '{}  {}'.format(self.employee_firstname, self.employee_lastname)

    def get_absolute_url(self):
        return reverse('employee_detail', kwargs={'pk': self.pk})

    def add_to_staff_group(sender, instance, created, **kwargs):
        if created:
            staff_group = Group.objects.get(name="staff")
            instance.groups.add(staff_group)
    post_save.connect(add_to_staff_group, sender=User)

# @receiver(post_save, sender=User)
# def create_employee(sender, instance, created, **kwargs):
#     if created:
#         Employee.objects.create(user=instance)
#         print('created employee')
#
#
# post_save.connect(create_employee, sender=User)
#
#
# @receiver(post_save, sender=User)
# def save_employee(sender, instance, **kwargs):
#     instance.employee.save()
#     print('employee updated')
#
#
# post_save.connect(save_employee, sender=User)
#

class Leave_type(models.Model):
    leave_type_name = models.CharField(choices=leave_category_list, max_length=30)
    leave_duration = models.CharField(default='30/36 days', max_length=30)
    leave_type_description = models.TextField()

    def __str__(self):
        return self.leave_type_name

    def get_absolute_url(self):
        return reverse('leave_detail', kwargs={'pk': self.pk})


class Leave_application(models.Model):
    Applicant = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL)
    financial_year = models.CharField(max_length=10)
    leave_type = models.ForeignKey(Leave_type, on_delete=models.CASCADE)
    medical_certificate = models.BooleanField(default=False)
    no_of_days_applied = models.IntegerField(default=30)
    remaining_leave_days = models.CharField(max_length=2)
    leave_application_date = models.DateTimeField(default=timezone.now)
    leave_starting_date = models.DateField()
    leave_end_date = models.DateField()

    def __str__(self):
        return '{}'.format(self.Applicant)

    def get_absolute_url(self):
        return reverse('leave_application_detail', kwargs={'pk': self.pk})
