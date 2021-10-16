import sys

import world
print("__Trying use africa submodule__")
try:
    print("Success:", world.africa)
except AttributeError:
    print("Can't import africa submodule. May be no import in world/__init__.py?")

print("__Trying import europe submodule__")
try:
    print("Success:", world.europe)
except AttributeError:
    print("Can't import europe submodule. May be no import in world/__init__.py?")

print("__Trying to import europe submodule directly from world module__")
print("Success. Automatically imported:")
from world import europe

print("__Trying use spain submodule__")
try:
    print("Success:", world.europe.spain)
except AttributeError:
    print("Can't import spain submodule. May be no import in world/europe/__init__.py?")

print("__Trying to import spain module directly from europe submodule__")
try:
    from world.europe import spain
    print("Success:", spain)
except Exception as e:
    print(e)

print("__Trying import norway module from europe submodule__")
try:
    from world.europe import norway
    print("Success:", norway)
except AttributeError:
    print("Can't import norway submodule. May be no import in world/europe/__init__.py?")

print("__Trying use zimbabwe module from africa submodule__")
try:
    print(world.africa.zimbabwe)
    print("Success:", world.africa.zimbabwe)
except:
    print("Can't import norway submodule. May be no import in world/africa/__init__.py?")

print("__Trying import zimbabwe module from africa submodule__")
try:
    from world.africa import zimbabwe
    print("Success:", zimbabwe)
except AttributeError:
    print("Can't import zimbabwe submodule.")

print("__All python import paths:__")
print(sys.path)