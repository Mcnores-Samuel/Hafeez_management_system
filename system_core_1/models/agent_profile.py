#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains the AgentProfile model, which represents the agents
who facilitate the sales process. It includes fields to store relevant
information about each agent, such as their name and email address

Classes:
    - AgentProfile
"""
from django.db import models
from django.conf import settings


class AgentProfile(models.Model):
  """The Agents model represents the individuals who facilitate the sales
  process. It includes fields to store relevant information about each agent,
  such as their name and email address

  Fields:
    - user: A foreign key reference to the UserProfile of the agent.
    - is_agent: A boolean field indicating whether the user is an agent.
    - is_active: A boolean field indicating whether the user is active.
    - date_joined: The date on which the user joined the application.
    - last_login: The date on which the user last logged in to the application.

  Usage:
    The Agents model is used to manage agent accounts and permissions within
    the application. It allows for the creation of new agents, as well as the
    assignment of permissions and roles.

  Note:
    - The Agents model is a subclass of the UserProfile model, which provides
      default implementations for the fields listed above.
    - The is_agent field is used to distinguish between agents and other users.
    - The is_active field is used to distinguish between active and inactive users.
    - The date_joined field is used to track when users joined the application.
    - The last_login field is used to track when users last logged in to the application.
  """
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  is_agent = models.BooleanField(default=True)
  contact_number = models.CharField(max_length=15, blank=True, null=True)
  location = models.CharField(max_length=100, blank=True, null=True)
  longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
  latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

  class Meta:
    app_label = 'system_core_1'
    indexes = [
      models.Index(fields=['user', 'is_agent']),
    ]

  def __str__(self):
    """Return a human readable representation of the model instance."""
    return "{}".format(self.user.username)
  

class Agent_sign_up_code(models.Model):
  """The Agent_sign_up_code model represents the agent sign up codes
  which are used to create new agents. It includes fields to store relevant
  information about each agent sign up code, such as the code and the date
  on which it was created.

  Fields:
    - code: The code used to create a new agent.
    - date_created: The date on which the code was created.

  Usage:
    The Agent_sign_up_code model is used to manage agent sign up codes within
    the application. It allows for the creation of new agent sign up codes,
    as well as the assignment of permissions and roles.

  Note:
    - The Agent_sign_up_code model is a subclass of the UserProfile model, which provides
      default implementations for the fields listed above.
    - The code field is used to distinguish between agent sign up codes.
    - The date_created field is used to track when agent sign up codes were created.
  """
  code = models.CharField(max_length=15, unique=True)
  used = models.BooleanField(default=False)

  def __str__(self):
      return self.code
