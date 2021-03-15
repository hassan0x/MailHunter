# Mail Hunter Tool

MailHunter is a tool to give you access to the exchange server mails.

The tool is diveded into two parts, the first is the full chain attack which take you from nothing to access the exchange server mails, the second is the single task where you can run only the functions that you need.

Here we will take the full chain attack which contains all the tool functions.

Now we will select option 0 which will take us to the full chain attack.

![alt text](https://github.com/hassan0x/resources/raw/main/Screenshot_0.png?raw=true)

The first task will be to login to linkedin and enumerate all the company employees, you will need to enter valid linkedin account credentials, and the company linkedin ID.

You can find the linkedin company id through the following picture.

![alt text](https://github.com/hassan0x/resources/raw/main/Screenshot_13.png?raw=true)

![alt text](https://github.com/hassan0x/resources/raw/main/Screenshot_1.png?raw=true)

When this task finished, the result will be written to linkedin_employees.txt file.

![alt text](https://github.com/hassan0x/resources/raw/main/Screenshot_2.png?raw=true)

The next task will be to enumerate the interal IP of the exchange mail server, and the internal company domain.

![alt text](https://github.com/hassan0x/resources/raw/main/Screenshot_3.png?raw=true)

Then will identify the users name schema, where we will generate many common used naming schemas.

![alt text](https://github.com/hassan0x/resources/raw/main/Screenshot_4.png?raw=true)

then will generate all the linkedin employess based on the identified username schema.

![alt text](https://github.com/hassan0x/resources/raw/main/Screenshot_5.png?raw=true)

then will try to enumerate the valid employees usernames.

![alt text](https://github.com/hassan0x/resources/raw/main/Screenshot_6.png?raw=true)

After we identified the valid usernames we will starting password spraying attack on them.

![alt text](https://github.com/hassan0x/resources/raw/main/Screenshot_7.png?raw=true)

and in our case we identified one valid username and password.

![alt text](https://github.com/hassan0x/resources/raw/main/Screenshot_8.png?raw=true)

then we will use this valid credentials to dump the global address list.

![alt text](https://github.com/hassan0x/resources/raw/main/Screenshot_9.png?raw=true)

then we will use the dumped global address list to launch another deep password spraying attack on all the dumped users.

![alt text](https://github.com/hassan0x/resources/raw/main/Screenshot_10.png?raw=true)

finally we successfully found 4 valid usernames and passwords, now we can login to the exchange server with these found credentials and start our post exploitation process.
Happy Hunting.
![alt text](https://github.com/hassan0x/resources/raw/main/Screenshot_11.png?raw=true)

![alt text](https://github.com/hassan0x/resources/raw/main/Screenshot_12.png?raw=true)
