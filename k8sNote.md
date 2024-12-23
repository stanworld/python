# K8s NOTEs
## pod template with emptyDir and multiple lines of args
```
apiVersion: v1
kind: Pod
metadata:
  name: time-check
  namespace: datacenter
spec:
  containers:
  - name: time-check
    image: busybox:latest
    command: ["/bin/sh", "-c"]
    args:
      - |
        while true; do
          date >> /opt/itadmin/time/time-check.log;
          sleep $(TIME_FREQ);
        done
    env:
    - name: TIME_FREQ
      valueFrom:
        configMapKeyRef:
          name: time-config
          key: TIME_FREQ
    volumeMounts:
    - name: log-volume
      mountPath: /opt/itadmin/time
  volumes:
  - name: log-volume
    emptyDir: {}

```
##
kubectl get pod <pod-name> -n <namespace> -o yaml > pod-config.yaml

##

kubectl create deployment --image=nginx nginx --dry-run=client -o yaml > nginx-deployment.yaml

kubectl taint nodes node1 color=blue:NoSchedule 

kubectl taint nodes node1 key1:NoSchedule-

## Label selector OR, AND operation
kubectl get pods -l 'environment in (production, staging)'

kubectl get pods -l environment=production,tier=frontend

## Check kubelet configuration
sudo systemctl cat kubelet

