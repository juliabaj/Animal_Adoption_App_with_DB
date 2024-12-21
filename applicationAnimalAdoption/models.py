from django.db import models
from django.contrib.auth.models import User


class Owners(models.Model):
    owner_id = models.AutoField(primary_key=True)
    owner_name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Powiązanie z User
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=9)
    email = models.CharField(max_length=50)
    is_verified = models.CharField(max_length=20, choices=[('unverified', 'Unverified'), ('in_progress', 'In_progress'),
                                                           ('verified', 'Verified')], default='unverified')

    def save(self, *args, **kwargs):
        if self.is_verified == 'verified':
            # Link this owner to an animal (example logic)
            animal = Animals.objects.filter(owner__isnull=True).first()
            if animal:
                animal.owner = self
                animal.save()
        super().save(*args, **kwargs)

    @property
    def user_username(self) -> str:
        return self.user.username

    def __str__(self):
        return self.user.username


# class User(models.Model):
#     id = models.AutoField(primary_key=True)
#     username = models.CharField(max_length=20)
#     password = models.CharField(max_length=20)
#
#     def __str__(self):
#         return self.id

class Animals(models.Model):
    animal_id = models.AutoField(primary_key=True)  # Primary Key
    animal_name = models.CharField(max_length=10)
    birth_date = models.DateTimeField()
    species = models.CharField(max_length=20)
    gender = models.CharField(max_length=6, choices=[('male', 'Male'), ('female', 'Female')])
    owner = models.ForeignKey('Owners', on_delete=models.CASCADE, null=True, blank=True)
    adoption_status = models.CharField(max_length=20, choices=[('available', 'Available'), ('pending', 'Pending'),
                                                               ('adopted', 'Adopted')], default='available')

    def __str__(self):
        return self.animal_name


class HealthRecords(models.Model):
    animal_id = models.ForeignKey('Animals', on_delete=models.CASCADE)
    diagnosis = models.CharField(max_length=100)
    veterinarian = models.CharField(max_length=50)
    treatment = models.CharField(max_length=50)
    chipped = models.BooleanField()
    vaccinated = models.BooleanField()


class Admins(models.Model):
    admin_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    passwd = models.CharField(max_length=20)

    def __str__(self):
        return self.admin_id


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
