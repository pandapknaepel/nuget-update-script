#!/usr/bin/env python3

import subprocess
import json

def run_command(command):
    """Run a shell command and return the output."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"\033[91mError running command '{' '.join(command)}': {e.stderr}\033[0m")
        return None

def parse_outdated_output(output):
    """Parse the output of 'dotnet list package --outdated' and extract package details."""
    packages = []
    project = None

    for line in output.splitlines():
        if line.startswith("Project `"):
            project = line.split('`')[1].split(' ')[0]
        elif project and line.strip().startswith(">"):
            parts = line.split()
            package_info = {
                "project": project,
                "name": parts[1],
                "current_version": parts[2],
                "latest_version": parts[4]  # Extract the latest version from the output
            }
            packages.append(package_info)

    return packages

def update_packages(packages):
    """Update the packages to the latest versions."""
    errors = []
    for package in packages:
        command = [
            "dotnet", "add", package["project"], "package",
            package["name"], "--version", package["latest_version"]
        ]
        try:
            print(f"\033[94mUpdating {package['name']} in {package['project']} to version {package['latest_version']}...\033[0m")
            result = subprocess.run(command, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"\033[91mError updating package {package['name']}: {e.stderr}\033[0m")
            errors.append((package["name"], e.stderr))

    return errors

def list_startup_projects():
    """List all available startup projects."""
    result = run_command(["dotnet", "sln", "list"])
    if result:
        projects = [line.strip() for line in result.splitlines() if line.strip().endswith(".csproj")]
        return projects
    return []

def ask_for_project(projects):
    """Ask the user to select a startup project if more than one is found."""
    print("\nMultiple startup projects found. Please select one:")
    for i, project in enumerate(projects, 1):
        print(f"{i}. {project}")
    selection = int(input("\nEnter the number of the startup project to use (or 0 to skip): ").strip())
    if 1 <= selection <= len(projects):
        return projects[selection - 1]
    return None

def restore_and_build(startup_project):
    """Run dotnet restore with no cache and build the selected startup project."""
    if not startup_project:
        print("\033[93mNo startup project specified, skipping restore and build.\033[0m")
        return False

    try:
        print(f"\033[94mRunning dotnet restore with no cache for {startup_project}...\033[0m")
        subprocess.run(["dotnet", "restore", "--no-cache", startup_project], capture_output=True, text=True, check=True)
        print(f"\033[92mRestoring packages completed successfully for {startup_project}.\033[0m")
    except subprocess.CalledProcessError as e:
        print(f"\033[91mError during dotnet restore: {e.stderr}\033[0m")
        return False

    try:
        print(f"\033[94mBuilding the solution for {startup_project}...\033[0m")
        subprocess.run(["dotnet", "build", startup_project], capture_output=True, text=True, check=True)
        print(f"\033[92mBuild completed successfully for {startup_project}.\033[0m")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\033[91mError during dotnet build: {e.stderr}\033[0m")
        return False

if __name__ == "__main__":
    # Step 1: List outdated packages
    print("\033[94mListing outdated packages...\033[0m")
    outdated_output = run_command(["dotnet", "list", "package", "--outdated"])

    if outdated_output:
        # Step 2: Parse the output
        packages = parse_outdated_output(outdated_output)
        print(f"\033[94mFound {len(packages)} outdated packages.\033[0m")

        if packages:
            # Step 3: Update the packages
            errors = update_packages(packages)
            
            # Step 4: Handle errors
            if errors:
                print("\033[91mSome errors occurred during the update process:\033[0m")
                for name, error in errors:
                    print(f"{name}: {error}")
            else:
                print("\033[92mAll packages were successfully updated.\033[0m")
                
                # Step 5: List startup projects and handle restore/build
                projects = list_startup_projects()
                if projects:
                    if len(projects) == 1:
                        startup_project = projects[0]
                    else:
                        startup_project = ask_for_project(projects)
                    if startup_project:
                        if not restore_and_build(startup_project):
                            print("\033[91mFailed to restore or build the solution.\033[0m")
                else:
                    print("\033[93mNo startup projects found.\033[0m")
        else:
            print("\033[92mNo packages need updating.\033[0m")
    else:
        print("\033[91mFailed to list outdated packages.\033[0m")
