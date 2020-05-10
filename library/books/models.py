from django.db import models
from django.utils.translation import ugettext as _
import uuid
import datetime
import random
YEAR_CHOICES = [(r,r) for r in range(1400, datetime.date.today().year+1)]
STATUSES = (('available', 'AVAILABLE'),
            ('borrowed', 'BORROWED'))
# Create your models here.


class User(models.Model):
    """
    Base model for user details
    """
    # Unique ID as the Primary Key instead of the default Integer Primary Key
    uid = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, editable=False,
                           verbose_name='unique id')
    username = models.CharField(_('User Name'), max_length=50, default='') # Used as user name

    #: Boolean flag to identify librarian and web users
    is_admin = models.BooleanField(_('Library staff'), default=False)

    #: User's wish list
    wishlist = models.ManyToManyField('Book', blank=True, related_name='user_wishlist')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Book(models.Model):
    """
        Base model for Book details
        """

    # Book Properties
    id = models.CharField(_('Book Id'), max_length=10, unique=True, default=str(random.randrange(10000)),
                          primary_key=True)
    isbn = models.CharField(_('ISBN'), max_length=20, unique=True)
    published_year = models.IntegerField(_('year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    title = models.CharField(_('Title'), max_length=150, default='', blank=True)
    language = models.CharField(_('Language'), max_length=50, blank=True)
    #: Foreign key to user table for authors
    authors = models.ManyToManyField('Author', blank=True, related_name='books_written')

    #: Book's availability status
    status = models.CharField(_('Availability'), max_length=20, choices=STATUSES, default='available')

    #: Number of days for which the book is rented
    rented_days = models.IntegerField(_('Rental days'), null=True, blank=True)

    #" Amazon idstatus
    amazon_id = models.CharField(_('Amazon ID'), null=True, max_length=20, blank=True)

    REQUIRED_FIELDS = ['book_id', 'isbn']

    def __init__(self, *args, **kwargs):
        super(Book, self).__init__(*args, **kwargs)
        self.__original_mode = self.status

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        """
        Function to notify users having the book on wishlist and status of it changes
        When ever status of a book changes, we need to notify the user's having that book in wish list
        :param force_insert:
        :param force_update:
        :param args:
        :param kwargs:
        :return:
        """
        if self.status != self.__original_mode:
            #: If status of book is updated, get the users having that book in their wish list
            users = self.user_wishlist.all()
            user_names = ''
            for user in users:
                user_names += user.username + ' '
            print(
                'Hi ' + user_names + ',\nThe status of book in your wish list is updated. Please find below the '
                                     'details.\n Book Name : ' + self.title + '\n Current status : ' + self.status)
        super(Book, self).save(force_insert, force_update, *args, **kwargs)
        self.__original_mode = self.status


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"


class Author(models.Model):
    """
    Class model for book writers
    """

    # Unique ID as the Primary Key instead of the default Integer Primary Key
    uid = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, editable=False,
                           verbose_name='unique id')
    username = models.CharField(_('User Name'), max_length=50, default='')  # Used as user name


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

