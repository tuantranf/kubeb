# Kubeb: Kubernetes deploy cli

## Note
 Kubeb (Cubeb or Cubeba) provide CLI to build and deploy a web application to Kubernetes environment
 Kubeb use Docker & Helm chart for Kubernetes deployment

## Python version

## Install:
```bash
  $ git clone [REPOSITORY_URL]
  $ cd docker-generator
  $ python3 -m venv env
  $ source env/bin/activate
  $ pip install -r requirements.txt
  $ pip install --editable .
  $ kubeb --help
    Usage: kubeb [OPTIONS] COMMAND [ARGS]...

    Options:
      --version  Show the version and exit.
      --help     Show this message and exit.

    Commands:
      build      Build current application Build Dockerfile...
      destroy    Remove all kubeb configuration
      info       Show current configuration
      init       Init kubeb configuration Generate config,...
      install    Install current application to Kubernetes...
      uninstall  Uninstall current application from Kubernetes
      version    Show current application versions
```

## Initiate your application

```bash
$ kubeb init --help
Usage: kubeb init [OPTIONS]

  Init kubeb configuration Generate config, script files Generate Docker
  stuff if use --docker option

Options:
  -n, --name TEXT      Release name.
  -n, --user TEXT      Maintainer name.
  -t, --template TEXT  Release template name.
  --image TEXT         Docker image name.
  --docker             Generate docket setup files.
  --force              Overwrite config file.
```

## Build your application (Dockerfile building)

```bash
$ kubeb build --help
Usage: kubeb build [OPTIONS]

  Build current application Build Dockerfile image Add release note, tag to
  config file

Options:
  -m, --message TEXT  Release note

```

## Install your application to Kubernetes enviroment

Using --version option to specify application version. If version is not specified, Kubeb will use the latest version
You can see version list by `kubeb version` command
```bash
$ kubeb install --help
Usage: kubeb install [OPTIONS]

  Install current application to Kubernetes Generate Helm chart value file
  with docker image version If version is not specified, will get the latest
  version

Options:
  -v, --version TEXT  Install version.
  --help               this message and exit.
```

## Uninstall your application from Kubernetes

```bash
$ kubeb uninstall --help
Usage: kubeb uninstall [OPTIONS]

  Uninstall current application from Kubernetes

Options:
  --yes   Confirm the action without prompting.
```

## How to add new template

Please add these files to templates folder.
Example [Laravel template](./libs/template/laravel)


```bash
$ tree libs/template/laravel
.
├── Dockerfile
├── docker
│   ├── entrypoint.sh
│   └── vhost.conf
├── helm-chart-info.yaml
└── helm-values.yaml
```