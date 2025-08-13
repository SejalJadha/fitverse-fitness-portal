from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate,login,logout
from authapp.models import Contact,MembershipPlan,Trainer,Enrollment,Attendance,Gallery


def home(request):
    return render(request,'authapp/index.html')


def signup(request):
    if request.method == "POST":
        username = request.POST.get('usernumber')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
      
        # Validate phone number
        if not username.isdigit() or len(username) != 10:
            messages.error(request, "Phone number must be 10 digits")
            return redirect('signup')

        # Validate passwords match
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')
            
        # Validate password strength
        if len(pass1) < 8:
            messages.error(request, "Password must be at least 8 characters")
            return redirect('signup')

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email format")
            return redirect('signup')
       
        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Phone number already registered")
            return redirect('signup')
           
        # Check if email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('signup')
        
        # Create user
        try:
            user = User.objects.create_user(username, email, pass1)
            user.save()
            messages.success(request, "Account created successfully! Please login")
            return redirect('handlelogin')
        except Exception as e:
            messages.error(request, f"Error creating account: {str(e)}")
            return redirect('signup')
            
    return render(request, 'authapp/signup.html')

def handlelogin(request):
    if request.method=="POST":        
        username=request.POST.get('usernumber')
        pass1=request.POST.get('pass1')
        myuser=authenticate(username=username,password=pass1)
        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Successful")
            return redirect('/')
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/login')
            
    return render(request,'authapp/handlelogin.html')

def handlelogout(request):
    logout(request)
    messages.success(request,"Logout Success")    
    return redirect('/login')


def contact(request):
    if request.method=="POST":
        name=request.POST.get('fullname')
        email=request.POST.get('email')
        number=request.POST.get('num')
        desc=request.POST.get('desc')
        myquery=Contact(name=name,email=email,phonenumber=number,description=desc)
        myquery.save()       
        messages.info(request,"Thanks for Contacting us we will get back you soon")
        return redirect('/contact')
        
    return render(request,'authapp/contact.html')

def enroll(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login and Try Again")
        return redirect('/login')
    
    Membership=MembershipPlan.objects.all()
    SelectTrainer=Trainer.objects.all()
    context={"Membership":Membership,"SelectTrainer":SelectTrainer}
    if request.method=="POST":
        FullName=request.POST.get('FullName')
        email=request.POST.get('email')
        gender=request.POST.get('gender')
        PhoneNumber=request.POST.get('PhoneNumber')
        DOB=request.POST.get('DOB')
        member=request.POST.get('member')
        trainer=request.POST.get('trainer')
        reference=request.POST.get('reference')
        address=request.POST.get('address')
        query=Enrollment(FullName=FullName,Email=email,Gender=gender,PhoneNumber=PhoneNumber,DOB=DOB,SelectMembershipplan=member,SelectTrainer=trainer,Reference=reference,Address=address)
        query.save()
        messages.success(request,"Thanks For Enrollment")
        return redirect('/enroll')
    return render(request,'authapp/enroll.html',context)

def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login and Try Again")
        return redirect('/login')
    user_phone=request.user
    posts=Enrollment.objects.filter(PhoneNumber=user_phone)
    attendance=Attendance.objects.filter(phonenumber=user_phone)
    print(posts)
    context={"posts":posts,"attendance":attendance}
    return render(request,"authapp/profile.html",context)

def gallery(request):
    posts=Gallery.objects.all()
    context={"posts":posts}
    return render(request,"authapp/gallery.html",context)

def attendance(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login and Try Again")
        return redirect('/login')
    SelectTrainer=Trainer.objects.all()
    context={"SelectTrainer":SelectTrainer}
    if request.method=="POST":
        phonenumber=request.POST.get('PhoneNumber')
        Login=request.POST.get('logintime')
        Logout=request.POST.get('loginout')
        SelectWorkout=request.POST.get('workout')
        TrainedBy=request.POST.get('trainer')
        query=Attendance(phonenumber=phonenumber,Login=Login,Logout=Logout,SelectWorkout=SelectWorkout,TrainedBy=TrainedBy)
        query.save()
        messages.warning(request,"Attendace Applied Success")
        return redirect('/attendance')
    return render(request,"authapp/attendance.html",context)
