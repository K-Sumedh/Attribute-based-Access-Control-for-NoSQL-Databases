# Attribute-based-Access-Control-for-NoSQL-Databases
NoSQL databases have recently gained popularity due to their capacity to efficiently manage large amounts of unstructured data. Role-based Access Control (RBAC) was employed in the majority of these databases. Permissions are associated with roles in role-based access control (RBAC), and users are made members of roles, thereby receiving the roles’ permissions. However, RBAC has certain restrictions, such as the inability to create rules utilising unknown, the fact that permissions may only be applied to roles rather than objects, and so on. The high flexibility and dynamic nature of Attribute-Based Access Control (ABAC) has been frequently praised. An strategy for integrating ABAC into NoSQL databases, notably MongoDB, that normally only support Role-Based Access Control, is provided to overcome these limitations (RBAC). The implementation and performance results for ABAC in MongoDB are also reviewed, with the emphasis on how it can be used in other databases.

This project focuses on addressing the challenge of integrating ABAC into NoSQL
databases in particular focused on MongoDB since it is one of the most popular NoSQL databases.To discuss an implementation enhancing MongoDB’s underlying
Role-Based Access Control (RBAC) system with attributes and dynamic
assignments. The system created should be such as it can be integrated easily
into any MongoDB server with no additional query overhead.


Files: 
source\Algorithm.py : Python Implementation of the algorithm to convert ABAC policies to RBAC policies.
source\driver.py: Main program to execute.
212IS012_Db_report.pdf : Report for this project
