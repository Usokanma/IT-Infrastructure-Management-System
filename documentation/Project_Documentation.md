\# PROJECT DOCUMENTATION



\# IT INFRASTRUCTURE MANAGEMENT SYSTEM



\## 1. Introduction



The IT Infrastructure Management System is a Python-based desktop application developed to support the organization and management of IT infrastructure information within an organization.



The application provides a centralized platform for managing users, IT assets, network devices, technical support tickets and maintenance records. It uses an SQLite relational database to store and retrieve information.



\## 2. Problem Statement



Managing IT infrastructure records manually can lead to disorganized information, difficulty retrieving records, poor equipment tracking and delays in resolving technical issues.



The IT Infrastructure Management System was developed to provide a computerized solution for organizing IT resources and maintaining accurate technical support records.



\## 3. Aim of the Project



The aim of this project is to design and develop a computerized system for managing IT infrastructure resources and technical support activities.



\## 4. Objectives



The objectives are to:



1\. Develop a centralized IT infrastructure management application.

2\. Provide facilities for managing user information.

3\. Maintain records of IT assets and equipment.

4\. Organize network device information.

5\. Support the recording and management of technical support tickets.

6\. Maintain equipment maintenance records.

7\. Store and retrieve information using a relational database.

8\. Provide a dashboard for accessing important application sections.



\## 5. Technologies Used



The application was developed using the following technologies:



\- Python: Main programming language.

\- Tkinter: Desktop graphical user interface.

\- SQLite3: Relational database management.

\- ttk: Interface widgets and controls.

\- Python messagebox: Application notifications and alerts.



\## 6. System Requirements



\### Hardware Requirements

\- Computer system or laptop.

\- Minimum 4 GB RAM recommended.

\- Sufficient storage space for the application and database.

\- Keyboard and mouse.



\### Software Requirements

\- Windows operating system.

\- Python 3.x.

\- SQLite database support (included with Python).

\- Visual Studio Code or another suitable code editor (optional).



\## 7. System Modules



\### 7.1 Dashboard

Provides access to the major sections of the application and displays relevant management information.



\### 7.2 User Management

Allows users and staff information to be recorded and managed, including names, departments, email addresses and roles.



\### 7.3 Asset Management

Provides facilities for recording and managing IT assets, including asset names, types, serial numbers, status and assigned users.



\### 7.4 Network Device Management

Maintains information about network equipment, including device names, device types, IP addresses, locations and associated assets.



\### 7.5 Support Ticket Management

Provides facilities for recording technical issues, descriptions, priority levels, ticket status, reporting users, assigned users and related assets.



\### 7.6 Maintenance Records

Maintains records of equipment maintenance activities, including maintenance type, description, date, related asset and personnel responsible.



\## 8. Database Design



The application uses SQLite as its relational database management system.



Database location:



database/it\_support.db



Database backup:



database/it\_support\_backup.db



The database contains five main application tables.



\### 8.1 Users Table

Stores user information.



Fields:

\- user\_id (Primary Key)

\- full\_name

\- department

\- email

\- role



\### 8.2 Assets Table

Stores information about organizational IT assets.



Fields:

\- asset\_id (Primary Key)

\- asset\_name

\- asset\_type

\- serial\_number

\- status

\- assigned\_to (Foreign Key reference to users)



\### 8.3 Network Devices Table

Stores network equipment information.



Fields:

\- device\_id (Primary Key)

\- device\_name

\- device\_type

\- ip\_address

\- location

\- asset\_id (Foreign Key reference to assets)



\### 8.4 Support Tickets Table

Stores technical support requests.



Fields:

\- ticket\_id (Primary Key)

\- issue\_title

\- description

\- priority

\- status

\- reported\_by (Foreign Key reference to users)

\- assigned\_to (Foreign Key reference to users)

\- asset\_id (Foreign Key reference to assets)

\- created\_at



\### 8.5 Maintenance Records Table

Stores equipment maintenance information.



Fields:

\- maintenance\_id (Primary Key)

\- asset\_id (Foreign Key reference to assets)

\- maintenance\_type

\- description

\- maintenance\_date

\- performed\_by (Foreign Key reference to users)



\## 9. Database Relationships



The database contains the following declared foreign-key relationships:



1\. An asset can be assigned to a registered user.

2\. A network device can be associated with an asset.

3\. A support ticket can be associated with the user who reported it.

4\. A support ticket can be assigned to a user.

5\. A support ticket can be associated with an asset.

6\. A maintenance record can be associated with an asset.

7\. A maintenance record can identify the user who performed the maintenance.



These relationships support the organization of information across the different application modules.



\## 10. Installation and Execution



Follow these steps to run the application:



1\. Install Python 3.x on the computer.

2\. Copy or extract the IT\_Infrastructure\_Management project folder.

3\. Open PowerShell or Command Prompt.

4\. Navigate to the project directory.

5\. Confirm that the database folder and database file are present.

6\. Execute the following command:



python app.py



7\. The application window will open.

8\. Select the required module from the application interface.



\## 11. Application Testing



The application should be tested to verify the following:



\- Successful application startup.

\- Successful database connection.

\- Display of user records.

\- Creation and retrieval of asset records.

\- Display of network device records.

\- Recording and retrieval of support tickets.

\- Recording and retrieval of maintenance activities.

\- Correct handling of user inputs.

\- Appropriate application notifications.



Initial verification has confirmed that the application launches, the main modules are accessible and the SQLite database contains the five expected application tables.



Further functional testing should confirm the complete create, read, update and delete operations for each applicable module.



\## 12. Backup and Data Protection



The application database is stored in the database folder.



A backup copy is maintained as:



database/it\_support\_backup.db



The backup provides an additional copy of the application records and can be used for recovery when necessary.



Users should create updated backups before making significant database changes.



\## 13. Conclusion



The IT Infrastructure Management System demonstrates the application of Python programming, graphical user interface development and relational database management to a practical organizational problem.



The application provides a centralized environment for organizing users, IT assets, network devices, technical support requests and maintenance records.



The project demonstrates practical software development and database management concepts through the development of a functional desktop application.

