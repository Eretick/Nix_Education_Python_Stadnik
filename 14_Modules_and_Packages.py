# task from https://www.learnpython.org/en/Modules_and_Packages
import re
re_list = dir(re)
find_members = [i for i in re_list if "find" in i.lower()]
find_members.sort()
print(find_members)
