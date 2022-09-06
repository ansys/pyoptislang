"""Create all possible nodes."""
# (c) 2021 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.
#
# Python example
#
# Try to create all actors that are available in Python and add them to the workflow


from inspect import getmembers, isclass

for actor in getmembers(actors, isclass):
    try:
        add_actor(actor[1](actor[0]))
    except:
        pass


# Try to add all custom integration plugins
for integration in actors.get_loaded_ci_plugins():
    try:
        add_actor(actors.CustomIntegrationActor(integration))
    except:
        pass


# Try to add all custom algorithm plugins
for plugins in actors.get_loaded_plugins():
    try:
        add_actor(actors.CustomAlgorithmActor(plugins))
    except:
        pass
