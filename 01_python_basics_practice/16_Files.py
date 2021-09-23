# there is no task link
import os
files = os.listdir(os.getcwd())
files_count = len(files)
print(files)

print(f"Here you have {files_count} files:")
print("====================================")
for file in files:
    if os.path.isfile(os.path.join(os.getcwd(),file)):
        print(file)
print("====================================")
choise = int(input("Which file you want to see? (type a number):"))
if choise <= files_count:
    try:
        with open(os.path.join(os.getcwd(), files[choise-1])) as f:
            print(f.read())
    except PermissionError:
        print("Sorry, you don't have permission to read this file =(")
    except Exception as e:
        print(e)
else:
    print("Probably wrong file number. Shut down...")




