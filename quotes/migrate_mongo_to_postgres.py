
import os
import django
from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE
from dateutil import parser as date_parser
from decouple import config

# Підключення Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quotes.settings")
django.setup()

# Імпорт Django моделей
from quoteapp.models import Author as PGAuthor, Quote as PGQuote, Tag, User

# Підключення до MongoDB
MONGO_ADMIN_PASSWORD = config("MONGO_ADMIN_PASSWORD")
connect(db="dz09", host=f"mongodb+srv://mongoadmin:{MONGO_ADMIN_PASSWORD}@cl0.59adrmp.mongodb.net/?retryWrites=true&w=majority&appName=cl0")

class MongoAuthor(Document):

    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors"}

class MongoQuote(Document):

    author = ReferenceField(MongoAuthor, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=40))
    quote = StringField()
    meta = {"collection": "quotes"}

print("Перед міграцією у нову БД postgres має бути створений суперкористувач: python manage.py createsuperuser")
print("== Початок міграції ==")

user = User.objects.get(pk=1)

# Міграція авторів
mongo_authors = MongoAuthor.objects()
mongo_id_to_pg = {}

for mongo_author in mongo_authors:

    try:
        born = date_parser.parse(mongo_author.born_date).date()
    except Exception:
        print(f"[!] Неможливо розпарсити дату: {mongo_author.born_date}")
        continue

    pg_author, created = PGAuthor.objects.get_or_create(
        name=mongo_author.fullname,
        born=born,
        location=mongo_author.born_location,
        description=mongo_author.description,
        user=user
    )
    mongo_id_to_pg[str(mongo_author.id)] = pg_author
    print(f"{'Створено' if created else 'Існує'}: {pg_author.name}")

# Міграція цитат
mongo_quotes = MongoQuote.objects()

for mongo_quote in mongo_quotes:

    pg_author = mongo_id_to_pg.get(str(mongo_quote.author.id))
    if not pg_author:
        print(f"[!] Автор не знайдений для цитати: {mongo_quote.quote}")
        continue

    pg_quote = PGQuote.objects.create(
        quote_text=mongo_quote.quote,
        author=pg_author,
        user=user
    )

    for tag_name in mongo_quote.tags:

        tag, _ = Tag.objects.get_or_create(name=tag_name)
        pg_quote.tags.add(tag)

    print(f"Цитата додана: {pg_quote.quote_text[:30]}...")

print("== Міграція завершена ==")