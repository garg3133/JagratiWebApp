from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Volunteer, Schedule, Volunteer_schedule
from django.http import HttpResponse
import datetime

# Create your views here.
def index(request):
	if request.user.is_authenticated:
		return redirect('dashboard')
	return render(request, 'home/index.html')

def dashboard(request):
	if request.user.is_authenticated:
		email = request.user
		if not Volunteer.objects.filter(email=email).exists():
			return redirect('set_profile')
		return render(request, 'home/dashboard.html')
	return redirect('home')

def volunteerInformation(request):
	if request.user.is_authenticated:
		schedules = Schedule.objects.all()
		email = request.user
		if Volunteer.objects.filter(email=email).exists():
			return redirect('dashboard')
		if request.method == 'POST':
			roll = str(email)
			rollnum = roll.split('@')[0]
			roll_no         = rollnum
			first_name      = request.POST['first_name']
			last_name       = request.POST['last_name']
			gender          = request.POST['gender']
			alt_email       = request.POST['alt_email']
			batch           = request.POST['batch']
			programme       = request.POST['programme']
			street_address1 = request.POST['street_address1']
			street_address2 = request.POST['street_address2']
			pincode         = request.POST['pincode']
			city            = request.POST['city']
			state           = request.POST['state']
			dob             = request.POST['dob']
			contact_no      = request.POST['contact_no']
			# sch_id          = request.POST['schedule']
			# sch_day         = Schedule.objects.get(id = sch_id).day
			vol_obj = Volunteer(
				email           = email,
				roll_no         = roll_no,
				first_name      = first_name,
				last_name       = last_name,
				gender          = gender,
				city            = city,
				state           = state,
				dob             = dob,
				contact_no      = contact_no,
				pincode         = pincode,
				programme       = programme,
				batch           = batch,
				alt_email       = alt_email,     
				street_address1 = street_address1,
				street_address2 = street_address2,
			)
			vol_obj.save()
			# sch_obj = Volunteer_schedule(
			# 	roll_no         = Volunteer.objects.get(roll_no = roll_no),
			# 	day             = sch_day,
			# 	schedule        = Schedule.objects.get(id = sch_id),
			# )
			
			# sch_obj.save()
			
			return redirect('dashboard')
		
		return render(request, 'home/set_profile.html', {
			'cur_year': datetime.datetime.now().year - 4,
			# 'schedule': schedules,
			})
	else:
		return redirect('login_signup')

		