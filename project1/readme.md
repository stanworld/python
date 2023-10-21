## Summary

A python script that spins up a VM of a given specification, and executes another script on said VM. The script execution should be containerized. Before the script is run, given assumptions about the script’s runtime, an estimated cost will be calculated. After the script is finished, output files will be put in cloud storage. Then, after the entire execution is completed, the VM will be spun down. Finally, a text/email will be sent with a user given job name, the original estimated cost, the actual cost, and other potential useful information. The solution should be implemented as in a code as infrastructure solution.  No restrictions on cloud provider.

### 1. Create a docker image that runs a script and copys the output file to an s3 bucket
   Go to docker folder:
       `sudo docker build -t p1image .`
       `sudo docker run -e AWS_ACCESS_KEY_ID='' -e AWS_SECRET_ACCESS_KEY='' p1image`
### 2. Create a terraform configuration that runs the image in a VM instance
### 3. Use python to orchestrate the process
