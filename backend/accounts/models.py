from django.contrib.auth.models import AbstractUser
from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    

class OrgUser(AbstractUser):
    # -- Could add in future
    # USER_ROLES = (
    #     ('admin', 'Admin'),
    #     ('manager', 'Manager'),
    #     ('employee', 'Employee'),
    # )
    # role = models.CharField(max_length=20, choices=USER_ROLES, default='employee')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='users', null = True, blank = True)