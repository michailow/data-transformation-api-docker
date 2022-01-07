# Data transormation API on Docker



Data transformation API in Docker Container with Python, Flask and MySQL.
____
### Overview of the data pipeline
![dashmote_aws](https://user-images.githubusercontent.com/53381140/145751154-2b38fb75-8176-4a47-b92b-163934e4b804.png)

For clarity, I have divided the entities into three layers:<br>
Control layer, with triggers to control workflow.<br>
Processing layers, with transformations and data checking.<br>
The data layer, where we store data.<br>

(1) First of all, we have the data scrapper that collection data (JSON, HTML, and Image files) to S3.<br>
(2) After data is put into S3, we have AWS Lambda with a trigger function that detects new data in S3.<br>

(3) When new data is detected, Lambda triggering API in Docker that takes data (4) from S3, transforming it and putting (5) into AWS RDS.<br>

(6) Then, some triggertells the Preprocessing step to take data, (7) normalize it, and put (8) into AWS RDS table with normalized data. For this purpose, we can use AWS Lambda that does this at some interval, or developers manually trigger that process.<br>

(6.1) We have another option. After certain conditions (for example if new data landing in AWS RDS)<br>

(9) Then we have the next trigger to check data before putting it (10) into Delivery DB. For that, we can use AWS Lambda that triggers after certain conditions, or developers manually start that after checking data quality. <br>
____
### Question 1
1. I. For <b>raw files from the sourcing</b> (such as JSON, HTML and Image files) we need cloud storage. AWS S3 is well-suited for this.<br>
II. Then that, we need <b>transrofm data in a structured way</b>. After transformation, we need to upload data into relational DB. AWS RDS is a good option for this.<br>
III At <b>preprocessing</b> step we apply some some <b>custom processes</b>. Data is in relational form, so we use AWS RDS.<br>
VI. Then, we can upload data to <b>delivery database</b>. Data is relational. We use AWS RDS for this.<br>
2. After all transformation data in relational form. AWS RDS provides cost-efficient and resizable capacity while automating time-consuming administration tasks such as hardware provisioning, database setup, patching, and backups. This is a good option for our data. 
3. Pandas .to_sql can handle DB modeling on it own. Moreover, this is not final step, we will have more transformations. Data modeling consuming a lot of time, so I decided that this is not a priority, given that Pandas doing this totaly fine.

4. AWS Lambda is a serverless, event-driven compute service that lets us run code. We can trigger Lambda from over 200 AWS services, that makes it a good choise for this king of operations. First instance (AWS Lambda) automaticly triggers when new appears in S3. <br>
We can use same approach for other processing, for example triggering it after new data arriver or at time interval. Or we can trigger in mannauly. So I left names as trigger 1 and trigger 2.
____
### Question 2

2. As a DE, I want to write clear documentation on what queries I used, which technologies I
implemented and why I made those choices;<br>
First of all, we need to implement some API. So I used Flash Python libraly because it great for these tasks and quite simple.<br>
Data processing and quering made in Python wtih Pandas and sqlalchemy libraly. For me it is comfortable to keep all my operations in Python code.<br>
After that, I Dockerrized app. And write YAML file to compose to it with MySQL server. MySQL is easier to use than Postgres, so this is my choise for this task.<br>

_____
### Docker start
To start the app launc command "docker compose up"<br>
![image](https://user-images.githubusercontent.com/53381140/147183498-276cc1c1-2a8d-4e94-895d-d1de9e77e2e5.png)<br>
We can see that Images builded after we get respocne from Flask:<br>
![image](https://user-images.githubusercontent.com/53381140/147183568-5fbe573d-4977-41ae-8b4c-537f085e2fcf.png)<br>
_____
### Testing
Test that app is running.<br>
Or app will be running on http://127.0.0.1:80 <br>
Try to connect with Postman:<br>
![image](https://user-images.githubusercontent.com/53381140/147183645-89054d31-ebd2-4eb3-8758-7f1098a67fb0.png)<br>
Server running<br>
Test connection with DB<br>
![image](https://user-images.githubusercontent.com/53381140/148603068-1d0d1982-a64b-4057-9649-cd991e4bc58b.png)<br>
Web Server working properly.

