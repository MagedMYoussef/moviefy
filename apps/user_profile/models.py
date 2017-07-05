from django.db import models

class UserDetails(models.Model):
    username = models.CharField(max_length=100)
    avatar_url = models.CharField(max_length=5000)
    user_tweets = models.CharField(max_length=10000)

    def __str__(self):
        """
        String to represent the Model object
        """
        return (self.username, self.avatar_url)