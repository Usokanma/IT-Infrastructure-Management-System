# PROJECT REPORT
## IT INFRASTRUCTURE MANAGEMENT SYSTEM

### 1. INTRODUCTION
The IT Infrastructure Management System is a desktop-based application developed to improve the organization and management of IT infrastructure records.

### 2. AIM AND OBJECTIVES
The aim is to develop a computerized IT infrastructure management application.

Objectives include:
- Managing user information.
- Recording IT assets.
- Managing network devices such as routers and switches.
- Organizing technical support tickets.
- Maintaining maintenance records.
- Storing information in a structured database.

### 3. SYSTEM DEVELOPMENT TOOLS
Programming Language: Python
Database: SQLite
Application Type: Desktop application

### 4. SYSTEM DESCRIPTION
The application contains modules for Dashboard and Reports, User Management, Asset Management, Network Devices, Support Tickets and Maintenance Records.

The application stores its records using an SQLite database located in the database folder.

### 5. SYSTEM IMPLEMENTATION
The application is launched using the command:

python app.py

The application provides a graphical interface through which users can access its management modules.

### 6. DATABASE MANAGEMENT
The system uses the database file it_support.db. A backup copy named it_support_backup.db is also maintained.

7. TESTING AND VERIFICATION

The IT Infrastructure Management System underwent application and database verification.

The following tests were performed:

- Successful application startup.
- Successful connection to the SQLite database.
- Verification of all five database tables.
- Verification of seven declared foreign-key relationships.
- Successful database integrity check.
- Verification of user records against the application interface.
- Verification of asset records against the application interface.
- Verification of network device records against the application interface.
- Verification of support ticket records against the application interface.
- Verification of maintenance records against the application interface.
- Successful creation, retrieval, updating and deletion of a user record.
- Verification of the dashboard.
- Verification and synchronization of the main database and backup database.

The final database verification confirmed that the main database and backup contained matching records across all five application tables.

These tests demonstrated the application's basic functionality and the integrity of its database.
8. CONCLUSION

The IT Infrastructure Management System was successfully developed to improve the management and monitoring of IT infrastructure records. The application provides a centralized platform for managing users, IT assets, network devices, support tickets, and maintenance records.

The system uses Python and SQLite to store and manage information efficiently. Testing confirmed that the major functionalities operate as expected and that records are maintained in the database.

The project demonstrates how a computerized system can simplify IT infrastructure management, improve record organization, and support better technical operations.

9. RECOMMENDATIONS

The following improvements are recommended for future development of the system:

1. User authentication should be introduced to improve system security.
2. Automated database backup should be implemented to prevent data loss.
3. The system could be expanded to support multiple users.
4. Additional reporting features could be introduced to provide more detailed information about IT assets and maintenance activities.
5. The application could be upgraded to a web-based platform for easier access across different devices.
