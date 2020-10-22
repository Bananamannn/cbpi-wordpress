# cbpi-wordpress
## Introduction
CraftBeerPi Plugin to upload data to Wordpress website

## Required packages to install:
- `sudo apt-get install python` Installing python3 (if not available, e.g. in Raspian Lite)
- `sudo apt-get install python-pip` Installing pip (if not available)
- `sudo pip2 install python-wordpress-xmlrpc` The WordPress XML-RPC API

## Usage
1. Install repo packages listed above
2. Install plugin via either the Plugins section in Craftbeerpi (hopefully done)
3. Update the parameters listed below with required values
- **Wordpress_Domain** is your base wordpress site address. E.g "https://yourdomainname.wordpress.com/"
- **Wordpress_Username** is a Wordpress username to post data as  (must be an author)
- **Wordpress_Password** is your wordpress password
- **Wordpress_Tag** is a tag which is appended to each post from CraftBeerPi
- **Wordpress_Category** is a category which is appended to each post from CraftBeerPi
4. Restart CraftBeerPi & have a beer :)

## Credits
- Marcel https://github.com/suterma/WeatherPress
- Atle https://github.com/aravndal/ThingSpeak
