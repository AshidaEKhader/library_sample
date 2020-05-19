from django.urls import path
from .views import BookListView, WishListUpdateView, BookStatusUpdateView, BookReportView, BookAmazonUpdateView

# URLs for User related views
urlpatterns = [
    #: API to search books using title and author
    path('books/list', BookListView.as_view(), name='book_list'),
    path('wishlist/update', WishListUpdateView.as_view(), name='wishlist_update'),
    path('book/update', BookStatusUpdateView.as_view(), name='book_update'),
    path('book/report', BookReportView.as_view(), name='report'),
    path('amazon/update', BookAmazonUpdateView.as_view(), name='amazon_update'),
]
