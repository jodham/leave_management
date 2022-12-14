from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Employee
from django.contrib.auth.models import User


# def create_employee(sender, instance, created, **kwargs):
#     if created:
#         Employee.objects.create(user=instance)
#         print("User created successfully")


# post_save.connect(create_employee, sender=User)

# post_save.connect(create_employee, sender=User)
# @receiver(post_save, sender=User)
# def update_employee(sender, instance, created, **kwargs):
#     if created == False:
#         instance.employee.save()
#         print("employee updated successfully")

# post_save.connect(update_employee, sender=User)
