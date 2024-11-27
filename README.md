# PROJECT MANAGER

A concise tool for project management and tracking.


## Features

- **Objective Management**: Create, view and delete Objectives.
- **Project Tracking**: Keep track of your progress in different parts of the project (say, the main and tests), with Objective and TODO flags.

## Installation

1. Clone this repository:

```commandline
git clone https://github.com/SamJohn04/Project-Manager.git
cd Project-Manager
```

2. Install the project using pip:
```commandline
pip install .
```

This will install *manager*, the CLI command for Project Manager.

## Usage

To run the CLI, use `manager`.

1. Navigate to the root directory of the project to be managed.

2. Initialize the specification file
```commandline
manager init title
```

> To initialize the specification from a template, use:
> `manager generate [--path PATH] title`

This will generate the `pm.config.json` file.

3. Add path groups and objectives to the specification
```commandline
manager add {objective,path} ...
```

For paths, specify the extensions that should be a part of the search.

---

To add an objective, use:
```commandline
manager add objective [-d DESCRIPTION] name
```

To add a path group, use:
```commandline
manager add path name directoryPath
```
When adding a path group, you will be prompted for a list of extensions to be included, separated by commas

To view data of the specification, use:
```commandline
manager view
```

To set the TODO flag or Objective flag, use:
```commandline
manager set {todoFlag,objectiveFlag} value
```

To reset them, use:
```commandline
manager unset {todoFlag,objectiveFlag}
```

### Scan

To scan each path group for TODO flags (default TODO) and objective flags (default @OBJECTIVE), use:

```commandline
manager scan
```

The scan command will search through all the files in each path group (with any of the specified extensions), and will display all TODO flags and all objective flags in the code.
The TODO flag can be used to mark incomplete sections. On scanning, the Manager will show all TODO flags in each path group, along with the file path and the line where it is present.

The Objective flag is used for denoting the main section of code relating to a specific objective. The scan will show the status of each objective, as specified along with the flag.

### TODO Flags

TODO flags are flags to denote that some part of the project has been left "TODO".
The `scan` command searches for the TODO flag across the files, and displays all instances of it.

The default TODO flag is `TODO`

### Objective Flags

Objective flags are flags to the main section of a code tied to a specific objective.
It is expected that the Objective flag is followed by the objective name (and, optionally, the current status of it), separated by whitespaces.

```python
# @OBJECTIVE init-specification On-Going
```

The `scan` command searches for all instances of the Objective flag, and displays the status of each objective for each path group.
Each path group is recommended to only have one Objective flag per objective.

The default Objective flag is `@OBJECTIVE`

## Templates

Templates are JSON files having the following information:

- `name`: The name of the template, for ease of identification
- `toCreate`: A list of files or directories to create. Contains the `path` and `type` (`file` or `dir`). If `type` is `file`, may contain `content`. All parent directories will be created, if they do not exist.
- `pathGroups`: A list of path groups to be added to the generated projects. (*optional*)

## Future Enhancements

Further enhancements and new features are on the roadmap for the Project-Manager tool. Feel free to raise your ideas and contributions!


## License

The project is licensed under the MIT License

