import string
import random
from models.models import User, Group, Post, Comment
from bson import ObjectId
from datetime import datetime
from random import randint
from werkzeug.security import generate_password_hash


def create_user(n):
    for i in range(n):
        username = ''.join([random.choice(string.ascii_letters) for k in range(8)])
        password = generate_password_hash(''.join([random.choice(string.digits) for k in range(2)]))
        number = randint(0, n)
        email = "{username}{number}@gmail.com".format(username=username, number=number)

        User(username=username, password=password, email=email).save()


def create_group(n):
    for i in range(n):
        accessibility = ['private', 'public']

        name = ''.join([random.choice(string.ascii_letters) for k in range(10)])
        # first member is the admin
        Group(name=name, visibility=random.choice(accessibility)).save()  # role_dict={str(user_id):'ADMIN'}


def add_user_group():
    from itertools import islice
    users = User.objects
    user_list = []
    roles = ['ADMIN', 'MODERATOR', 'MEMBER']
    for user in users:
        user_list.append(str(user.id))
    total = len(user_list)
    distribution = []
    for val in range(0, total, 30):
        if total - val > 30:
            distribution.append(30)
        else:
            distribution.append(total - val)
    in_put = iter(user_list)
    out_put = [list(islice(in_put, ele)) for ele in distribution]
    groups = Group.objects
    count = 0
    for group in groups:
        temp_dict = {}
        for val in out_put[count]:
            temp_dict[val] = random.choice(roles)
        group.update(set__role_dict=temp_dict)
        count += 1


def add_post_comment():
    groups = Group.objects
    for group in groups:
        temp_dict = group.last_active_dict
        for user_id in group.role_dict.keys():
            temp_dict[user_id] = datetime.now()
            name = ''.join([random.choice(string.ascii_letters + string.digits) for k in range(9)])
            content1 = "post is {name}".format(name=name)
            post = Post(user_id=ObjectId(user_id), group_id=ObjectId(group.id), content=content1).save()
            content2 = "comment is {name}".format(name=name)
            Comment(user_id=ObjectId(user_id), post_id=post.id, content=content2).save()
        group.update(set__last_active_dict=temp_dict)
