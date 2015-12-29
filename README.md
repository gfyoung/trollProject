[![Build Status](https://travis-ci.org/gfyoung/trollProject.svg?branch=master)](https://travis-ci.org/gfyoung/trollProject)

[![Build status](https://ci.appveyor.com/api/projects/status/99y4rnj23e3yjo4k/branch/master?svg=true)](https://ci.appveyor.com/project/gfyoung/trollproject/branch/master)

# trollProject
Website for all wonderful things troll

# Running the Website Locally (Development Work)
* Fork and clone this repository
* Move to your trollProject/trollSite directory
* From there, run the following command: `python manage.py runserver`
  * If there are issues running this command, try changing the port number by adding `<Port Number>` to the end of the command
  * You can also change the IP address by adding `<IP Address>:<Port Number>` to the end of the command
  * Please refer to https://docs.djangoproject.com/en/1.9/ref/django-admin/ for more information otherwise
    * Note that this documentation is for Django 1.9, so make sure that you change the version number in the URL depending on which version of Django you are using
