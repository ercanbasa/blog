# -*- coding: utf-8 -*-
import random
import sha
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.profiles.models import Profile
from apps.blog.models import Post, PostComment


class Command(BaseCommand):
    help = "Creates the default values for project to function properly"

    def handle(self, *args, **options):
        user1 = User.objects.create_user(username="user1@user.com",
                                         password="123456",
                                         email="user1@user.com"
                                         )
        user1.first_name = "User"
        user1.last_name = "One"
        user1.save()

        p1 = Profile.objects.create(
            about="Wellcome to user1's profile.",
            user=user1,
            is_verified=True,
            activation_key="aaa"
        )

        print "user1 kullanicisi olusturuldu.(aktif kullanici)"
        print "email: user1@user.com"
        print "sifre: 123456"

        user2 = User.objects.create_user(username="user2@user.com",
                                         password="123456",
                                         email="user2@user.com"
                                         )
        user2.first_name = "User"
        user2.last_name = "Two"
        user2.is_active = False
        user2.save()

        p2 = Profile.objects.create(
            about="Wellcome to user2's profile.",
            user=user2,
            is_verified=False,
            activation_key="bbb"
        )

        print "user2 kullanicisi olusturuldu.(dogrulanmamis kullanici)"
        print "email: user2@user.com"
        print "sifre: 123456"

        user3 = User.objects.create_user(username="user3@user.com",
                                         password="123456",
                                         email="user3@user.com"
                                         )
        user3.first_name = "User"
        user3.last_name = "Three"
        user3.is_active = False
        user3.save()

        p3 = Profile.objects.create(
            about="Wellcome to user3's profile.",
            user=user3,
            is_verified=True,
            is_deleted=True,
            activation_key="ccc"
        )


        print "user3 kullanicisi olusturuldu.(silinmis kullanici)"
        print "email: user3@user.com"
        print "sifre: 123456"

        c1 = "In magna mi, aliquam eget interdum ac, luctus bibendum arcu. Curabitur sem ante, elementum nec fermentum ut, gravida eget mi. Fusce quis tempus nunc. Vestibulum quis mi a neque scelerisque lobortis. Vivamus tincidunt suscipit metus, eu lobortis turpis tempor vitae. Phasellus sed ante erat, at scelerisque lacus. Proin varius ligula quis quam semper condimentum."
        c2 = "Duis blandit risus dapibus quam condimentum eu dictum mauris congue. Phasellus nisl metus, lobortis sed volutpat id, lobortis nec dolor. Sed id magna eu ante euismod faucibus et eu lorem. Ut eget mi in diam hendrerit consectetur quis non magna. Ut non dolor dictum justo viverra dapibus. Pellentesque justo mauris, eleifend eu dictum sit amet, aliquet non tortor. Nam lacus augue, adipiscing in feugiat in, vulputate a elit. Donec elementum nulla mauris, vel luctus nisi."
        c3 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis volutpat auctor libero, ut malesuada eros vehicula ut. Nam eu facilisis ligula. Vivamus at neque sed massa vestibulum congue. Vestibulum libero augue, hendrerit ut pretium in, imperdiet eget felis. Aenean cursus interdum dictum. Vivamus in massa mollis nisi consequat molestie eget eu magna. Mauris accumsan euismod orci vel imperdiet. Suspendisse potenti. Mauris pharetra, augue sit amet commodo pulvinar, velit turpis vehicula urna, ac posuere enim nibh in diam."

        t1 = "In magna mi"
        t2 = "Duis blandit risus dapibus quam"
        t3 = "Lorem ipsum dolor sit amet"

        post1 = Post.objects.create(author = p1, title = t1, content = c1)
        post2 = Post.objects.create(author = p3, title = t2, content = c2)
        post3 = Post.objects.create(author = p1, title = t3, content = c3)

        print "blog postlari olusturuldu"
        print post1
        print post2
        print post3

        # def guest_comments(post=None, name=None, verify=False):
        #     GUESTS = {
        #         'guest1': ['Guest One', 'guest1@guest.com', 'guest1', 'greetings from greece'],
        #         'guest2': ['Guest Two', 'guest2@guest.com', 'guest2', 'you are best'],
        #         'guest3': ['Guest Three', 'guest3@guest.com', 'guest3', 'are you kidding me'],
        #         'guest4': ['Guest Four', 'guest4@guest.com', 'guest4', 'what the hell'],
        #         'guest5': ['Guest Five', 'guest5@guest.com', 'guest5', 'you stole two minutes from my life'],
        #         'guest6': ['Guest Six', 'guest6@guest.com', 'guest6', 'good job, bro'],
        #
        #     }
        #
        #     guest = GUESTS[name]
        #
        #     comment = PostComment.objects.create(post=post,
        #                                          anonymous_name=guest[0],
        #                                          anonymous_mail=guest[1],
        #                                          activation_key=guest[2],
        #                                          content=guest[3],
        #                                          is_verified=verify
        #                                          )
        #     return comment
        #
        #
        # print "post1 in yorumlari olusturuluyor"
        # com = guest_comments(post1, "guest1", True)
        # CommentComment.objects.create(
        #         post_comment=com, writer=p1, content="thank you")
        # CommentComment.objects.create(
        #         post_comment=com, writer=p3, content="i dont believe you")
        # com = guest_comments(post1, "guest2", False)
        # com = guest_comments(post1, "guest5", True)
        # CommentComment.objects.create(
        #         post_comment=com, writer=p1, content="good comment")
        # com = guest_comments(post1, "guest3", False)
        # com = guest_comments(post1, "guest6", True)
        #
        # print "post2 nin yorumlari olusturuluyor"
        # com = guest_comments(post2, "guest3", True)
        # CommentComment.objects.create(
        #         post_comment=com, writer=p3, content="really good")
        # CommentComment.objects.create(
        #         post_comment=com, writer=p1, content="i dont think like you")
        # com = guest_comments(post2, "guest2", True)
        # com = guest_comments(post2, "guest6", True)
        # CommentComment.objects.create(
        #         post_comment=com, writer=p1, content="nice")
        # com = guest_comments(post2, "guest5", False)
        # com = guest_comments(post2, "guest4", True)
        #
        # print "post3 nin yorumlari olusturuluyor"
        # com = PostComment.objects.create(post=post3, writer=p3, content="nice")
        # CommentComment.objects.create(
        #         post_comment=com, writer=p1, content="i dont think like you")
        # CommentComment.objects.create(
        #         post_comment=com, writer=p3, content="i dont care")
        # CommentComment.objects.create(
        #         post_comment=com, writer=p1, content="nice")
        # com = guest_comments(post3, "guest4", True)
        # com = guest_comments(post3, "guest5", True)
        #
        # print "default degerler eklendi. islem bitti."
