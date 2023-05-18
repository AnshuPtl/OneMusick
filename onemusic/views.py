from django.shortcuts import render,redirect
from .models import User,Product,Cart
from django.conf import settings
from django.core.mail import send_mail
import random



def index(request):
	products=Product.objects.all()
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user,payment_status=False)
	request.session['cart_count']=len(carts)
	return render(request,"index.html",{'products':products})

def seller_index(request):
	return render(request,"seller_index.html")

def about(request):
	return render(request,"about.html")

def blog(request):
	return render(request,"blog.html")

def events(request):
	products=Product.objects.all()
	return render(request,"events.html",{'products':products})

def contacts(request):
	return render(request,"contacts.html")

def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'],password=request.POST['password'])
			if user.usertype=="Organizer":
				request.session['email']=user.email
				request.session['fname']=user.fname
				request.session['lname']=user.lname
				return render(request,"seller_index.html")

			else:
				request.session['email']=user.email
				request.session['fname']=user.fname
				request.session['lname']=user.lname
				carts=Cart.objects.filter(user=user,payment_status=False)
				request.session['cart_count']=len(carts)
				return render(request,"index.html")

		except Exception as e:
			print(e)
			msg1="Email or Password Does Not Matched!!!"
			return render(request,"login.html",{'msg1':msg1})

	else:
		return render(request,"login.html")

def signup(request):
	if request.method=="POST":
		try:
			User.objects.get(email=request.POST['email'])
			msg1="Email Already Exist"
			return render(request,"signup.html",{'msg1':msg1})

		except:
			if request.POST['password'] == request.POST['cpassword']:
				User.objects.create(
					fname=request.POST['fname'],
					lname=request.POST['lname'],
					mobile=request.POST['mobile'],
					email=request.POST['email'],
					password=request.POST['password'],
					usertype=request.POST['usertype'],
				)

				msg="Sign Up Successful"
				return render(request,"signup.html",{'msg':msg})

			else:
				msg1="Password and Confim Password Does Not Matched !!!"
				return render(request,"signup.html",{'msg1':msg1})

	else:
		return render(request,"signup.html")


def logout(request):

	try:

		del request.session['email']
		del request.session['fname']
		del request.session['cart_count']
		return render(request,'login.html')
	
	except:

		return render(request,'login.html')


def change_password(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])

		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				user.password=request.POST['new_password']
				user.save()
				return redirect('logout')

			else:
				msg1="New Password & Confirm New Passwrd Does Not Matched !!!"
				return render(request,'change_password.html',{'msg1':msg1})

		else:
				msg1="Old Passwrd Does Not Matched !!!"
				return render(request,'change_password.html',{'msg1':msg1})

	else:
		return render(request,'change_password.html')


def forgot_password(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			otp = random.randint(1000,9999)
			subject = 'OTP - Forgot Password'
			message = "Hello "+user.fname+ ", Your OTP : "+str(otp)
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user.email,]
			send_mail( subject, message, email_from, recipient_list )
			msg="OTP Sent Successful"
			return render(request,'verify_otp.html',{'email':user.email,'otp':otp,'msg':msg})

		except Exception as e:
			print(e)
			print("Hello1")
			msg1="Email Does Not Exist !!!"
			return render(request,'forgot_password.html',{'msg1':msg1}) 

	else:
		return render(request,'forgot_password.html')


def verify_otp(request):
	email=request.POST['email']
	otp=request.POST['otp']
	uotp=request.POST['uotp']

	if otp==uotp:
		return render(request,'new_password.html',{'email':email})

	else:
		msg1="OTP Does Not Matched !!!"
		return render(request,'verify_otp.html',{'email':email, 'otp':otp,'msg1':msg1})


def new_password(request):
	
	if request.POST['new_password']==request.POST['cnew_password']:
		user = User.objects.get(email=request.POST['email'])
		user.password=request.POST['new_password']
		user.save()

		return redirect('login')

	else:
		msg1="New Password & Condirm New password Does Not 'Matched !!!"
		return render(request,'new_password.html',{'email':email, 'msg1':msg1})

def profile(request):
	return render (request,'profile.html')

def seller_change_password(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])

		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				user.password=request.POST['new_password']
				user.save()
				return redirect('logout')

			else:
				msg1="New Password & Confirm New Passwrd Does Not Matched !!!"
				return render(request,'seller_change_password.html',{'msg1':msg1})

		else:
				msg1="Old Passwrd Does Not Matched !!!"
				return render(request,'seller_change_password.html',{'msg1':msg1})

	else:
		return render(request,'seller_change_password.html')


def seller_add_product(request):

	if request.method=="POST":
		seller=User.objects.get(email=request.session['email'])
		Product.objects.create(
				seller=seller,
				product_name=request.POST['product_name'],
				product_price=request.POST['product_price'],
				product_qty=request.POST['product_qty'],
				product_desc=request.POST['product_desc'],
				product_image=request.FILES['product_image'],
				product_venue=request.POST['venue'],
				product_time=request.POST['time'],
				product_date=request.POST['date'],
			)

		msg="Concert Added Successfully"
		return render(request,'seller_add_product.html',{'msg':msg})

	else:
		return render(request,'seller_add_product.html')

def seller_view_product(request):
	seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=seller)
	return render(request,'seller_view_product.html',{'products':products})

def seller_product_detail(request,pk):
	product=Product.objects.get(pk=pk)
	return render(request,'seller_product_detail.html',{'product':product})

def seller_product_edit(request,pk):
	product=Product.objects.get(pk=pk)
	if request.method=="POST":
		product.product_name=request.POST['product_name']
		product.product_desc=request.POST['product_desc']

		try:
			product.product_image=request.FILES['product_image']
			product.product_qty=request.POST['product_qty']
			product.product_price=request.POST['product_price']
			product.product_venue=request.POST['product_venue']
			product.product_date=request.POST['product_date']
			product.product_time=request.POST['product_time']

		except:
			pass
		
		product.save()
		msg="Concert Updated Successfully"
		return render(request,'seller_product_detail.html',{'product':product, 'msg':msg})

	else:
		return render(request,'seller_product_edit.html',{'product':product})

def seller_product_delete(request,pk):
	product=Product.objects.get(pk=pk)
	product.delete()
	return redirect('seller_view_product')

def product_detail(request,pk):
	cart_flag=False
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	try:
		Cart.objects.get(user=user,product=product)
		cart_flag=True
	except:
		pass

	return render(request,'product_detail.html',{'product':product,'cart_flag':cart_flag})

def cart(request):
	net_price=0
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user,payment_status=False)
	request.session['cart_count']=len(carts)
	for i in carts:
		net_price+=i.total_price
	return render(request,'cart.html',{'carts':carts,'net_price':net_price})

def add_to_cart(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	Cart.objects.create(user=user,
		product=product,
		product_qty=1,
		product_price=product.product_price,
		total_price=product.product_price
		)

	return redirect('cart')

def remove_from_cart(request,pk):

	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	Cart.objects.get(user=user,product=product).delete()

	carts=Cart.objects.filter(user=user,payment_status=False)
	request.session['cart_count']=len(carts)

	return redirect('cart')

def change_qty(request):
	pk=request.POST['cid']
	product_qty=int(request.POST['product_qty'])
	cart=Cart.objects.get(pk=pk)
	cart.product_qty=product_qty
	cart.total_price=cart.product_price*product_qty
	cart.save()

	return redirect('cart')

def initiate_payment(request):
	user=User.objects.get(email=request.session['email'])
	try:
		amount = int(request.POST['amount'])
	except:
		return render(request, 'cart.html', context={'error': 'Wrong Accound Details or amount'})

	transaction = Transaction.objects.create(made_by=user,amount=amount)
	transaction.save()
	merchant_key = settings.PAYTM_SECRET_KEY

	params = (
	    ('MID', settings.PAYTM_MERCHANT_ID),
	    ('ORDER_ID', str(transaction.order_id)),
	    ('CUST_ID', str(transaction.made_by.email)),
	    ('TXN_AMOUNT', str(transaction.amount)),
	    ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
	    ('WEBSITE', settings.PAYTM_WEBSITE),
	    # ('EMAIL', request.user.email),
	    # ('MOBILE_N0', '9911223388'),
	    ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
	    ('CALLBACK_URL', 'http://localhost:8000/callback/'),
	    # ('PAYMENT_MODE_ONLY', 'NO'),
	)

	paytm_params = dict(params)
	checksum = generate_checksum(paytm_params, merchant_key)

	transaction.checksum = checksum
	transaction.save()

	carts=Cart.objects.filter(user=user,payment_status=False)
	for i in carts:
		i.payment_status=True
		i.save()

	paytm_params['CHECKSUMHASH'] = checksum
	print('SENT: ', checksum)
	return render(request, 'redirect.html', context=paytm_params)


