#coding : utf -8
  
import os,sys,subprocess,random,time

os.system("source /etc/apache2/envvars")
os.system("clear")

class Fore:
    GREEN="\u001b[32;1m"
    BLUE="\u001b[34;1m"
    YELLOW="\u001b[33;1m"
    RED="\u001b[31;1m"
    RESET="\u001b[0m"

if os.getuid() != 0:
    print(Fore.RED + "\tSorry, you have to run this as root :(" + Fore.RESET)
    sys.exit(0)

cwd=os.getcwd()

print(Fore.GREEN + "\tWelcome to my program, allowing you to change apache2 root (LINUX ONLY) ! enjoy")
print(Fore.RED + "\n\t\tMade by <3 by McPqndq (bibivilleneuve11@gmail.com)")
print(Fore.BLUE + "\n\n\t\t\t[PRESS ENTER TO CONTINUE]")
print(Fore.GREEN + "\n\n\n\nDonate :(my monero/xmr adress) : 49KHKsubi9dWyysLYVo8oNS82iKMbtXc4axhWAi7bkPadQbF9BUN5e4FeHtgSH7gv9dBHEqZibswED7etoBreBLFTEAQWyu" + Fore.RESET)
input("")



delete=""
while delete.lower()!="y" and delete.lower()!="n":
    os.system("clear")
    print(Fore.YELLOW + "Do you want to delete already existing available sites ? (Y/N)")
    delete=input("\n>>> ")

if delete.lower()=="y":
    os.chdir("/etc/apache2/sites-available")
    files = [f for f in os.listdir(".") if os.path.isfile(os.path.join(".", f))]
    for el in files:
        if el!="000-default.conf":
            os.remove(el)

os.system("clear")
os.chdir(cwd)


continuer=""
while continuer.lower()!="y":
    os.system("clear")
    print(Fore.GREEN + "Enter new apache2 root path :")
    newDir=input(Fore.YELLOW + "\n\n>>> ")

    if os.path.exists(newDir)==False:
        continuer=""
        while continuer.lower()!="y" and continuer.lower()!="n":
            os.system("clear")
            print(Fore.RED + "\tWarning ! The choosed path doesn't exist !\n\tDo you still want to continue ? (Y/N)")
            continuer=input(Fore.YELLOW + ">>> ")
    else:
        continuer="y"


with open("default_apache2.conf","r") as default:
    new_config_file=""
    for count,line in enumerate(default):
        if "DocumentRoot" in line:
            new_config_file+="\n\tDocumentRoot " + newDir
        else:
            new_config_file+=line

os.chdir("/etc/apache2/sites-available")

random_name = "new_root_" + str(random.randrange(10000,100000)) + ".conf"

with open(random_name,"w") as nfile:
    nfile.write(new_config_file)


os.chdir(cwd)

with open("defaultconf.conf","r") as deconf:
    dec=""
    for count,line in enumerate(deconf):
        if "NEWDIR" in line:
            dec+=line.replace("NEWDIR",newDir)
        else:
            dec+="\n" + line

with open("apache2.conf","r") as conf:
    new_apache2_conf=""
    first=True
    for count,line in enumerate(conf):
        if "</Directory>" in line:
            if first==True:
                new_apache2_conf+="\n" + line + "\n"
                new_apache2_conf+=dec
                first=False
            else:
                new_apache2_conf+="\n" + line
        else:
            new_apache2_conf+=line

os.chdir("/etc/apache2")
os.remove("apache2.conf")

with open("apache2.conf","w") as apache2conf:
    apache2conf.write(new_apache2_conf)

os.chdir("/etc/apache2/sites-available")

print(Fore.RESET)

null=open(os.devnull,"w")

print(Fore.GREEN + "\nDisabling enabled sites...")
time.sleep(1)
output=subprocess.call("a2dissite *",shell=True,stdout=null,stderr=null)
print("Enabling new site...")
time.sleep(1)
output=subprocess.call("a2ensite " + random_name,shell=True,stdout=null,stderr=null)
print("Restarting apache2 server...")
time.sleep(1)
output=subprocess.call("systemctl restart apache2",shell=True,stdout=null,stderr=null)
print("\nDone ! apache2 root has been successfully changed !\n" + Fore.RESET)

os.chdir(cwd)
