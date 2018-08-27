#!/usr/bin/env bash
helm repo add laravel-rocket-helm-chart https://tuantranf.github.io/laravel-rocket-helm-chart
helm repo update
helm upgrade --install --force example -f .kubeb/helm-values.yml laravel-rocket-helm-chart/laravel-rocket --wait