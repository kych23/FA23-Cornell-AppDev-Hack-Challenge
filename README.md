# hack-challenge
FA23 Cornell AppDev Hack Challenge

Latte Link:
A scheduling app that allows you to connect with coffee chatters and arrange coffee chats from a range of Cornell organizations.

![image](https://github.com/kych23/hack-challenge/assets/108193938/edd6c7e9-8aa2-49ad-88f4-0785d33cd6f3)
![image](https://github.com/kych23/hack-challenge/assets/108193938/2addf3e2-8aef-4f4f-b259-5be528972687)
![image](https://github.com/kych23/hack-challenge/assets/108193938/d8f58d77-3904-4f55-828d-07920bbdcec2)

We noticed that when people are trying to coffee chat with others, in particular for club recruitment, they can face difficulties because the system for scheduling chats varies between organizations and coordinating schedules is tedious. With this people problem in mind, we decided to create “Latte Link,” a coffee chat scheduling app where people can see information about current members in an organization as well as the person’s availability.

Backend:
The backend API has many GET, POST, and DELETE requests for our many databases, which include users, organizations, coffee chat requests, orgaization requests, etc. For example, we have a get all users, post new user, and delete user request. Our tables have many interconnecting relationships, such as a many to many relationship between users and organizations, or a one to many relationship between coffee chat requests and user.





