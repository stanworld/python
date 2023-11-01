import subprocess
import time

def run_terraform_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    while True:
        output = process.stdout.readline()
        if process.poll() is not None:
            break
        if output:
            print(output.decode('utf-8').strip())

# Replace with the path to your Terraform directory
terraform_dir = "/home/stan/Code/python/project1/tf"

# Run 'terraform init' to initialize Terraform (if needed)
run_terraform_command(f"terraform -chdir={terraform_dir} init")

# Run 'terraform apply' to apply the changes
run_terraform_command(f"terraform -chdir={terraform_dir} apply -auto-approve")

# Wait for a while to let worker.sh finish
print("Waiting for 5 minute...\n")

time.sleep(60*5)

# Run 'terraform destroy' to destroy the resources
run_terraform_command(f"terraform -chdir={terraform_dir} destroy -auto-approve")







