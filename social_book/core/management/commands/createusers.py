import csv
import json
import random
import string

from django.core.management.base import BaseCommand
from core.models import *


class Command(BaseCommand):
    help = 'Create new random users.'

    def add_arguments(self, parser):
        parser.add_argument('num_users', nargs=1, type=int)
        parser.add_argument('file_to_record', nargs=1, type=str)

    def load_names(self):
        random_names = []

        with open('names.csv', newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            random_names = [row[0] for row in csvreader]

        return random_names

    def generate_new_random_user(self):
        random_user_name = random.choice(self.load_names())

        return {
            "username": random_user_name.lower().replace(" ", "_"),
            "email": random_user_name.lower().replace(" ", "_") + "@gmail.com",
            "password": self.generate_random_password(16)
        }

    def generate_random_password(self, size: int) -> str:
        return "".join([random.choice(string.ascii_letters) for _ in range(size)])

    def handle(self, *args, **options):
        print("Reading users from the database...")

        num_users = options.get('num_users', 0)[0]
        file_to_record = options.get('file_to_record', "user.json")[0]

        users = [self.generate_new_random_user() for _ in range(num_users)]

        for u in users:
            user = User.objects.create_user(
                username=u.get("username"),
                email=u.get("email"),
                password=u.get("password"))
            user.save()

            user_model = User.objects.get(username=u.get("username"))
            new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
            new_profile.save()

        with open(file_to_record, "w") as f:
            f.write(json.dumps(users))

        print("Users were added successfully!")
