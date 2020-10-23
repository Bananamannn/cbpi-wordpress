from modules import cbpi
from thread import start_new_thread
import time 
import logging

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts

DEBUG = False
Wordpress_Domain = None
Wordpress_Username = None
Wordpress_Password = None
Wordpress_Tag = None
Wordpress_Category = None

def log(s):
    if DEBUG:
        s = "IOT: " + s
        cbpi.app.logger.info(s)

def WordpressDomain():
    global Wordpress_Domain
    Wordpress_Domain = cbpi.get_config_parameter("Wordpress_Domain", None)
    if Wordpress_Domain is None:
        log("Init Wordpress Config Domain name")
        try:
            cbpi.add_config_parameter("Wordpress_Domain", "", "text", "Wordpress base domain site address. E.g. https://yourdomainname.wordpress.com/")
        except:
            cbpi.notify("Wordpress Error", "Unable to update domain name parameter", type="danger")

def WordpressUsername():
    global Wordpress_Username
    Wordpress_Username = cbpi.get_config_parameter("Wordpress_Username", None)
    if Wordpress_Username is None:
        log("Init Wordpress Config Username")
        try:
            cbpi.add_config_parameter("Wordpress_Username", "", "text", "Wordpress Site Username")
        except:
            cbpi.notify("Wordpress Error", "Unable to update username parameter", type="danger")

def WordpressPassword():
    global Wordpress_Password
    Wordpress_Password = cbpi.get_config_parameter("Wordpress_Password", None)
    if Wordpress_Password is None:
        log("Init Wordpress Password")
        try:
            cbpi.add_config_parameter("Wordpress_Password", "", "text", "Wordpress user password")
        except:
            cbpi.notify("Wordpress Error", "Unable to update config parameter", type="danger")
            
def WordpressTag():
    global Wordpress_Tag
    Wordpress_Tag = cbpi.get_config_parameter("Wordpress_Tag", None)
    if Wordpress_Tag is None:
        log("Init Wordpress Tag")
        try:
            cbpi.add_config_parameter("Wordpress_Tag", "", "text", "Wordpress update tag")
        except:
            cbpi.notify("Wordpress Error", "Unable to update config parameter", type="danger")

def WordpressCategory():
    global Wordpress_Category
    Wordpress_Category = cbpi.get_config_parameter("Wordpress_Category", None)
    if Wordpress_Category is None:
        log("Init Wordpress Category")
        try:
            cbpi.add_config_parameter("Wordpress_Category", "", "text", "Wordpress update category")
        except:
            cbpi.notify("Wordpress Error", "Unable to update config parameter", type="danger")
            
@cbpi.initalizer(order=9001)
def init(cbpi):
    cbpi.app.logger.info("Wordpress plugin Initialize")
    WordpressDomain()
    WordpressUsername()
    WordpressPassword()
    WordpressTag()
    WordpressCategory()

@cbpi.backgroundtask(key="wordpress_task", interval=300)
def wordpress_background_task(api):
    log("IOT background task")

    data1= "{"
    for key1, value in cbpi.cache.get("sensors").iteritems():
        data1 += ", " if key1 >1 else ""
        data1 += "\"%s\":%s" % (value.name, value.instance.last_value)
    data1 += "}"
    
    data2= "{"
    for key2, value2 in cbpi.cache.get("actors").iteritems():
        data2 += ", " if key2 >1 else ""
        data2 += "\"%s\":%s,%s" % (value2.name, value2.state, value2.power)
    data2 += "}"
    
    log("Wordpress Update")
    
    blog = Client(Wordpress_Domain + "xmlrpc.php", Wordpress_Username, Wordpress_Password)
    post = WordPressPost()
    # Create a title with some simple styling classes
    post.title = time.strftime("%y/%m/%d %H:%M:%S", time.localtime())
    post.content = data1 + "<br />" + data2
    post.terms_names = {
            'post_tag': [Wordpress_Tag],
            'category': [Wordpress_Category],
    }
    post.id = blog.call(posts.NewPost(post))
    # Always publish these posts
    post.post_status = 'publish'
    blog.call(posts.EditPost(post.id, post))
