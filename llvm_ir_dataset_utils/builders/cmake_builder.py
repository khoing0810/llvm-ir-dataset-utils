"""Module for building and extracting bitcode from applications using CMake"""

import subprocess
import json
import os

from compiler_opt.tools import extract_ir_lib


def generate_configure_command(root_path, options_dict):
  command_vector = ["cmake", "-G", "Ninja"]
  for option in options_dict:
    command_vector.append(f"-D{option}={options_dict[option]}")
  # Add some default flags that are needed for bitcode extraction
  command_vector.append("-DCMAKE_C_COMPILER=clang")
  command_vector.append("-DCMAKE_CXX_COMPILER=clang++")
  # These two flags assume this is a stanard non-LTO build, will need to fix
  # later when we want to support (Thin)LTO builds.
  command_vector.append("-DCMAKE_C_FLAGS='-Xclang -fembed-bitcode=all'")
  command_vector.append("-DCMAKE_CXX_FLAGS='-Xclang -fembed-bitcode=all'")
  command_vector.append("-DCMAKE_EXPORT_COMPILE_COMMANDS=ON")
  command_vector.append(root_path)
  return command_vector


def generate_build_command(targets, threads):
  command_vector = ["ninja", "-j", str(threads)]
  command_vector.extend(targets)
  return command_vector


def perform_build(configure_command_vector, build_command_vector, build_dir,
                  corpus_dir):
  configure_log_path = os.path.join(corpus_dir, 'configure.log')
  with open(configure_log_path, 'w') as configure_log_file:
    subprocess.run(
        configure_command_vector,
        cwd=build_dir,
        check=True,
        stderr=configure_log_file,
        stdout=configure_log_file)
  build_log_path = os.path.join(corpus_dir, 'build.log')
  with open(build_log_path, 'w') as build_log_file:
    subprocess.run(
        build_command_vector,
        cwd=build_dir,
        check=True,
        stderr=build_log_file,
        stdout=build_log_file)


def extract_ir(build_dir, corpus_dir, threads):
  with open(os.path.join(
      build_dir, "./compile_commands.json")) as compilation_command_db_file:
    objects = extract_ir_lib.load_from_compile_commands(
        json.load(compilation_command_db_file), corpus_dir)
  relative_output_paths = extract_ir_lib.run_extraction(objects, threads,
                                                        "llvm-objcopy", None,
                                                        None, ".llvmcmd",
                                                        ".llvmbc")
  extract_ir_lib.write_corpus_manifest(None, relative_output_paths, corpus_dir)
