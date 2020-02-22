# OpenCue GKE sandbox environment

The GKE sandbox environment provides a way to run a test OpenCue deployment on Google
Kubernetes Engine. You can use the test deployment to run small tests or development
work, then scale the GKE node pools to meet production needs.

1.  Create a GKE Cluster from the GKE console.
    *  https://cloud.google.com/kubernetes-engine/docs/how-to/creating-a-cluster
    *  Give it a name
    *  Pick a Zone near you e.g. 'us-west1-b'
    *  Use n1-standard-2 or bigger (ensures no shared cores)
    *  Click 'Create'

1.  Create a rqd node pool
    *  Select your cluster in the GKE console
    *  Click 'Add Node Pool'
    *  Set name to 'rqd-pool'
    *  Click on 'More Options'
    *  Set machine type to 'n1-standard-2' or bigger
    *  Enable 'Set access for each API'
       *  Set 'Storage' to 'Full' (necessary for gcsfuse)
    *  Click 'Save'

1.  Wait for cluster to be ready
    *  GKE will probably upgrade the master on a newly created cluster and prevent you
       from connecting for ~10 min.
    *  For demos it's good to have a cluster already configured and ready to go so you
       can skip this step.
       
1.  Apply kube configs
    *  Connect to your cluster
    *  Using the GKE console:
       *  From the GKE console, 'Clusters' page
       *  Click 'Connect' button for your cluster
       *  Copy and run the 'gcloud' command
    *  Apply the configs from the repo root directory
       -  Apply the db config, volume configs, and security policy

          ```
          kubectl apply \
            -f kubernetes/manifests/production/postgres-configmap.yaml \
            -f kubernetes/manifests/production/db-claim0-persistentvolumeclaim.yaml \
            -f kubernetes/manifests/production/privileged-policy.yaml
          ```

       -  Apply the service configs

          ```
          kubectl apply \
            -f kubernetes/manifests/production/db-service.yaml \
            -f kubernetes/manifests/production/cuebot-service.yaml \
            -f kubernetes/manifests/production/rqd-service.yaml`
          ```

       - Create the DB deployment

         ```
         kubectl apply -f kubernetes/manifests/production/db-deployment.yaml
         ```

       - Create the Cuebot deployment (Runs the migrations as init container)

         ```
         kubectl apply -f kubernetes/manifests/production/cuebot-deployment.yaml
         ```

       - Create the RQD deployment

         ```
         kubectl apply -f kubernetes/manifests/production/rqd-deployment.yaml
         ```

    *  View the kubernetes resources that were created:

       ```
       kubectl get services
       kubectl get deployments
       kubectl get pods
       ```

1.  Start gRPC port forwarding to Cuebot
    * From GKE cluster, select 'Services & Ingress'
    * Click on the 'cuebot' service
    * Click on 'Port forwarding' for port 8443.
    * Copy and paste command into a shell and run, make sure to change the ports to '8443:8443'

1.  Run the client tools like normal from your workstation

    ```
    source venv/bin/activate
    export CUEBOT_HOSTS=localhost
    cuegui
    ```

1.  View hosts in CueGUI. You should have 1 host available.

1.  Scale the RQD replicas
    * From the GKE console, select 'Workloads'
    * Click on 'rqd' workload
    * At the top, under 'Actions', select 'Scale'
    * Set to '3'
    * Wait a few minutes and new nodes will show up in CueGUI
