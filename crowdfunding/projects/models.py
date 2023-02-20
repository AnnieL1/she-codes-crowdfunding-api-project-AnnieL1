from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model() 

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal = models.IntegerField()
    stretchgoal_trigger = models.IntegerField()
    image = models.URLField()  #hard to store in database because there's a lot of 0s and 1s, hence we're using a URL to redirect to image
    is_open = models.BooleanField()
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True) #auto_now_add tells the backend to just auto record whatever time the command was run, rather than having to GET the time from the db and then POST the same time back to the DB
    ## owner=models.CharField(max_length=200) #need to change to Primary or Foriegn Key in future so the tables can talk to each other. The CharField class won't allow tables to talk to each other 
    favourite = models.BooleanField()
    owner = models.ForeignKey(
        User,   # we're saying there is a relo between users and projects
        on_delete=models.CASCADE,  # when user is deleted, delete all their projects as well so user PK always has projects to correspond to
        related_name='owner_projects'   # eg. ask computer to look for user1 projects and then all the projects will be shown 
    )

##attempting properties     

    def __str__(self) -> str:
        return self.title

    @property
    def total_pledge_amount(self):
        total = 0 
        for pledge in self.pledges.all():
            total += pledge.amount
        return total

    @total_pledge_amount.setter
    def total_pledge_amount(self, value):
        # Do nothing, since we don't want to allow direct modification of this property
        pass

    @property
    def funding_reached(self):
        # return self.goal <= self.total_pledge_amount
        return True if self.goal <= self.total_pledge_amount else False

    @funding_reached.setter
    def funding_reached(self, value):
        # Do nothing, since we don't want to allow direct modification of this property
        pass
    
    
class Pledge(models.Model):
    amount = models.IntegerField()
    # comment = models.CharField(max_length=200)
    anonymous = models.BooleanField()
    # is_active=models.BooleanField()
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,  #if you delete project, automatically delete all the pledges associated with the project so there are no floating pledges in the database 
        ## there's also on_update.CASCADE - this let's the pledges ID change if the project ID changes. ID shouldn't be sequential because hackers will be able to scrap people's data based on order of user's ID
        related_name='pledges', #tells Project to look for the Pledges model because it needs all the data from a certain row within Pledges database
    )
    supporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='supporter_pledges'
    )

    #attempting to limit users to only be allowed to pledge once
    # class Meta:
    #     # add a unique together constraint on project and supporter fields
    #     unique_together = ('project', 'supporter')

    def __str__(self) -> str:
        return self.project


class StretchGoals(models.Model):
    fanbased_stretchgoal = models.TextField()    
    pledge = models.ForeignKey(
        'Pledge',
        on_delete=models.CASCADE,
        related_name = 'stretch_goals'
    )
    gamer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='player_stretch_goals'
    )

    