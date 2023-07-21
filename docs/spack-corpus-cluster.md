# Building a Spack Corpus on a Cluster

This document is aimed to walk you through building a corpus containing all
spack packages on a cluster. This document makes a lot of assumptions about the
environment that is present. The assumptions are as follows:
* Running containers can only be done with `singularity`
* A high performance networked file system is mounted to all the nodes being
used for the build.
* Flux is being used as the cluster scheduler (Slurm might be assumed on
auxiliary clusters).
* Your home directory is mounted across all machines.
* You have a `/tmp` directory that can be used for scratch, is mounted as a RAM
disk, and enough RAM to support this kind of usage.

Now, getting on with the process.

### Building the container image

Before running anything, the container images that contain all the dependencies
necessary for running the build need to be built. This might need to be done on
another machine as a lot of clusters don't have user namespace access which is
necessary for the container build process. Custom SSL certificates might also
need to be inserted into the container. More documentation on that process is
available [here](../.packaging/README.md). When on a cluster with appropriate
permissions (mostly namespacing related), run the following command to allocate
a node:

```bash
salloc -N 1 -p pdebug --userns
```

Once you have a node allocated, run the following commands to build the container:

```bash
git clone https://github.com/llvm-ml/llvm-ir-dataset-utils
cd llvm-ir-dataset-utils
cp /path/to/certificate.crt ./additional_cert.crt
podman build \
  -t llvm-ir-dataset-utils \
  -f ./.packaging/Dockerfile
podman save llvm-ir-dataset-utils > llvm-ir-dataset-utils.tar
singularity build llvm-ir-dataset-utils.sif docker-archive:llvm-ir-dataset-utils.tar
cp ./llvm-ir-dataset-utils.sif ~/
```

After the container image is built, we can get to setting up the build.

### Setting up the build

SSH into a login node of a cluster that has access to your home directory.

Then create directories to hold the buildcache and the corpus output. Here
we're making the assumption that the `/p/lustre<x>/<username>` directory is
a mount of a high performance parallel file system. The following commands
will need to be adapted for your environment:

```bash
mkdir -p /p/lustre1/<username>/spack_corpus/corpus
mkdir -p /p/lustre1/<username>/spack_corpus/buildcache
```

Now we need to create some setup scripts. Put the following in a script
at `~/in-container-setup.sh`:

```bash
ulimit -s 8192
ulimit -s 32768
ulimit -n 128000
cd /tmp
git clone https://github.com/llvm-ml/llvm-ir-dataset-utils
git clone https://github.com/spack/spack --depth=1
cd spack
git remote add fork https://github.com/boomanaiden154/spack
git fetch fork
git checkout running-fixes
cd ..
source ./spack/share/spack/setup-env.sh
export PATH=/tmp/share/spack/setup-env.sh
export PYTHONPATH=$PYTHONPATH:/tmp/llvm-ir-dataset-utils:/tmp/spack/lib/spack:/tmp/spack/lib/spack/external/_vendoring:/tmp/spack/lib/spack/external
```

TODO(boomanaiden154): Figure out how necessary the ulimit clauses are,
especially the stack size limit. Also figure out whether or not the
$PATH export is necessary after the source export.

Now put the following script into a script called `in-container-setup-headless.sh`:

```bash
source ~/in-container-setup.sh
ray start --address=$1
read -r -d '' _
```

Now put the following into a script called `container-setup.sh`:

```bash
singularity run \
  --bind /p/lustre1/<username>/spack_corpus:/corpus \
  ~/in-container-setup-headless.sh
```

Now the initial setup is complete! We should now be able to move on to setting
up a cluster, generating a list of packages, running the actual build, and
cleaning up.

TODO(boomanaiden154): Pull these scripts out of this documentation and put them
into a separate directory to make it easier to setup infrastructure. Perhaps
something like `infrastructure/llnl` and then group it with externally
contributed cloud infrastructure.

### Setting up a cluster

Now that everything is ready, we can start allocating nodes and getting a
cluster setup. Start off by allocating a node that will become the head node:

```bash
flux alloc -N 1
```

Then, start the singularity container:

```bash
singularity run --bind /p/lustre1/<username>/spack_corpus:/corpus bash
```

Now inside the container, run the `in-container-setup.sh` script:

```bash
source ~/in-container-setup.sh
```

Now, start the ray cluster so that we can attach other nodes:

```
ray start --head --port 6379
```

Now we need to attach other nodes. Open another terminal window and ssh into
the login node. Run `flux jobs` and note the name of the head node. Then run
the following command:

```
flux run -N <number of nodes to allocate> ~/container-setup.sh <node name>:6379
```

If all goes well, then running `ray status` on the head node should show a list
of nodes. In regards to the number of nodes, I've found 16 48-core nodes to work
reasonably well for a build of the spack corpus.

Now, go back to head node to create the package list and launch the build.

### Creating the Package List

This should be as simple as running the following script:


```bash
cd /tmp/llvm-ir-dataset-utils
python3 ./llvm_ir_dataset_utils/get_spack_package_list.py \
  --package_list=/corpus/package_list.json \
  --error_log=/corpus/package_list_errors.log
```

That command should concretize all the packages using all the nodes in the
cluster.

Now that we have a package list ready, we can run the build.

### Running the Build

This should be as simple as running the following command and then waiting a
couple hours:

```bash
python3 ./llvm_ir_dataset_utils/build_spack_package_from_list.py \
  --package_list=/corpus/package_list.json \
  --corpus_dir=/corpus/corpus \
  --buildcache_dir=/corpus/buildcache \
  --thread_count=32
```

If all goes well, the command will complete after building a couple thousand
packages and the desired bitcode files with be present in `/corpus` within the
container.

### Cleanup

After running everything, there will be a lot of leftover folders, like those
in the buildcache directory, and even in the corpus directory after it has been
copied/archived somewhere else. There is a script present in the repository that
can do many delete jobs in parallel to avoid using a significant amount of time
to do the deletions serially. For example, to delete everything in the
`/corpus/buildcache` directory:

```bash
python3 ./llvm_ir_dataset_utils/tools/delete_folder.py \
  --folder=/corpus/buildcache
```

You should end up with a clean folder pretty quickly.

### Evaluation

In order to see how much bitcode has been collected, you can run the following
script:

```bash
python3 ./llvm_ir_dataset_utils/tools/aggregate_build_sizes.py \
  --corpus_dir=/corpus/corpus
```

This should print out some warnings and give you the aggregate size in bytes.

TODO(boomanaiden154): Validate that these build instructions are correct at some
point.
