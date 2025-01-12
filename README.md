# Demo_system

This instance project belongs to course design. A monitoring system that includes a collection-end（PythonScript）, a back-end (Springboot+mariadb) , and a front-end(Streamlit).

The project accomplishes the following tasks:

1. Collect six types of data (wind speed, wind direction, rainfall, humidity, temperature, and air pressure) from the monitor through the serial port .
2. upload the data. Data storage, reception, and reading. 
3. Data visualization, as well as analysis, suggestions, and predictions.

The overall system architecture is mainly divided into four layers: client, front-end, back-end and collection end. Each layer collaborates with each other to jointly realize the system functions. The architecture diagram is as follows:

![image-20250103053046877](https://resource-un4.pages.dev/article/image-20250103053046877.png)

youcan view :

the back-end project in springboot_Jiang folder (task3); 

the collection-end project in monitor_app folder (task2);

the front-end project in analy_app folder(task1).



no need to try connecting the ports of springboot or database which show on architecture diagram or write in demoproject. 

Those ports are only accessable during class presentation and need to connect the wlan wifi (web) of my colleges. 
