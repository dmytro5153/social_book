import random

from django.core.management.base import BaseCommand
from social_book.social_book.core.models import *



class Command(BaseCommand):
    help = 'Create new random posts for a requested username.'

    social_media_posts = [
        "Feeling adventurous and ready to explore #adventure #nature",
        "Just had a fantastic meeting with my team #teamwork #success",
        "Can't stop listening to this new album #music #newrelease",
        "Feeling motivated after watching a TED talk #motivation #inspiration",
        "Had a great day out with the family #family #fun",
        "Loving this new app #technology #innovation",
        "Feeling relaxed after a spa day #spa #relaxation",
        "Can't wait for the weekend to start #weekend #fun",
        "Just got a new puppy and he's already a part of the family #puppy #family",
        "Had a great time at the concert last night #music #concert",
        "Enjoying a beautiful day at the beach #beach #sun",
        "Feeling creative after a painting class #art #creativity",
        "Can't wait to try this new restaurant #food #yum",
        "Just had a great hike in the mountains #hiking #outdoors",
        "Feeling accomplished after finishing a project #accomplishment #success",
        "Having a great time at the festival #festival #fun",
        "Feeling energized after a cardio class #fitness #workout",
        "Can't wait to watch the new movie #movies #cinema",
        "Just had a great Skype call with friends #skype #friends",
        "Just had the best cup of coffee #coffee #caffeinefix",
        "Feeling grateful for this beautiful sunset #sunset #grateful",
        "Can't wait to travel again #travel #wanderlust",
        "Just finished a great book #reading #bookworm",
        "Had a great workout at the gym #gym #fitness",
        "Loving this new song #music #newrelease",
        "Feeling inspired by this quote #inspiration #motivation",
        "Can't believe it's already Friday #weekend #TGIF",
        "Just got a new haircut and feeling fresh #haircut #newlook",
        "Had a great time with friends at the park #friends #outdoors",
        "Enjoying a delicious meal #food #yum",
        "Feeling productive after a day of work #productivity #work",
        "Can't wait for the weekend #weekend #relax",
        "Just learned something new #learning #growth",
        "Feeling accomplished after completing a task #accomplishment #success",
        "Having a great day #goodday #positivity",
        "Feeling refreshed after a yoga class #yoga #relaxation",
        "Can't wait to try this new recipe #cooking #foodie",
        "Just had a great conversation #conversation #friends"
    ]

    def add_arguments(self, parser):
        parser.add_argument('username', nargs=1, type=str)
        parser.add_argument('num_posts', nargs=1, type=int)

    def handle(self, *args, **options):
        username = options['username'][0]
        num_posts = options['num_posts'][0]

        print(f"Creating {num_posts} posts for user {username}...")

        for _ in range(num_posts):
            new_post = *.objects.create(user=username, caption=random.choice(self.social_media_posts))
            new_post.save()
            print(f"Created new post: {new_post.id}")
