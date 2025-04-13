from django.contrib import admin
from .models import Library, Book, User, Loan

admin.site.register(Library)
admin.site.register(Book)
admin.site.register(User)
admin.site.register(Loan)
