set -e
cp /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem ./tls-ca-bundle.crt
podman build -t llvm-ir-dataset-utils -f ./.packaging/Dockerfile --build-arg="ENABLE_LEGACY_RENEGOTIATION=ON" --build-arg="CUSTOM_CERT=./tls-ca-bundle.crt" .
podman save llvm-ir-dataset-utils > llvm-ir-dataset-utils.tar
export SINGULARITY_CACHEDIR=/tmp/singularity-cache
singularity build llvm-ir-dataset-utils.sif docker-archive:llvm-ir-dataset-utils.tar
