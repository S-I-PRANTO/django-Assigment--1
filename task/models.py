from django.db import models

class Category(models.Model):
    Event_Categorys=models.CharField(max_length=250)
    description=models.TextField()


class Event(models.Model):
    Event_Name=models.CharField(max_length=200)
    description=models.TextField()
    data=models.DateField()
    time=models.TimeField()
    location=models.CharField(max_length=150)
    category=models.ForeignKey(Category,on_delete=models.CASCADE ,related_name="event")

    def __str__(self):
        return self.Event_Name
    
class Participant(models.Model):
    Participant=models.CharField(max_length=250)
    description=models.TextField()
    Event=models.ManyToManyField(Event,related_name="participant", blank=True)



    # 

# from datetime import date, time
# from task.models import Category, Event, Participant 

# cat1 = Category.objects.create(Event_Categorys="Fasting", description="Fasting related events")
# cat2 = Category.objects.create(Event_Categorys="Ramadan", description="Ramadan events")
# cat3 = Category.objects.create(Event_Categorys="Eid Festival", description="Eid celebration events")
# cat4 = Category.objects.create(Event_Categorys="Tech Talk", description="Technology events")
# cat5 = Category.objects.create(Event_Categorys="Workshop", description="Educational workshops")


# event1 = Event.objects.create(
#     Event_Name="Ramadan Iftar Party",
#     description="Community Iftar gathering",
#     data=date(2026, 2, 10),
#     time=time(6,30),
#     location="Sirajganj",
#     category=cat1
# )

# event2 = Event.objects.create(
#     Event_Name="Eid Festival",
#     description="Eid celebration with cultural programs",
#     data=date(2026, 3, 15),
#     time=time(9,0),
#     location="Sirajganj",
#     category=cat3
# )

# event3 = Event.objects.create(
#     Event_Name="Tech Talk 2025",
#     description="Latest trends in AI and ML",
#     data=date(2025, 12, 20),
#     time=time(14,0),
#     location="Dhaka",
#     category=cat4
# )

# event4 = Event.objects.create(
#     Event_Name="Python Workshop",
#     description="Hands-on Python training",
#     data=date(2026, 1, 5),
#     time=time(10,0),
#     location="Dhaka",
#     category=cat5
# )

# event5 = Event.objects.create(
#     Event_Name="Ramadan Charity Event",
#     description="Fundraising for community support",
#     data=date(2026, 2, 20),
#     time=time(17,30),
#     location="Chittagong",
#     category=cat2
# )

# event6 = Event.objects.create(
#     Event_Name="Eid Parade",
#     description="City parade for Eid celebration",
#     data=date(2026, 3, 16),
#     time=time(11,0),
#     location="Dhaka",
#     category=cat3
# )

# event7 = Event.objects.create(
#     Event_Name="AI Seminar",
#     description="Seminar on AI applications",
#     data=date(2025, 12, 22),
#     time=time(15,0),
#     location="Khulna",
#     category=cat4
# )

# event8 = Event.objects.create(
#     Event_Name="Web Dev Bootcamp",
#     description="Learn web development from scratch",
#     data=date(2026, 1, 10),
#     time=time(9,0),
#     location="Dhaka",
#     category=cat5
# )

# event9 = Event.objects.create(
#     Event_Name="Fasting Awareness Session",
#     description="Health benefits of fasting",
#     data=date(2026, 2, 5),
#     time=time(16,0),
#     location="Rajshahi",
#     category=cat1
# )

# event10 = Event.objects.create(
#     Event_Name="Ramadan Community Talk",
#     description="Discussion on Ramadan practices",
#     data=date(2026, 2, 15),
#     time=time(18,0),
#     location="Sylhet",
#     category=cat2
# )


# p1 = Participant.objects.create(Participant="MD. Shariful Islam Pranto", description="Interested in Islamic events")
# p2 = Participant.objects.create(Participant="MD. Mehedi Hasan", description="Loves festivals and community events")
# p3 = Participant.objects.create(Participant="Ayesha Rahman", description="Tech enthusiast")
# p4 = Participant.objects.create(Participant="Rahat Hossain", description="Python developer")
# p5 = Participant.objects.create(Participant="Fatema Akter", description="Interested in charity events")


# p1.Event.add(event1, event2, event5, event9)
# p2.Event.add(event2, event6, event10)
# p3.Event.add(event3, event7)
# p4.Event.add(event4, event8)
# p5.Event.add(event5, event10)
