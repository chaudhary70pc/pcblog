from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import Post

# Create your views here.
def home(request):
    return render(request, 'home/home.html')


def contact(request):
    
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<5:
             messages.error(request, "Plese fill Form Correctly")
        else:
            contact = Contact(name=name, phone=phone, email=email, content=content)
            contact.save()
            messages.success(request, "you're message has been send successfuly")
    return render(request, 'home/contact.html')


def about(request):
    return render(request, 'home/about.html')


def search(request):
    query=request.GET['query']
    if len(query) > 70:
        allPosts = []
    else:
        allPosts= Post.objects.filter(titel__icontains=query)
        allPostsAuthor= Post.objects.filter(author__icontains=query)
        allPostsContent =Post.objects.filter(content__icontains=query)
        # allPosts=  allPostsTitel.union(allPostsContent, allPostsAuthor)
    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    params={'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)




def handleSignup(request):
    if request.method == 'POST':
        #get the perameter
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        #chek errorneus input
        if len(username) >10:
            messages.error(request, "username must be under the 10 cherercter")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "plese enter the same password")
            return redirect('home')
                
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "youre pcCoder account is created")
        return redirect('home')
    
    else:
        return HttpResponse('404 -Not Found')


def handleLogin(request):
    if request.method =="POST":

        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username= loginusername, password= loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, 'you are successfully loagin')
            return redirect('home')
        else:
            messages.error(request, 'plese enter valid username and password')
            return redirect('home')
    else:
        return HttpResponse('404 -Not Found')

    

def handleLogout(request):
    # if request.method == 'POST':
        logout(request)
        messages.success(request, 'logout sucssesfuly')
        return redirect('home')
    
    
    
