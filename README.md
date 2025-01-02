# Demo_system
This instance project belongs to course design. A monitoring system that includes a collection-end（PythonScript）, a back-end (Springboot+mariadb) , and a front-end(Streamlit).

The project accomplishes the following tasks:

1. Collect six types of data (wind speed, wind direction, rainfall, humidity, temperature, and air pressure) from the monitor through the serial port .
2. upload the data. Data storage, reception, and reading. 
3. Data visualization, as well as analysis, suggestions, and predictions.

The overall system architecture is mainly divided into four layers: client, front-end, back-end and collection end. Each layer collaborates with each other to jointly realize the system functions. The architecture diagram is as follows:

![image-20250103053046877](https://resource-un4.pages.dev/article/image-20250103053046877.png)



