import json
import urllib
from django.db import models
from django.contrib.auth.models import User
from django.template import Template
from django_extensions.db.fields import UUIDField
from fastapp.utils import Connection


class AuthProfile(models.Model):
    user = models.OneToOneField(User, related_name="authprofile")
    access_token = models.CharField(max_length=72)


class Base(models.Model):
    name = models.CharField(max_length=32)
    uuid = UUIDField(auto=True)
    content = models.CharField(max_length=8192)
    user = models.ForeignKey(User, related_name='+', default=0, blank=True)

    @property
    def url(self):
        return "/fastapp/%s" % self.name

    @property
    def shared(self):
        return "/fastapp/%s/index/?shared_key=%s" % (self.name, urllib.quote(self.uuid))

    def refresh(self):
        connection = Connection(self.user.authprofile.access_token)
        template_name = "%s/index.html" % self.name
        template_content = connection.get_file(template_name)
        self.content = template_content

        # execs
        app_config = "%s/app.json" % self.name
        app_config_json = connection.get_file(app_config)
        for name, value in json.loads(app_config_json).iteritems():
            module_content = connection.get_file("%s/%s" % (self.name, value))
            app_exec_model, created = Exec.objects.get_or_create(base=self, name=name)
            app_exec_model.module = module_content
            app_exec_model.save()

    def template(self, context):
        t = Template(self.content)
        return t.render(context)

    def __str__(self):
        return "<Base: %s>" % self.name

class Exec(models.Model):
    name = models.CharField(max_length=64)
    module = models.CharField(max_length=8192)
    base = models.ForeignKey(Base, related_name="execs", blank=True, null=True)