from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login as auth_login
from .models import Book, Profile, BorrowedBook, Comment
from .forms  import AddBookForm,LoginForm, AddUserForm, BookUpdateForm, UserUpdateForm, CommentForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate,login,logout
from django.db.models.query import QuerySet

def home(request):

    book=Book.objects.all()
    query=request.GET.get("q")
    if query:
        book=book.filter(title__icontains=query)

    return render(request,"index.html",{'book':book})
def details(request,b_id):
    book=Book.objects.get(id =b_id)
    group = Group.objects.get(name='lib')
    bookform = BookUpdateForm(request.POST or None)
    comments = Comment.objects.filter(book=book)
    commentform = CommentForm()

    if request.method == 'POST':
        if bookform.is_valid():
            book = bookform
            book.save()
            return redirect(reverse('details', kwargs={'id': id}))
    try:
        borrowed_book = BorrowedBook.objects.get(book=book, borrower=request.user)
    except:
        borrowed_book = None
    if request.method == 'POST':
        book_borrow(request.user, book)
        return redirect('/index')
    context={'book':book, 'group': group, 'borrowed_book': borrowed_book,'commentform': commentform,  'comments': comments,'bookform': bookform}
    return render(request, 'details.html', context)
def delete(request,b_id):
    group = Group.objects.get(name='lib')

    b=Book.objects.get(id=b_id)

    if group not in request.user.groups.all():
        return redirect('/index')

    b.delete()

    return HttpResponseRedirect('/index')

def ajouter(request):
    group = Group.objects.get(name='lib')

    form=AddBookForm(request.POST,request.FILES)
    if form.is_valid():
        f=form.save(commit=False)
        f.user=request.user
        form.save()
        return HttpResponseRedirect('/index')
    if group not in request.user.groups.all():
        return redirect('/index')

    return render(request,"ajouter.html",{'form':form})
def back(request):
   return HttpResponseRedirect('/index')
def profile(request, username):
    user = User.objects.get(username=username)
    book = Book.objects.filter(user=user)
    return render(request, 'profile.html',{'user': user,'book': book})
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username=u, password=p)
            if user is not None:
                if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect('/index')
                else:
                    print("The account has been disabled!")
            else:
                print("The username and password were incorrect.")
    else:
        form = LoginForm()
        return render(request, 'login.html',{'form': form})
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def like_book(request):
    book_id = request.POST.get('treasure_id', None)
    likes = 0
    if (book_id):
        book = Book.objects.get(id=int(book_id))
        if book is not None:
            likes = book.likes + 1
            book.likes = likes
            book.save()

    return HttpResponse(likes)


def Bookupdate(request, b_id=None):
        group = Group.objects.get(name='lib')
        book = Book.objects.get(id=b_id)
        form = BookUpdateForm(request.POST or None, request.FILES or None, instance=book)

        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return redirect('/%s' % (book.id))
        if group not in request.user.groups.all():
            return redirect('/%s' % (book.id))
        context = {'form': form}
        return render(request, 'edit.html', context)
def signIn(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if request.method=='POST':

            if form.is_valid():
                inst=form.save()
                groupe=Group.objects.get(name="user")
                inst.groups.add(groupe)
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return HttpResponseRedirect('/index')
    else:
        form = AddUserForm()
    return render(request, 'signIn.html', {'form': form})
def user_list(request):
    group = Group.objects.get(name='lib')
    u=User.objects.filter(groups__name='user')
    if group not in request.user.groups.all():
        return redirect('/index')
    return render(request, "user_list.html", {'Profile': u})
def User_update(request, key=None):
    group = Group.objects.get(name='lib')
    user = User.objects.get(id=key)
    form = UserUpdateForm(request.POST or None, request.FILES or None, instance=user)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('user_list')
    if group not in request.user.groups.all():
        return redirect('/index')
    context = {'form': form}
    return render(request, 'user_update.html', context)

def user_search(request):
    group = Group.objects.get(name='lib')
    query = request.GET.get('q')
    user = User.objects.filter(username=query)
    if group not in request.user.groups.all():
        return redirect('/index')
    context = {'users': user}
    return render(request, 'user_search.html', context)

def user_add(request):
    group = Group.objects.get(name='lib')
    form = UserCreationForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            inst = form.save()
            groupe = Group.objects.get(name="user")
            inst.groups.add(groupe)
            return redirect('/index')
    context = {'form': form}
    if group not in request.user.groups.all():
        return redirect('/index')
    return render(request, 'add_user.html', context)
def delete_user(request,u_name=None):
    p=Profile.objects.get(id=u_name)
    p.delete()
    return HttpResponseRedirect('/')
def search_user(request):
    query = request.GET.get('q')
    user = User.objects.filter(username=query)
    context = {'members': user}
    return render(request, 'user_search.html', context)

def book_borrow(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        if book.copies > 0:
            borrowed_book = BorrowedBook()
            borrowed_book.book = book
            borrowed_book.save()
            borrowed_book.borrower.add(request.user)
            borrowed_book.save()
            book.copies -= 1
            book.save()
            return redirect('/%s' %(book.id))

    return redirect('/%s' %(book.id))


def book_return(request, id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=id)
        try:
            borrowed_book = BorrowedBook.objects.get(book=book, borrower=request.user)
        except:
            borrowed_book = None
        book.copies += 1
        book.save()
        borrowed_book.delete()
        return redirect('/%s' %(id))

    return redirect('/%s' %(id))

def book_comment(request, id):
    book = Book.objects.get(id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.comment_author = request.user
            instance.book = book
            instance.save()
            return redirect('/%s' %(book.id))

    return redirect('/%s' %(book.id))