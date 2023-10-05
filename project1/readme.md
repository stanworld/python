## Summary
A python script that spins up a VM of a given specification, and executes another script on said VM. The script execution should be containerized. Before the script is run, given assumptions about the script’s runtime, an estimated cost will be calculated. After the script is finished, output files will be put in cloud storage. Then, after the entire execution is completed, the VM will be spun down. Finally, a text/email will be sent with a user given job name, the original estimated cost, the actual cost, and other potential useful information. The solution should be implemented as in a code as infrastructure solution.  No restrictions on cloud provider.
### Basic example
Include a basic example or links here.

### Motivation
Sample project