#!/usr/bin/env bash
php artisan migrate:fresh

/usr/sbin/httpd -DFOREGROUND