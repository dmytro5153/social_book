import random

from django.core.management.base import BaseCommand
from core.models import Post


class Command(BaseCommand):
    help = 'Like random posts of a user.'

    def add_arguments(self, parser):
        parser.add_argument('username', nargs=1, type=str)
        parser.add_argument('num_post', nargs=1, type=int)

    def handle(self, *args, **options):
        username = options['username'][0]
        num_post = options['num_post'][0]

        print(f"Liking {username} user posts {num_post} times...")

        posts = list(Post.objects.filter(user=username))
        
        for post in random.choices(posts, k=num_post):
            post.no_of_likes += 1
            post.save()

            print(f"Liked post {post.id}")
