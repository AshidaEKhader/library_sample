"""
TO load the csv data given to database
"""
import logging
from django.core.management.base import BaseCommand
from books.models import Book, Author
from books import errors as err
import csv

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def create_or_get_authors(self, author_name):
        """
        Create authors for books
        :return: author instance
        """
        try:
            # Check if an author with give name exist
                # If so get the first author with given name else create one
            author, created = Author.objects.get_or_create(username=author_name)
            return author
        except Exception as e:
            logger.error('Error inside get or create function for author')
            raise err.ValidationError(*(400, e))

    def create_book(self, data):
        try:
            authors = data.pop('authors').split(',')
            book_instance = Book.objects.create(**data)
            for author_name in authors:
                author_instance = self.create_or_get_authors(author_name)
                book_instance.authors.add(author_instance)
        except Exception as e:
            logger.error('Error inside create book method')
            raise err.ValidationError(*(400, e.args[0]))

    def handle(self, *args, **options):
        try:
            #: Before trying to import delete the existing to avoid duplication
            Book.objects.all().delete()
            with open('Backend Data.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 1
                for row in csv_reader:
                    if line_count == 1:
                        line_count += 1
                        continue
                    print(row[2])
                    data = dict(id=row[0], isbn=row[1], authors=row[2], published_year=int(row[3]), title=row[4],
                                language=row[5])
                    self.create_book(data)
                    line_count += 1
        except Exception as e:
            logger.error('Error inside handle for sync db')
            raise err.ValidationError(*(400, e.args[0]))