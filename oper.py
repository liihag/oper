#!/usr/bin/env python
# coding: utf-8

import os, sys
#dot_repo_dir = "/srv/storage/intel/windriver/.repo"

git_project_list = []

def extract_projects(manifest_file, verbose=False):
    from xml.dom.minidom import parse
    import xml.dom.minidom
    domtree = xml.dom.minidom.parse(manifest_file)
    domtree.getElementById("manifest")
    manifest = domtree.getElementsByTagName("manifest")[0]
    projects = manifest.getElementsByTagName("project")

    for p in projects:
        name = p.getAttribute("name")
        path = p.getAttribute("path")
        revision = p.getAttribute("revision")
        if verbose:
            print("extracing project name: %s\npath: %s\n" % (name, path))
        git_project_list.append({"name": name, "path": path, "revision": revision})


def doit(projects_dir, output_dir, test=True, verbose=False):  
    import shutil
    for p in git_project_list:
        source = os.path.join(projects_dir, p["path"])
        source += ".git"
            
        destination = os.path.join(output_dir, p["name"])
        destination += ".git"
        des_dir, des_base = os.path.split(destination)
        if not os.path.exists(des_dir):
            os.makedirs(des_dir)
        if not test:
            try:
                shutil.copytree(source, destination, symlinks=False)
                if verbose:
                    print("copy from %s to %s\n" % (source, destination))
            except OSError, e:
                if e.errno == 17:
                    print("destination: %s already exists" % destination)
            except:
                print "Unexpected error:", sys.exc_info()[0]
                raise
        else:
            if verbose:
                print("simulating copy from %s to %s\n" % (source, destination))
    

import argparse

parser = argparse.ArgumentParser(
        description='reverse an Android repo to server hierarchy',
        epilog="oper is the reverse of repo")
parser.add_argument("manifest_file",
        help="repo manifest file")
parser.add_argument("-r", "--dot_repo_dir", required=True,
        help="directory where .repo is")
parser.add_argument("-o", "--output_dir", default=os.getcwd(),
        help="directory for repo output")
parser.add_argument("-t", "--test", action="store_true", default=False,
        help="run in test mode")
parser.add_argument("--verbose", action="store_true",
        help="increase output verbosity")
parser.add_argument('--version', action='version', version='%(prog)s 0.1')

args = parser.parse_args()
parser.print_help()

extract_projects(args.manifest_file, verbose=args.verbose)

projects_dir = os.path.join(args.dot_repo_dir, "projects")

doit(projects_dir, args.output_dir, test=args.test, verbose=args.verbose)
