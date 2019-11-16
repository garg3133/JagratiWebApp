from django.db import models
from accounts.models import User
import datetime
import calendar
# Create your models here.

class Volunteer(models.Model):
	CURRENT_YEAR = datetime.datetime.now().year

	BATCH = (
		(CURRENT_YEAR		, CURRENT_YEAR),
		(CURRENT_YEAR - 1	, CURRENT_YEAR - 1),
		(CURRENT_YEAR - 2	, CURRENT_YEAR - 2),
		(CURRENT_YEAR - 3	, CURRENT_YEAR - 3),
		(CURRENT_YEAR - 4	, CURRENT_YEAR - 4),
	)

	PROGRAMME = (
		('bt'	, 'B.Tech'),
		('mt'	, 'M.Tech'),
		('phd'	, 'phD'),
		('bd'	, 'B.Des'),
		('md'	, 'M.Des'),
	)

	DESIG = (
		('Co-Convenor', (
				('mcoco', 'Math Co-Convenor'),
				('ecoco', 'English Co-Convenor'),
				('hcoco', 'Hindi Co-Convenor'),
			)
		),
		('Convenor', (
				('mco', 'Math Convenor'),
				('eco', 'English Convenor'),
				('hco', 'Hindi Convenor'),
			)
		),
		('jac'	, 'Jagrati Advisory Commitee'),
		('v'	, 'Volunteer'),
	)

	GENDER = (
		('M', 'Male'),
		('F', 'Female'),
		('O', 'Other')
	)

	roll_no 				= models.CharField(verbose_name="Roll Number", max_length=8, unique=True, primary_key=True)
	email 					= models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
	first_name 				= models.CharField(verbose_name="First Name",max_length=50)
	last_name 				= models.CharField(verbose_name="Last name",max_length=50)
	gender 					= models.CharField(max_length=1, choices=GENDER, default='M')
	batch					= models.IntegerField(choices=BATCH)
	programme				= models.CharField(max_length=2, choices=PROGRAMME)
	dob 					= models.DateField(verbose_name="Date of Birth", default=datetime.datetime.now)
	contact_no 				= models.CharField(verbose_name="Contact Number", max_length=10)
	street_address1			= models.CharField(verbose_name="Address Line 1", max_length=255)
	street_address2			= models.CharField(verbose_name="Address Line 2", max_length=255)
	city					= models.CharField(max_length=20)
	state					= models.CharField(max_length=25)
	pincode					= models.CharField(max_length=6)
	alt_email 				= models.EmailField(verbose_name="Alternate Email", max_length=255, unique=True)
	desig 					= models.CharField(verbose_name="Designation", choices=DESIG, default='v', max_length=5)
	active 					= models.BooleanField(default=True)

	def __str__(self):
		return self.roll_no

class Student(models.Model):
	VILLAGE = (
		('G', 'Gadheri'),
		('M', 'Mehgawan'),
		('C', 'Chanditola'),
		('A', 'Amanala'),
		('S', 'Suarkol'),
	)
	first_name 				= models.CharField(max_length=30)
	last_name 				= models.CharField(max_length=30)
	school_class 			= models.CharField(max_length=2)
	village 				= models.CharField(max_length=30, choices=VILLAGE, default='Gadheri')
	contact_no 				= models.CharField(max_length=10)
	guardian_name 			= models.CharField(max_length=30)
	restricted 				= models.BooleanField(default=False)

	def __str__(self):
		return self.first_name+self.last_name


class Schedule(models.Model):

	DAY = [(calendar.day_name[i], calendar.day_name[i]) for i in range(0,6)]

	SECTION = (
		('1A', "Class 1/2/3 Section-A"),
		('1B', "Class 1/2/3 Section-B"),
		('1C', "Class 1/2/3 Section-C"),
		('1I', "Class 1/2/3 Irregular"),

		('2A', "Class 4/5 Section-A"),
		('2B', "Class 4/5 Section-B"),
		('2C', "Class 4/5 Section-C"),
		('2I', "Class 4/5 Irregular"),

		('3A', "Class 6/7/8 Section-A"),
		('3B', "Class 6/7/8 Section-B"),
		('3C', "Class 6/7/8 Section-C"),
		('3I', "Class 6/7/8 Irregular"),

		('4A',  "Class 9"),
		('4B',  "Class 10"),

		('NA',  "Navodaya A"),
		('NB',  "Navodaya B"),
		('NC',  "Navodaya C"),
	)

	SUBJECT = (
		('eng', "English"),
		('hin', "Hindi"),
		('mat', "Mathematics"),
		('sci', "Science"),
	)

	day 					= models.CharField(max_length=9, choices = DAY)
	section 				= models.CharField(max_length=2, choices=SECTION)
	subject 				= models.CharField(max_length=3, choices=SUBJECT, default="hin")

	class Meta:
		unique_together = (('day', 'section'),)

	def __str__(self):
		return self.day.__str__() + " - " + self.section.__str__()


class Calendar(models.Model):
	date 					= models.DateField(primary_key=True)
	remark 					= models.TextField(max_length=255, blank=True)
	class_scheduled 		= models.BooleanField(default=True)

	def __str__(self):
		s=str(self.date)
		return s

class Volunteer_schedule(models.Model):
	roll_no  				= models.ForeignKey(Volunteer, on_delete=models.CASCADE)
	day 	 				= models.CharField(max_length=10, blank=True)
	schedule 				= models.ForeignKey(Schedule, on_delete=models.CASCADE)

	class Meta:
		unique_together = (('roll_no', 'day'),)

	def __str__(self):
		return self.roll_no.__str__() + " - " + self.schedule.__str__()

	def save(self, *args, **kwargs):
		self.day = Schedule.objects.get(id = self.schedule.id).day
		super(Volunteer_schedule, self).save(*args, **kwargs)


class Student_schedule(models.Model):
	sid 	 				= models.ForeignKey(Student, on_delete=models.CASCADE)
	day 	 				= models.CharField(max_length=10, blank=True)
	schedule 				= models.ForeignKey(Schedule, on_delete=models.CASCADE)

	class Meta:
		unique_together = (('sid', 'day'),)

	def __str__(self):
		return self.sid.__str__() + " - " + self.schedule.__str__()

	def save(self, *args, **kwargs):
		self.day = Schedule.objects.get(id = self.schedule.id).day
		super(Student_schedule, self).save(*args, **kwargs)

class cw_hw(models.Model):
	date 					= models.ForeignKey(Calendar, on_delete=models.CASCADE)
	section 				= models.ForeignKey(Schedule, on_delete=models.CASCADE)#, limit_choices_to={'day': limit(self)})
	cw 						= models.TextField(max_length=255)
	hw 						= models.TextField(max_length=255)
	# day = models.ForeignKey(Schedule.day)
	# section = models.ForeignKey(Schedule.section)
	# SCHEDULE = Schedule.objects.filter(day = date.date.strftime("%A"))

	class Meta:
		unique_together = (('date', 'section'),)

	def __str__(self):
		
		return self.date.__str__() + " - " + self.section.__str__()

	def save(self, *args, **kwargs):
		if self.date.date.strftime("%A") != Schedule.objects.get(id = self.section.id).day:
			raise ValueError("dgdgdgdd")
		else:
			super(cw_hw, self).save(*args, **kwargs)

	# def limit(self):
	# 	return {'day' : self.date.date.strftime("%A")}

class Student_attended_on(models.Model):
	sid 					= models.ForeignKey(Student, on_delete=models.CASCADE)
	date 					= models.ForeignKey(Calendar, on_delete=models.CASCADE)
	hw_dome 				= models.BooleanField(default=False)

	class Meta:
		unique_together = (('sid', 'date'),)

	def __str__(self):
		return self.sid.__str__() + " - " + self.date.__str__()


class Volunteer_attended_on(models.Model):
	roll_no 				= models.ForeignKey(Volunteer, on_delete=models.CASCADE)
	date 					= models.ForeignKey(Calendar, on_delete=models.CASCADE)

	class Meta:
		unique_together = (('roll_no', 'date'),)

	def __str__(self):
		return self.roll_no.__str__() + " - " + self.date.__str__()