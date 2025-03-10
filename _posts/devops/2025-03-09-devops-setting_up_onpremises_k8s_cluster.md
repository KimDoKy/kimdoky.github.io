---
layout: post
section-type: post
title: Setting Up Your Own On-Premises Kubernetes Cluster
category: devops
tags: [ 'k8s', 'cluster', 'raspberrypi' ]
---

# Setting Up Your Own On-Premises Kubernetes Cluster

This guide details how to set up an on-premises Kubernetes cluster using a Mini PC as the control plane and Raspberry Pi devices as worker nodes. By following these steps, you can create a personal Kubernetes environment for learning, testing, or small-scale projects.

---

### **1. Hardware Setup**

- **Devices**:
  - Mini PC (Ubuntu installed) x 1
  - Raspberry Pi (Raspberry Pi OS Lite installed) x 2
- **Network**:
  - Ensure all devices are connected to the same network and assign static IPs.
- **Install SSH Server and Firewall**:

```bash
# Install SSH Server
sudo apt update
sudo apt install openssh-server
sudo systemctl status ssh
sudo systemctl enable ssh

# Install UFW and allow necessary ports
sudo apt install ufw
sudo ufw allow ssh
sudo ufw allow 6443/tcp
sudo ufw reload

# Check IP address
ip a
```

---

### **2. Setting Up the Control Plane (Mini PC)**

1. **Install K3s**:

```bash
# This installs the K3s control plane and starts the Kubernetes API server.
curl -sfL https://get.k3s.io | sh -
```

2. **Retrieve Cluster Token**:

```bash
# Save this token; it will be used to join worker nodes.
sudo cat /var/lib/rancher/k3s/server/node-token
```

3. **Configure Firewall**:

```bash
sudo ufw allow 6443/tcp
sudo ufw reload
```

---

### **3. Configuring Worker Nodes (Raspberry Pi)**

#### **Pre-requisites**

- Install Raspberry Pi OS Lite.
- Enable `cgroup` memory management:

```bash
# Edit /boot/cmdline.txt or /boot/firmware/cmdline.txt
cgroup_memory=1 cgroup_enable=memory

# Reboot the device
sudo reboot
```

#### **Install Required Packages**

```bash
sudo apt update
sudo apt install iptables iptables-persistent
```

#### **Set Hostnames to Avoid Conflicts**

1. For Worker Node 1:

```bash
sudo hostnamectl set-hostname worker1
sudo nano /etc/hosts
```

2. For Worker Node 2:

```bash
sudo hostnamectl set-hostname worker2
sudo nano /etc/hosts
```

#### **Join Worker Nodes to the Cluster**

1. Worker Node 1:

```bash
curl -sfL https://get.k3s.io | K3S_URL=https://<master-node-ip>:6443 K3S_TOKEN=<your_token> sh -
```

2. Worker Node 2:

```bash
curl -sfL https://get.k3s.io | K3S_URL=https://<master-node-ip>:6443 K3S_TOKEN=<your_token> sh -
```

#### **Verify Connection**

On the control plane (Mini PC):

```bash
kubectl get nodes
```

---

### **4. Managing the Cluster from macOS**

#### **Install kubectl**

```bash
brew install kubectl
```

#### **Copy kubeconfig File**

1. Copy `k3s.yaml` from the control plane to your macOS machine:

```bash
scp ubuntu@<master-node-ip>:/etc/rancher/k3s/k3s.yaml ~/.kube/config
```

2. Update the `server` field in `~/.kube/config` to point to the control plane's IP address:

```yaml
server: https://<master-node-ip>:6443
```

3. Set proper permissions for the file:

```bash
chmod 600 ~/.kube/config
```

#### **Test Connection**

```bash
kubectl get nodes
```

- You should see all nodes in your cluster.

---

### **5. Deploying a Test Application**

Deploy an Nginx application to test your cluster:

```bash
kubectl create deployment nginx --image=nginx

# Expose it as a service on a NodePort for external access.
kubectl expose deployment nginx --type=NodePort --port=80

# Check the service details.
kubectl get services nginx

# Access it via http://<worker_node_ip>:<node_port>
```

---

### **6. Troubleshooting**

#### **Apt Update Error (Signature Verification)**

If `apt update` fails with a signature verification error, add the missing public key:

```bash
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys <NO_PUBKEY>
sudo apt update
```

#### **SSH Issues**

Verify SSH is running and listening on the correct port:

```bash
sudo ss -tulpn | grep ssh

# Restart SSH service if needed.
sudo systemctl restart sshd.service
```

#### **K3s Agent Fails to Start**

Check agent logs:

```bash
sudo journalctl -xeu k3s-agent.service

# Restart agent service.
sudo systemctl restart k3s-agent.service

# If needed, uninstall and reinstall the agent.
sudo /usr/local/bin/k3s-agent-uninstall.sh
```

---

### Conclusion

By following this guide, you’ve successfully set up an on-premises Kubernetes cluster using K3s with a Mini PC as the control plane and Raspberry Pi devices as worker nodes. You can now deploy applications and manage your cluster from your macOS machine!
