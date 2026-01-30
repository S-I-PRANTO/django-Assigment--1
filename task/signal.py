from django.dispatch import receiver
from django.db.models.signals import post_save,m2m_changed
from django.contrib.auth.models import  Group
from django.conf import settings
from django.core.mail import send_mail
from task.models import Event
from django.contrib.auth import get_user_model
User=get_user_model()

@receiver(m2m_changed,sender=Event.participants.through)
def RSVP_sentMail(sender,instance,action,pk_set,**kwargs):
    if action == 'post_add':
        for user_id in pk_set:
            try:
                user=User.objects.get(id=user_id)
                user_email = [user.email]
                subject="RSVP Confirmation"
                message=(
                     f"Hi{user.username},\n\n"
                     f"You have Successfully RSVP for the event : \n"
                     f"{instance.Event_name}\n\n"
                     "Thank you "
                )
                send_mail(
                     subject,message,settings.EMAIL_HOST_USER,user_email,fail_silently=True

                )
            except Exception as e :
                   print(f"Failed to send RSVP email: {str(e)}")



@receiver(post_save,sender=User)
def assign_role(sender,instance,created, **kwargs):
     if created:
          user_group,created=Group.objects.get_or_create(name='User')
          instance.groups.add(user_group)
          instance.save()

