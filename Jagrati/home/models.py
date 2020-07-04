from django.db import models
from accounts.models import User
import datetime
import calendar
# Create your models here.

class Volunteer(models.Model):
	CURRENT_YEAR = datetime.datetime.now().year

	PROGRAMME = (
		('bt'	, 'B.Tech'),
		('mt'	, 'M.Tech'),
		('phd'	, 'PhD'),
		('bd'	, 'B.Des'),
		('md'	, 'M.Des'),
	)

	DESIG = (
		('Co-Convenor', (
				('mcoco', 'Math Co-Convenor'),
				('ecoco', 'English Co-Convenor'),
				('hcoco', 'Hindi Co-Convenor'),
				('scoco', 'Science Co-Convenor'),
				('9coco', '9-10 Co-Convenor'),
				('navcoco', 'Navodaya Co-Convenor'),
			)
		),
		('Convenor', (
				('mco', 'Math Convenor'),
				('eco', 'English Convenor'),
				('hco', 'Hindi Convenor'),
				('sco', 'Science Convenor'),
				('9co', '9-10 Convenor'),
				('navco', 'Navodaya Convenor'),
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

	roll_no 				= models.CharField(verbose_name="Roll Number", max_length=8, unique=True)
	email 					= models.OneToOneField(User, on_delete=models.CASCADE)
	first_name 				= models.CharField(verbose_name="First Name",max_length=50)
	last_name 				= models.CharField(verbose_name="Last name",max_length=50)
	profile_image			= models.ImageField(default='logo.png', upload_to='profile_pics')
	gender 					= models.CharField(max_length=1, choices=GENDER, default='M')
	batch					= models.IntegerField()
	programme				= models.CharField(max_length=2, choices=PROGRAMME)
	dob 					= models.DateField(verbose_name="Date of Birth", default=datetime.datetime.now)
	contact_no 				= models.CharField(verbose_name="Contact Number", max_length=13)
	street_address1			= models.CharField(verbose_name="Address Line 1", max_length=255)
	street_address2			= models.CharField(verbose_name="Address Line 2", max_length=255, blank=True)
	city					= models.CharField(max_length=20)
	state					= models.CharField(max_length=25)
	pincode					= models.CharField(max_length=6)
	alt_email 				= models.EmailField(verbose_name="Alternate Email", max_length=255, blank=True)
	desig 					= models.CharField(verbose_name="Designation", choices=DESIG, default='v', max_length=5)
	# resp					= models.ForeignKey()
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
	school_class 			= models.IntegerField()
	village 				= models.CharField(max_length=30, choices=VILLAGE, default='Gadheri')
	contact_no 				= models.CharField(max_length=13, blank=True)
	guardian_name 			= models.CharField(max_length=30, blank=True)
	restricted 				= models.BooleanField(default=False)

	def __str__(self):
		return self.first_name + " " + self.last_name


class Calendar(models.Model):
	date 					= models.DateField(primary_key=True)
	remark 					= models.TextField(max_length=255, blank=True)
	class_scheduled 		= models.BooleanField(default=True)

	class Meta:
		verbose_name_plural = 'Calendar'

	def __str__(self):
		return str(self.date)


class Section(models.Model):
	section_id = models.CharField(max_length=5, unique=True)   # For grouping and sorting
	name = models.CharField(max_length=30, unique=True)

	def __str__(self):
		return self.name


class Schedule(models.Model):

	DAY = [(calendar.day_name[i], calendar.day_name[i]) for i in range(0,6)]   # They won't ever change and will give us dropdown in Admin site

	# SECTION = (
	# 	('0A', "Section-A"),
	# 	('0B', "Section-B"),
	# 	('0C', "Section-C"),

	# 	('1', "Class 1/2/3"),
	# 	('1A', "Class 1/2/3 Section-A"),
	# 	('1B', "Class 1/2/3 Section-B"),
	# 	('1C', "Class 1/2/3 Section-C"),
	# 	('1I', "Class 1/2/3 Irregular"),

	# 	('2', "Class 4/5"),
	# 	('2A', "Class 4/5 Section-A"),
	# 	('2B', "Class 4/5 Section-B"),
	# 	('2C', "Class 4/5 Section-C"),
	# 	('2I', "Class 4/5 Irregular"),

	# 	('3', "Class 6/7/8"),
	# 	('3A', "Class 6/7/8 Section-A"),
	# 	('3B', "Class 6/7/8 Section-B"),
	# 	('3C', "Class 6/7/8 Section-C"),
	# 	('3I', "Class 6/7/8 Irregular"),

	# 	('4A',  "Class 9"),
	# 	('4B',  "Class 10"),

	# 	('NA',  "Navodaya A"),
	# 	('NB',  "Navodaya B"),
	# 	('NC',  "Navodaya C"),
	# )

	SUBJECT = (
		('eng', "English"),
		('hin', "Hindi"),
		('mat', "Mathematics"),
		('sci', "Science"),
		('mab', "Mental Ability"),
	)

	day 					= models.CharField(max_length=9, choices=DAY)
	# section 				= models.CharField(max_length=2, choices=SECTION)
	section 				= models.ForeignKey(Section, on_delete=models.CASCADE)
	subject 				= models.CharField(max_length=3, choices=SUBJECT, default="hin")

	class Meta:
		unique_together = (('day', 'section'),)

	def __str__(self):
		return self.day + " - " + self.section.name


class StudentSchedule(models.Model):
	sid 	 				= models.ForeignKey(Student, on_delete=models.CASCADE)
	day 	 				= models.CharField(max_length=10, blank=True)
	schedule 				= models.ForeignKey(Schedule, on_delete=models.CASCADE)

	class Meta:
		unique_together = (('sid', 'day'),)
		verbose_name = 'Student Schedule'
		verbose_name_plural = 'Students Schedule'

	def __str__(self):
		return self.sid.__str__() + " - " + self.schedule.__str__()

	def save(self, *args, **kwargs):
		self.day = Schedule.objects.get(id = self.schedule.id).day
		super(StudentSchedule, self).save(*args, **kwargs)


class VolunteerSchedule(models.Model):
	roll_no  				= models.ForeignKey(Volunteer, on_delete=models.CASCADE)
	day 	 				= models.CharField(max_length=10, blank=True)
	schedule 				= models.ForeignKey(Schedule, on_delete=models.CASCADE)

	class Meta:
		unique_together = (('roll_no', 'day'),)
		verbose_name = 'Volunteer Schedule'
		verbose_name_plural = 'Volunteers Schedule'

	def __str__(self):
		return self.roll_no.__str__() + " - " + self.schedule.__str__()

	def save(self, *args, **kwargs):
		self.day = Schedule.objects.get(id = self.schedule.id).day
		super(VolunteerSchedule, self).save(*args, **kwargs)


class ClassworkHomework(models.Model):
	date 					= models.ForeignKey(Calendar, on_delete=models.CASCADE)
	section 				= models.ForeignKey(Section, on_delete=models.CASCADE)
	#, limit_choices_to={'day': limit(self)})  <-- was used in section when it had FK ref to Schedule (see save method)
	# section 				= models.CharField(max_length=2, choices=Schedule.SECTION)
	cw 						= models.TextField(max_length=255, blank = True)
	hw 						= models.TextField(max_length=255, blank = True)
	comment					= models.TextField(max_length=255, blank = True)
	# day = models.ForeignKey(Schedule.day)
	# section = models.ForeignKey(Schedule.section)
	# SCHEDULE = Schedule.objects.filter(day = date.date.strftime("%A"))

	class Meta:
		unique_together = (('date', 'section'),)
		verbose_name = 'ClassWork/HomeWork'
		verbose_name_plural = 'ClassWork/HomeWork'

	def __str__(self):
		return self.date.__str__() + " - " + self.section.name

	# def save(self, *args, **kwargs):
	# 	if self.date.date.strftime("%A") != Schedule.objects.get(id = self.section.id).day:
	# 		raise ValueError("dgdgdgdd")
	# 	else:
	# 		super(ClassworkHomework, self).save(*args, **kwargs)

	# def limit(self):
	# 	return {'day' : self.date.date.strftime("%A")}


class StudentAttendence(models.Model):
	sid 					= models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Student Name")
	date 					= models.ForeignKey(Calendar, on_delete=models.CASCADE)
	present					= models.BooleanField(default=False)
	hw_done 				= models.BooleanField(default=False, verbose_name="HomeWork Done")

	class Meta:
		unique_together = (('sid', 'date'),)
		verbose_name = 'Student Attendence'
		verbose_name_plural = 'Students Attendence'

	def __str__(self):
		return self.sid.__str__() + " - " + self.date.__str__()


class VolunteerAttendence(models.Model):
	roll_no 				= models.ForeignKey(Volunteer, on_delete=models.CASCADE)
	date 					= models.ForeignKey(Calendar, on_delete=models.CASCADE)
	present					= models.BooleanField(default=False)
	extra 					= models.BooleanField(default=False)

	class Meta:
		unique_together = (('roll_no', 'date'),)
		verbose_name = 'Volunteer Attendence'
		verbose_name_plural = 'Volunteers Attendence'

	def __str__(self):
		return self.roll_no.__str__() + " - " + self.date.__str__()


class Feedback(models.Model):
	name 					= models.CharField(max_length=50)
	roll_no					= models.CharField(max_length=10, blank=True)
	email 					= models.EmailField(max_length=255, blank=True)
	feedback 				= models.TextField(max_length=1023)
	date					= models.DateTimeField(verbose_name='Date', auto_now_add=True)

	def __str__(self):
		return self.name.__str__()


class UpdateScheduleRequest(models.Model):
	volunteer 				= models.ForeignKey(Volunteer, on_delete=models.CASCADE)
	previous_schedule 		= models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='previous_schedule', null=True, blank=True)
	updated_schedule 		= models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='updated_schedule')
	date 					= models.DateTimeField(verbose_name='Date', auto_now_add=True)

	# Only one of the below booleans will be true. Request pending if all false!
	approved				= models.BooleanField(default=False)
	declined				= models.BooleanField(default=False)
	by_admin				= models.BooleanField(default=False)   # If shedule is updated by admin without request by volunteer
	cancelled				= models.BooleanField(default=False)

	def __str__(self):
		return self.volunteer.__str__()

	def save(self, *args, **kwargs):

		# Create VolunteerSchedule instance
		if self.approved is True or self.by_admin is True:   # Schedule is updated in only these two cases
			prev_sch = VolunteerSchedule.objects.filter(roll_no=self.volunteer)
			if prev_sch.exists():
				prev_sch = prev_sch[0]
				prev_sch.schedule = self.updated_schedule
				prev_sch.save()
			else:
				vol_sch = VolunteerSchedule(roll_no=self.volunteer, schedule=self.updated_schedule)
				vol_sch.save()
		
		super(UpdateScheduleRequest, self).save(*args, **kwargs)