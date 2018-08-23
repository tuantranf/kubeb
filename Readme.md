# Kubeb: Kubernetes deploy cli

 Kubeb (Cubeb or Cubeba) provide CLI to build and deploy a web application to Kubernetes environment
 Kubeb use Docker & Helm chart for Kubernetes deployment

## Install

  Kubeb is installed by running one of the following commands in your terminal. You can install this via the command-line with either curl or wget.

  ### Requirement

  - Git
  - Python 3

  ### via curl
  ```bash
  sh -c "$(curl -fsSL https://raw.githubusercontent.com/tuantranf/kubeb/master/tools/install.sh)"
  ```

  ### via wget
  ```bash
  $ sh -c "$(wget https://raw.githubusercontent.com/tuantranf/kubeb/master/tools/install.sh -O -)"
  ```

## TL;DR;

```bash
# Init application
$ kubeb init --name sample --template laravel
# Build application
$ kubeb build -m 'release version 1'
# Deploy application
$ kubeb install
```

## Command
  ```bash
  kubeb --help
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
kubeb init --help

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
kubeb build --help

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
kubeb install --help

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
kubeb uninstall --help

Usage: kubeb uninstall [OPTIONS]

  Uninstall current application from Kubernetes

Options:
  --yes   Confirm the action without prompting.
```

## Deploy a Laravel example

Example [Laravel example](./example)

### Initiate application

```bash
$ kubeb init --docker

Release name [sample]:
Maintainer name [tranminhtuan]:
Release template [laravel]:
Docker image name [tranminhtuan/example]:
Kubeb config file generated in .kubeb/config.yml
```

### Build application

```bash
$ kubeb build --message "first build"
```

### Get all versions

```bash
$ kubeb version
- v1534975136422: first build
```

### Deploy application with specified version

```bash
$ kubeb install --version v1534975136422

Deploying version: v1534975136422
....
NOTES:
1. Get the application URL by running these commands:
  export POD_NAME=$(kubectl get pods --namespace default -l "app=laravel-rocket,release=sample" -o jsonpath="{.items[0].metadata.name}")
  echo "Visit http://127.0.0.1:8080 to use your application"
  kubectl port-forward --namespace default $POD_NAME 8080:80

2. Migrate database by running these commands:
  export POD_NAME=$(kubectl get pods --namespace default -l "app=laravel-rocket,release=sample" -o jsonpath="{.items[0].metadata.name}")
  Migrate database
  kubectl --namespace default exec -ti $POD_NAME -- php artisan migrate
  Run test data seeder
  kubectl --namespace default exec -ti $POD_NAME -- php artisan db:seed


Install application succeed.
```

### Apllication verify

```bash
$ export POD_NAME=$(kubectl get pods --namespace default -l "app=laravel-rocket,release=sample" -o jsonpath="{.items[0].metadata.name}")
$ kubectl port-forward --namespace default $POD_NAME 8080:80
```

Visit http://127.0.0.1:8080 to use your application"

### Uninstall application

```bash
$ kubeb uninstall

Do you want to continue? [y/N]: y
release "sample" deleted

Uninstall application succeed.
```

## How to add new template

Please add these files to templates folder.
Example [Laravel template](./libs/templates/laravel)

# Clean up all Kubeb configuration
kubeb destroy --yes

```bash
tree libs/template/laravel
.
├── Dockerfile
├── docker
│   ├── entrypoint.sh
│   └── vhost.conf
├── helm-chart-info.yaml
└── helm-values.yaml
```
