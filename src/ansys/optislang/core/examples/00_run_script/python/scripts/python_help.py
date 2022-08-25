"""Return info about actors."""
###############################################################################
# (c) 2021 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.

# See which nodes are available in python console
###############################################################################
for i in actors.__dict__:
    print(i)

# print help for all actors
help(actors)

# print help for sensitivity actor
help(actors.SensitivityActor)
