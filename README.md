# Learning notes

## k8s in action
Learning notes about k8s in action

### namespace and cgroup
- namespace is used isolate processes
- since parent process and child process are in the same pid namespace, they can see similar number of processes
- ps -ef to list all processes
- echo $$ to list current process pid
- echo $PPID to list parent process pid
- ls -l /proc/14356/ns  to list pid 14356 namespaces
- /sys/fs/cgroup is the place where user space and kernel interact about cgroup settings
- use unshare command to specify the namespace that a child process doesn't want to share with its parent.
- dmesg -T | grep "oom" is used to check kernel message about out of memory error