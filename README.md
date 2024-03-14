# CBACK TEST:
This repository is submission for evaluation test for CBACK(CERN) gsoc 2024  

Completed Task:  
Challange 1 is completely done  
Bonus functionalities of recurring tasks and APIs to interact with service  

Challange 2 is partially completed  
Dockerization done  
Kubernetes deployment yaml files and job files  

Task Left:  
Testing of Kubernetes Part   
Implementation of Helm Charts  
Bonus Part of Challange 2    


These are list of commands to run the service in docker:  

``` cd cback ```  
``` docker-compose up --build```  
``` docker-compose exec app flask db upgrade```  

then call this API to start the scheduler:   
http://127.0.0.1:5000/start  

Other APIs for CRUD operations:  

Create Task :  
http://127.0.0.1:5000/tasks/create  

Example Body:   
{
    "task_name" : "task2",  
    "scheduled_execution_time" : "2024-03-13T15:30:00Z",  
    "task_type" : "daily"  
}

Get All-Task: 
http://127.0.0.1:5000/tasks/detail

Get Specific Task:
http://127.0.0.1:5000/tasks/get/<task_id>  

Update Task:
http://127.0.0.1:5000/tasks/update/<task_id>

Delete Task:
http://127.0.0.1:5000/tasks/delete/<task_id>







