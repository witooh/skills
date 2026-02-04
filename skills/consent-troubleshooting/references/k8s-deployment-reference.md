# Kubernetes Deployment Reference

Complete reference for the consent service Kubernetes deployment on AWS EKS.

## Configuration Location

```
kong-gateway-auxiliarysystems/services/consent/
├── base/
│   ├── kustomization.yaml      # Base kustomization
│   ├── deployment.yaml         # Main deployment
│   ├── service.yaml            # ClusterIP service
│   ├── configmap.yaml          # Non-sensitive config
│   └── externalsecret.yaml     # External Secrets Operator config
└── overlays/
    └── dev/
        └── kustomization.yaml  # Dev environment overlay
```

## Deployment Overview

- **Namespace**: `consent`
- **Deployment Name**: `consent`
- **Service Account**: `consent-sa`
- **Replicas**: 1 (base)
- **Container Port**: 8080
- **Image**: Configured via overlay

## Resources

### Example Deployment Template (Not latest)

**Key Configuration**:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: consent
  namespace: consent
spec:
  replicas: 1
  revisionHistoryLimit: 3
  selector:
    matchLabels:
      app: consent
  template:
    spec:
      serviceAccountName: consent-sa
      containers:
        - name: consent
          image: consent:latest # Overridden in overlay
          ports:
            - containerPort: 8080
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 30
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
          envFrom:
            - configMapRef:
                name: consent-config
            - secretRef:
                name: consent-secrets
```

**Health Checks**:

- **Liveness**: `/health` every 30s (failure → pod restart)
- **Readiness**: `/health` every 10s (failure → remove from service endpoints)

### Service

**Configuration**:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: consent
  namespace: consent
spec:
  type: ClusterIP
  ports:
    - port: 8080
      targetPort: 8080
      protocol: TCP
  selector:
    app: consent
```

**Access**:

- Internal: `http://consent.consent.svc.cluster.local:8080`
- Port-forward: `kubectl port-forward -n consent svc/consent 8080:8080`

### ConfigMap

**Name**: `consent-config`

**Non-sensitive Configuration**:
| Key | Value | Description |
|-----|-------|-------------|
| APP_ENV | production | Environment |
| APP_PORT | 8080 | Application port |
| APP_NAME | consent | Application name |
| LOG_LEVEL | debug | Logging level |
| DB_SSL_MODE | require | PostgreSQL SSL mode |
| DB_MAX_OPEN_CONNS | 25 | Max DB connections |
| DB_MAX_IDLE_CONNS | 5 | Max idle connections |
| DB_CONN_MAX_LIFETIME | 1h | Connection lifetime |
| DB_CONN_MAX_IDLE_TIME | 30m | Idle timeout |
| KAFKA_ENABLED | false | Kafka enabled flag |
| KAFKA_TOPIC | consent-audit-events | Kafka topic |
| KAFKA_TLS_ENABLED | true | Kafka TLS |
| KAFKA_SASL_MECHANISM | AWS_MSK_IAM | Kafka auth |
| KAFKA_AWS_REGION | ap-southeast-7 | AWS region |

### ExternalSecret

**Name**: `consent-secrets`

**External Secrets Operator** configuration:

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: consent-secrets
  namespace: consent
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-store
    kind: ClusterSecretStore
  target:
    name: consent-secrets
  dataFrom:
    - extract:
        key: sit/aux-systems/consent
```

**Secrets from AWS Secrets Manager**:

| Secret Key      | AWS Property    | Purpose                |
| --------------- | --------------- | ---------------------- |
| VALKEY_HOST     | valkey.host     | Valkey/Redis host      |
| VALKEY_PORT     | valkey.port     | Valkey/Redis port      |
| VALKEY_USERNAME | valkey.username | Valkey/Redis username  |
| VALKEY_PASSWORD | valkey.password | Valkey/Redis password  |
| DB_HOST         | rds.host        | PostgreSQL RDS host    |
| DB_PORT         | rds.port        | PostgreSQL RDS port    |
| DB_USER         | rds.username    | PostgreSQL username    |
| DB_PASSWORD     | rds.password    | PostgreSQL password    |
| DB_NAME         | rds.database    | PostgreSQL database    |
| DB_SCHEMA       | rds.schema      | PostgreSQL schema      |
| KAFKA_BROKERS   | kafka.address   | Kafka broker addresses |

**AWS Secrets Manager Path**: `sit/aux-systems/consent`

## Environment Overlay (Dev)

**Location**: `overlays/dev/kustomization.yaml`

**Image Override**:

```yaml
images:
  - name: consent
    newName: 290768402609.dkr.ecr.ap-southeast-7.amazonaws.com/consent/consent-service
    newTag: 1.0.5-dev
```

**Version Tracking**:
Uses Kustomize replacements to:

1. Set `APP_VERSION` in ConfigMap to the image tag
2. Set `app-version-checksum` annotation on Deployment to trigger rolling updates

## Troubleshooting Commands

### Check All Resources

```bash
kubectl config use-context arn:aws:eks:ap-southeast-7:290768402609:cluster/aux-eks-goqmac0w

# Get all resources in namespace
kubectl get all -n consent

# Get deployments
kubectl get deployment -n consent

# Get pods
kubectl get pods -n consent -o wide

# Get services
kubectl get svc -n consent

# Get configmaps
kubectl get configmap -n consent

# Get secrets
kubectl get secret -n consent

# Get externalsecrets
kubectl get externalsecret -n consent
```

### Pod Diagnostics

```bash
# Describe pod (shows events, conditions, issues)
kubectl describe pod -n consent <pod-name>

# Get pod logs
kubectl logs -n consent <pod-name>

# Follow logs
kubectl logs -n consent <pod-name> -f

# Get logs from previous container (if restarted)
kubectl logs -n consent <pod-name> --previous

# Get logs with timestamps
kubectl logs -n consent <pod-name> --timestamps

# Search logs for errors
kubectl logs -n consent <pod-name> | grep -i error
```

### Deployment Diagnostics

```bash
# Check rollout status
kubectl rollout status deployment/consent -n consent

# View rollout history
kubectl rollout history deployment/consent -n consent

# Rollback to previous version
kubectl rollout undo deployment/consent -n consent

# Describe deployment
kubectl describe deployment consent -n consent
```

### ExternalSecret Diagnostics

```bash
# Check ExternalSecret status
kubectl get externalsecret -n consent

# Describe ExternalSecret
kubectl describe externalsecret consent-secrets -n consent

# Check if secret was created
kubectl get secret consent-secrets -n consent

# View secret keys (values are base64 encoded)
kubectl get secret consent-secrets -n consent -o yaml

# Check External Secrets Operator logs
kubectl logs -n external-secrets deployment/external-secrets-operator
```

### Events

```bash
# Get all events in namespace
kubectl get events -n consent --sort-by='.lastTimestamp'

# Get warning events only
kubectl get events -n consent --field-selector type=Warning

# Watch events
kubectl get events -n consent -w
```

### Port Forwarding

```bash
# Forward service to localhost
kubectl port-forward -n consent svc/consent 8080:8080

# Forward specific pod
kubectl port-forward -n consent <pod-name> 8080:8080

# Forward to different local port
kubectl port-forward -n consent svc/consent 9090:8080
```

## Common Issues

### 1. ExternalSecret Not Syncing

**Symptoms**: Pod fails to start, missing environment variables

**Check**:

```bash
kubectl describe externalsecret consent-secrets -n consent
```

**Common Causes**:

- External Secrets Operator not installed
- AWS credentials not configured
- Secret path `sit/aux-systems/consent` doesn't exist in AWS Secrets Manager
- IAM permissions missing

**Fix**:

```bash
# Verify secret exists in AWS
aws secretsmanager get-secret-value --secret-id sit/aux-systems/consent --region ap-southeast-7

# Check ExternalSecret status
kubectl get externalsecret consent-secrets -n consent -o yaml
```

### 2. Pod CrashLoopBackOff

**Symptoms**: Pod repeatedly restarting

**Check**:

```bash
kubectl describe pod -n consent <pod-name>
kubectl logs -n consent <pod-name> --previous
```

**Common Causes**:

- Missing database connection (can't reach RDS)
- Invalid database credentials
- Application error on startup
- Memory/resource limits

### 3. Readiness Probe Failing

**Symptoms**: Pod running but not receiving traffic

**Check**:

```bash
kubectl describe pod -n consent <pod-name>
kubectl logs -n consent <pod-name> | grep -i health
```

**Common Causes**:

- Database connection pool exhausted
- Application initialization slow
- Health check endpoint returning errors

### 4. Image Pull Errors

**Symptoms**: Pod stuck in `ImagePullBackOff`

**Check**:

```bash
kubectl describe pod -n consent <pod-name>
```

**Common Causes**:

- Invalid image tag in overlay
- ECR authentication expired
- Image doesn't exist in registry

**Fix**:

```bash
# Update ECR token
aws ecr get-login-password --region ap-southeast-7 | docker login --username AWS --password-stdin 290768402609.dkr.ecr.ap-southeast-7.amazonaws.com

# Verify image exists
aws ecr describe-images --repository-name consent/consent-service --region ap-southeast-7
```

## Deployment Updates

### Apply Changes

```bash
# Apply dev overlay
kubectl apply -k overlays/dev/

# Verify rollout
kubectl rollout status deployment/consent -n consent
```

### Update Image

```bash
# Edit overlay
vi overlays/dev/kustomization.yaml

# Change newTag to desired version
# Apply changes
kubectl apply -k overlays/dev/
```

### Force Restart

```bash
# Restart deployment (triggers rolling update)
kubectl rollout restart deployment/consent -n consent
```
