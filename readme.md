# NuGet Update Script

A Python script that automates the process of updating NuGet packages for .NET projects. This script identifies outdated packages, updates them to the latest versions, restores the packages with no cache, and optionally builds the solution. It is especially useful for developers using editors like Visual Studio Code, which may not have built-in NuGet package management.

## Features

- **Identify Outdated Packages**: Lists all outdated NuGet packages in your projects.
- **Update Packages**: Automatically updates packages to their latest versions.
- **Optional Restore and Build**: Restores packages without using the cache and builds the solution if a startup project is specified.
- **Error Handling**: Displays errors only when they occur, providing clear and concise feedback.

## Prerequisites

- Python 3.x
- .NET SDK

## Installation

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/your-username/nuget-update-script.git
   cd nuget-update-script
   ```

2. **Set Up Python Environment**:
   Create a virtual environment and activate it (optional but recommended).
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

## Usage

1. **Basic Usage**:
   Run the script to update NuGet packages.
   ```sh
   python3 nuget_update.py
   ```

2. **Alias for Easy Access**:
   Add an alias to your shell configuration file (e.g., `.bashrc`, `.zshrc`) for convenience.
   ```sh
   alias nuget-update='python3 /path/to/nuget_update.py'
   ```
   Reload your shell configuration:
   ```sh
   source ~/.bashrc  # Or `source ~/.zshrc`
   ```

3. **Selecting a Startup Project**:
   If multiple startup projects are found, the script will prompt you to select one. If only one project is found, it will automatically use it.

4. **Handling Errors**:
   The script will only display output if an error occurs during the update, restore, or build processes, ensuring a clean and concise workflow.

![image](https://github.com/user-attachments/assets/785a9478-1610-413c-a068-d03776aab0e0)
