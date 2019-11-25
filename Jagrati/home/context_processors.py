from .models import(
	Volunteer,
	Volunteer_schedule,
	Volunteer_attended_on,
	Student,
	Student_schedule,
	Student_attended_on,
	Calendar,
	Schedule,
	Cw_hw,
) 

def database_context(request):
	if request.user.is_authenticated:
		# Logged in Volunteer's data
		obj = Volunteer.objects.filter(email = request.user)
		if obj.exists():
			volunteer = obj[0]
			obj2 = Volunteer_schedule.objects.filter(roll_no = volunteer)
			if obj2.exists():
				vol_schedule = obj2[0]
			else:
				vol_schedule = None
		else:
			volunteer = None
			vol_schedule = None


		return {
			'volunteer': volunteer,
			'volunteers': Volunteer.objects.all(),
			'vol_schedule': vol_schedule,
			'vol_schedules': Volunteer_schedule.objects.all(),
			'schedules' : Schedule.objects.order_by('section'),
		}

	else:
		return {}