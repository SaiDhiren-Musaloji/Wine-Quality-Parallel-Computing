# Wine-Quality-Parallel-Computing
Wine Quality Prediction 
Parallel Machine Learning on AWS

Goal
The purpose of this individual assignment is to develop parallel machine learning (ML) applications in the Amazon AWS cloud platform. The objectives are:
1.	To train an ML model in parallel on multiple EC2 instances using Apache Spark.
2.	To use Spark’s MLlib to develop and use an ML model in the cloud.
3.	To use Docker to create a container for the ML model to simplify model deployment.
Project Description
The goal is to build a wine quality prediction ML model using Spark over AWS. The model is trained in parallel using four EC2 instances. The trained model is saved and then used for wine quality prediction using a separate Spark application that runs on a single EC2 instance. The project is implemented in Java on Ubuntu Linux.
Input Datasets
•	TrainingDataset.csv: Used to train the model in parallel on multiple EC2 instances.
•	ValidationDataset.csv: Used to validate the model and tune the model parameters.
•	TestDataset.csv: Used by the instructors to test the final performance and functionality of the prediction application. This file is not shared with students.
Output
The application outputs the F1 score, a performance metric available in Spark MLlib.
Model Implementation
•	The ML model is developed using Spark MLlib.
•	Logistic regression was used initially, with additional models tested to optimize performance.
•	Classification is treated as a 10-class problem (wine scores from 1 to 10).

Implementation
GitHub Repository
Link: https://github.com/SaiDhiren-Musaloji/Wine-Quality-Parallel-Computing
Docker Hub Repository
Link: https://hub.docker.com/repository/docker/dhirennnn/wine_quality/general
Step-by-step Setup and Execution Instructions
AWS S3 Bucket Setup
1.	Access the AWS Console via AWS Academy Lab.
2.	Search for and select S3.
3.	Click Create Bucket.
4.	Enter a unique bucket name (e.g., wine-quality-dhiren).
5.	Leave other settings as default, and click Create Bucket.
6.	Upload the following files to the bucket:
o	TrainingDataset.csv
o	ValidationDataset.csv
o	wine_quality_training.py
o	wine_quality_prediction.py
 
EMR Cluster Creation
1.	In AWS Console, search for EMR and open the service.
2.	Click Create Cluster.
3.	Provide a cluster name.
4.	Set Core nodes to 1 and Task nodes to 4.
5.	Under Security, either create a new key pair or use an existing one.
6.	Set roles:
o	Service Role: EMR_DefaultRole
o	EC2 Instance Profile: EMR_EC2_DefaultRole
7.	Click Create Cluster.

Connecting to Master Node
1.	After the cluster is created, select it and choose the Master node.
2.	Use EC2 Instance Connect (SSM) or SSH with a private key:
ssh -i <your-key.pem> hadoop@<master-public-dns>
Training the Model in Spark
1.	Connect to the EMR cluster.
2.	Run the training script using Spark:
spark-submit s3://wine-quality-dhiren/wine_quality_training.py
  
Running the Prediction Script
1.	Still on the master node, execute the prediction script:
spark-submit s3://wine-quality-dhiren/wine_quality_prediction.py s3://wine-quality-dhiren/ValidationDataset.csv

Dockerized Execution (on Single EC2 Instance)
Docker Image Creation and Upload
1.	Navigate to the directory containing Dockerfile.
2.	Build the Docker image:
docker build -t wine_quality .
3.	Tag and push the image:
docker tag wine_quality dhirennnn/wine_quality:2.0
docker push dhirennnn/wine_quality:2.0
 
Run Docker Container on EC2
1.	SSH into the EC2 instance.
2.	Start and enable Docker:
sudo systemctl start docker
sudo systemctl enable docker
3.	Pull the image:
docker pull dhirennnn/wine_quality:2.0
4.	Run the container:
docker run dhirennnn/wine_quality:2.0 s3://wine-quality-dhiren/ValidationDataset.csv



![image](https://github.com/user-attachments/assets/61c1facf-6562-4230-b9e9-24f2ff3f82e8)
