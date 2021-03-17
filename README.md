# Mail Hunter Tool

MailHunter is a tool to give you access to the exchange server mails.

The tool has two modes:
  - The first is the full chain attack which take you from nothing to access the exchange server mails.
  - The second is the single task where you can run only the functions that you need.

Here we will talk about the full chain attack which contains all the tool functions.

Now we will select option 0 which will take us to the full chain attack.

![alt text](https://github.com/hassan0x/resources/raw/main/Screenshot_0.png?raw=true)

The first task will be to login to linkedin using the firefox web driver and enumerate all the company employees, you will need to enter valid linkedin account credentials, and the company linkedin ID.

You can find the linkedin company id through the following screenshot.

![alt text](https://github.com/hassan0x/resources/raw/main/Screenshot_13.png?raw=true)

Now we will take the credentials and the company ID and start the firefox web driver and authenticate to linkedin, and go to the company employees and dump all their usernames, this process may take some time depends on the number of employees, but to make this process limited by time, we set the maximum number of retured employees is 1000.

![alt text](https://github.com/hassan0x/resources/raw/main/Screenshot_1.png?raw=true)

When this task finished, the result will be written to linkedin_employees.txt file.

![alt text](https://github.com/hassan0x/resources/raw/main/Screenshot_2.png?raw=true)

The next task will be to enumerate the interal IP of the exchange mail server, and the internal company domain.

You will need to enter the exchange server of the company for example mail.company.com or webmail.company.com, then you will need to enter the company name.

the tool will take this information and trying to discover the Internal IP of the exchange server, then will trying to discover the Internal Domain based on the function of the MailSniper tool. (you will need to disable the antivirus becouse MailSniper marked as malicious)

![alt text](https://github.com/hassan0x/resources/raw/main/Screenshot_3.png?raw=true)

Then will identify the users name schema, where we will generate many common used naming schemas and trying them against the timing reponse of the exchange server to discover the valid users and from them discover the valid schema, we will just take 20 users and try on them all the naming schema.

![alt text](https://github.com/hassan0x/resources/raw/main/Screenshot_4.png?raw=true)

The tool will take some time to finish this process and after that will save the found users in a file, and from that file you can identify the used naming schema.

![alt text](https://github.com/hassan0x/resources/raw/main/Screenshot_5.png?raw=true)

Then will generate all the linkedin employess based on the identified username schema.

![alt text](https://github.com/hassan0x/resources/raw/main/Screenshot_6.png?raw=true)

Then will try to enumerate the valid employees usernames.

![alt text](https://github.com/hassan0x/resources/raw/main/Screenshot_7.png?raw=true)

![alt text](https://github.com/hassan0x/resources/raw/main/Screenshot_8.png?raw=true)

![alt text](https://github.com/hassan0x/resources/raw/main/Screenshot_9.png?raw=true)

After we identified the valid usernames we will starting password spraying attack on them, and in our case we identified one valid username and password.

![alt text](https://github.com/hassan0x/resources/raw/main/Screenshot_10.png?raw=true)

Then we will use this valid credentials to dump the global address list.

![alt text](https://github.com/hassan0x/resources/raw/main/Screenshot_11.png?raw=true)

Then we will use the dumped global address list to launch another deep password spraying attack on all the dumped users.

![alt text](https://github.com/hassan0x/resources/raw/main/Screenshot_12.png?raw=true)

Finally we successfully found 4 valid usernames and passwords, now we can login to the exchange server with these found credentials and start our post exploitation process.

Happy Hunting.
