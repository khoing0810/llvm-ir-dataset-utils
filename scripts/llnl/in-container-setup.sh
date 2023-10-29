#!/bin/bash
set -e
rm -rf /tmp/llvm-ir-dataset-utils
rm -rf /tmp/llvm-ir-transformers
rm -rf /tmp/spack
rm -rf /tmp/build
rm -rf /tmp/rustup
rm -rf /tmp/cargo
rm -rf /tmp/llvm-tokenizer
rm -rf /tmp/llvm-ml-utils
rm -rf /tmp/fastBPE
rm -rf /tmp/gold
export CARGO_HOME=/tmp/cargo
export RUSTUP_HOME=/tmp/rustup
rustup default nightly
# TODO(boomanaiden154): See how necessary these ulimit clauses actually are.
ulimit -s 8192
ulimit -u 32768
ulimit -n 128000
cd /tmp
# TODO(boomanaiden154): Switch back to using spack (or at least do some cleanup)
# once most of the patches have landed upstream.
git clone https://github.com/llvm-ml/llvm-ir-dataset-utils
export PYTHONPATH=$PYTHONPATH:/tmp/llvm-ir-dataset-utils:/tmp/spack/lib/spack/:/tmp/spack/lib/spack/external/_vendoring/:/tmp/spack/lib/spack/external/
git clone -b running-fixes-2 --depth=1 https://github.com/boomanaiden154/spack
source ./spack/share/spack/setup-env.sh
export PATH=/tmp/spack/bin:$PATH
spack bootstrap root /tmp/bootstrap-root
spack bootstrap now
cd /tmp
git clone https://github.com/llvm-ml/llvm-tokenizer
mkdir llvm-tokenizer/build
cd llvm-tokenizer/build
cmake -GNinja -DCMAKE_BUILD_TYPE=Release ../
ninja
export PATH=$PATH:/tmp/llvm-tokenizer/build
cd /tmp
git clone https://github.com/llvm-ml/llvm-ml-utils
mkdir llvm-ml-utils/build
cd llvm-ml-utils/build
cmake -GNinja -DCMAKE_BUILD_TYPE=Release ../
ninja
cd /tmp
export PATH=$PATH:/tmp/llvm-ml-utils/build
export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
# Install FastBPE
git clone https://github.com/glample/fastBPE.git
cd fastBPE
clang++ -std=c++11 -pthread -O3 fastBPE/main.cc -IfastBPE -o fast
export PATH=$PATH:/tmp/fastBPE
cd /tmp
git clone https://github.com/llvm-ml/llvm-ir-transformers
export PYTHONPATH=$PYTHONPATH:/tmp/llvm-ir-transformers
cd /tmp
curl -L https://github.com/go-enry/go-license-detector/releases/download/v4.3.0/license-detector-v4.3.0-linux-amd64.tar.gz > gold.tar.gz
tar -xf gold.tar.gz
mkdir /tmp/gold
mv ./license-detector /tmp/gold/license-detector
export PATH=$PATH:/tmp/gold
set +e
