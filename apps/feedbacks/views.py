from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Feedback, Contact


def index(request):
    if request.method == 'POST':
        anonymous_array = request.POST.getlist('anonymousCheck')
        name = request.POST['name']
        roll_no = request.POST['rollNo']
        email = request.POST['email']
        feedback = request.POST['feedback']
        if len(anonymous_array) != 0:
            feedback = Feedback(name='Anonymous', feedback=feedback)
            feedback.save()
        else:
            feedback = Feedback(name=name, roll_no=roll_no, email=email, feedback=feedback)
            feedback.save()
        return redirect('feedbacks:feedback_submitted')

    context = {
        'logout_redirect_site': request.path,
        'login_redirect_site': request.path,
    }
    return render(request, 'feedbacks/index.html', context)

def feedback_submitted(request):
    return render(request, 'feedbacks/feedback_submitted.html')


@csrf_exempt
def contact(request):
    if request.method == 'POST':
        try:
            name = request.POST['full_name']
            phone = request.POST['phone']
            email = request.POST['email_id']
            msg = request.POST['msg']
            # save the data in database
            contact_data = Contact(name=name, phone=phone, email=email, message=msg)
            contact_data.save()
            # print(name, phone, email, msg)
            messages.success(request, 'Your Contact information is saved successfully.')
            return redirect('home:new_index')
        except Exception:
            messages.error(request, 'Error, On Submitting the contact form.')
            return redirect('home:new_index')
    return redirect('home:new_index')
