Messages in a bottle.py
=====

About
----
Messages in a bottle.py is a message board engine written using bottle.py webframework. It's targeted at small teams that would like to have their discussions organized threads and categories, yet fell like PHPBB message boards are to complex for their needs. Or just don't want to use PHP.

While creating MIAB.py I decided to mostly use libs and modules I haven't previously used, so that I could learn some new tools of trade. I guess that's the real reason I started this project :)  


Features 
---
None for now :(  

To do
--
There's a lot to do! To give You some ideas about what's planned:
 
* notification system - yes, I get it, people now want to see little icon with number of unread nessages 
* Facebook/Google auth integration - another must have i contemporary apps
* admin panel - nothing as fancy as django admin panel... I mean I'm just one man :) 
* moderation tools
* basic search engine
* grouping threads in categories and subcategories
* looooots of customization options. My idea is, that user should have possibility of customizing everything. And by everything I really mean **everything** So yeah... there will be some settings ;) 


Requirements
--
 
**python 2.7 stuff:**

* **bottle.py** - web framework, does most of the work
* **WTForms** - form handling and validation
* **peewee** - ORM, decided to use something lighter than SQLAlchemy
* **beaker** - for session management
* **PIL** - some minor avatar editing, resizing etc.
* **passlib** - used in auth framework

**other stuff:**

* SQLite3 database
* AngularJS
* Botstrap 3.0