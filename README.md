# API Data Ingestion and Analysis
<p align="justify">
In this project, CDK stack code, implemented in Python (runtime: 3.7) is used to deploy various AWS resources and techniques which takes in api data from the website https://openweathermap.org/ using a secret API key in the JSON format.
The JSON file is then preprocessed using a lambda function and stored in an S3 bucket. Another lambda function is used which takes in this stored JSON file and converts it into a Quicksight data-source CSV file. A trigger is set on this lambda function
to automatically get invoked whenever an object is created into the S3 bucket mentioned earlier. Using a manifest file placed inside the same s3 bucket and the CSV file output from the second lambda function, detailed dashboards and analysis are carried out
using Quicksight. The process diagram is shown below:
</p>

![Process Architecture](architecture.png)

<ul style="list-style-type:circle">
  <li><b>Step 1:<b> <br> The API data account is set up with a secret API key.</li>
  <li>Step 2: <br> API endpoint url is used with the corresponding API key stored in secrets manager by a lambda function which preprocesses the ingested data and converts it into a suitable JSON file. EventsBridge is set up along with this function
  for invocation daily to have the latest data.</li>
  <li>Step 3: <br> The output JSON file from the lambda function is stored into an S3 bucket.</li>
  <li>Step 4: <br> Another lambda function is set up attached with a trigger which invokes the lambda function on object creation into the previously mentioned S3 bucket. This lambda function takes in the generated API data JSON file and converts 
  it into a processed CSV file suitable for input as a dataset for Quicksight analysis.</li>
  <li>Step 5: <br> The CSV file output from the second lambda function along with a JSON manifest file stored inside the mentioned S3 bucket are used to set up a dataset source for analysis with Quicksight.</li>
  <li>Step 6: <br> Detailed analysis and dashboards are created using Quicksight and shared.</li>
</ul>
