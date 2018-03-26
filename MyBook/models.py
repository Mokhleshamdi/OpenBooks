

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from django.urls import reverse  # Used to generate urls by reversing the URL patterns

TITLE_CHOICES = (
    ('MR', 'Mr.'),
    ('MRS', 'Mrs.'),
    ('MS', 'Ms.'),
)

class Genre(models.Model):
    """
    Model representing a book genre (e.g. Science Fiction, Non Fiction).
    """
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")
    def __str__(self):
        return str(self.name)
class Language(models.Model):
    """
    Model representing a Language (e.g. English, French, Japanese, etc.)
    """
    name = models.CharField(max_length=200,
                            help_text="Enter a the book's natural language (e.g. English, French, Japanese etc.)")
    def __str__(self):
        return str(self.name)

class Book(models.Model):
    """
    Model representing a book (but not a specific copy of a book).
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in file.
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    # ManyToManyField used because Subject can contain many books. Books can cover many subjects.
    # Subject declared as an object because it has already been defined.
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    image=models.ImageField(upload_to='media',default='media/html.png')
    file=models.FileField(upload_to='media/files',default='media/files')
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    copies = models.IntegerField(default=1)

    def D_Genre(self):
        return ",".join ([g.name for g in self.genre.all()])

    def __str__(self):
        return str(self.title)


import uuid  # Required for unique book instances
from datetime import date, timezone

from django.contrib.auth.models import User  # Required to assign User as a borrower


class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    #imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('d', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='d', help_text='Book availability')
    def __str__(self):
        return str(self.id)
    class Meta:
        get_latest_by = "due_back"
class Author(models.Model):
    """
    Model representing an author.
    """
    first_name = models.CharField(max_length=100,choices=TITLE_CHOICES)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)
    def __str__(self):
        return str(self.first_name)
    class Meta:
        get_latest_by = "date_of_birth "

class productBacklog(models.Model):
    class Meta:
        verbose_name="Backlog de produit"
        verbose_name_plural="Backlogs de produit"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=True)
    image = models.ImageField(upload_to='media',default='media/html.png')

    def __str__(self):  # __unicode__ for Python 2
        return self.user.username


def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class BorrowedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ManyToManyField(User)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.book.title

class Comment(models.Model):
    content = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.book.title