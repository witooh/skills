#!/bin/bash

# K8s Diagnostics Script
# Check consent service health in AWS EKS

set -e

NAMESPACE="consent"
CONTEXT="arn:aws:eks:ap-southeast-7:290768402609:cluster/aux-eks-goqmac0w"

echo "========================================"
echo "Consent Service K8s Diagnostics"
echo "========================================"
echo ""

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "ERROR: kubectl is not installed"
    exit 1
fi

# Set context
echo "Setting kubectl context..."
kubectl config use-context "$CONTEXT" || {
    echo "ERROR: Failed to set context $CONTEXT"
    exit 1
}

echo ""
echo "========================================"
echo "1. Namespace Resources"
echo "========================================"
kubectl get all -n "$NAMESPACE" || true

echo ""
echo "========================================"
echo "2. Pod Status"
echo "========================================"
kubectl get pods -n "$NAMESPACE" -o wide || true

echo ""
echo "========================================"
echo "3. Deployment Status"
echo "========================================"
kubectl get deployment -n "$NAMESPACE" -o yaml | grep -A5 "status:" || true

echo ""
echo "========================================"
echo "4. Service Status"
echo "========================================"
kubectl get svc -n "$NAMESPACE" || true
kubectl get endpoints -n "$NAMESPACE" || true

echo ""
echo "========================================"
echo "5. ConfigMap & Secrets"
echo "========================================"
echo "ConfigMaps:"
kubectl get configmap -n "$NAMESPACE" || true
echo ""
echo "Secrets:"
kubectl get secret -n "$NAMESPACE" || true
echo ""
echo "ExternalSecrets:"
kubectl get externalsecret -n "$NAMESPACE" 2>/dev/null || echo "ExternalSecret CRD not found"

echo ""
echo "========================================"
echo "6. Recent Events"
echo "========================================"
kubectl get events -n "$NAMESPACE" --sort-by='.lastTimestamp' | tail -20 || true

echo ""
echo "========================================"
echo "7. Pod Logs (last 50 lines)"
echo "========================================"
POD_NAME=$(kubectl get pods -n "$NAMESPACE" -l app=consent -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "")
if [ -n "$POD_NAME" ]; then
    echo "Pod: $POD_NAME"
    kubectl logs -n "$NAMESPACE" "$POD_NAME" --tail=50 || true
    
    echo ""
    echo "Errors in logs:"
    kubectl logs -n "$NAMESPACE" "$POD_NAME" | grep -i error || echo "No errors found"
else
    echo "No consent pods found"
fi

echo ""
echo "========================================"
echo "8. Resource Usage"
echo "========================================"
kubectl top pod -n "$NAMESPACE" 2>/dev/null || echo "Metrics not available (metrics-server not installed?)"

echo ""
echo "========================================"
echo "Diagnostics Complete"
echo "========================================"
