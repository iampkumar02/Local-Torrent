import os
dirname = f"{os.getcwd()}/client_data"
filelist = os.listdir(dirname)
filename = "first_1.txt"
filepath = os.path.join(dirname, filename)
name = filename.split(".")

if filename in filelist:
    print(name[0])
    if name[0][-1].isnumeric():
        i = int(name[0][-1])+1
        rename = name[0].split("_")
        filename = rename[0]+"_"+str(i)+"."+name[1]
        filepath = os.path.join(dirname, filename)
        print(rename)
        with open(filepath, "w") as f:
            f.write("Yo PK")
    else:
        print("X")
else:
    with open(filepath, "w") as f:
        f.write("Yo PK")
