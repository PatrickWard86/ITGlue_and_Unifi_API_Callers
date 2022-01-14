# Unipy_and_PyTglu
Unifi API caller and a IT Glue API caller. with a demo application that syncs devices from a site in the Unifi Controller, to an organisation in IT Glue as a configuration

Both of the API callers in this repo have standalone functionality and can be integrated as they are into any application.
You will need to add your credentials in the Config.py file. 
I have included a short script utlizing both of the callers to sync up devices from a specified site in the Unifi controller with an organisation in IT Glue as configurations.
Configuration created includes mac, IP, alias, although you would need to change the configuration type id`s to the ones specific to your IT Glue setup.
You can get your configuration type ID`s by making a call that is built into PyTGlu.py, the functions name is getConfigurationTypes().

To use the Unifi controller you create a new instance of the class and pass the credentials. then you can use it to make requests eg:
u = UniPy.Unifier(host=Config.UnifiCreds.host, port=Config.UnifiCreds.port, user=Config.UnifiCreds.username, password=Config.UnifiCreds.password)

then the line
u.getSites
Will return a list of dicts contailing all the sites on the controller.

The IT Glue API caller works in much the same way.

Please feel free to make additions to the codebase and comment it all the way.
