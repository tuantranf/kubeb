FROM centos/httpd:latest

MAINTAINER {{ maintainer }}

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# Update and install latest packages and prerequisites
RUN yum makecache fast && yum -y --setopt=tsflags=nodocs update \
    && yum -y --setopt=tsflags=nodocs install https://mirror.webtatic.com/yum/el7/webtatic-release.rpm \
    && yum -y --setopt=tsflags=nodocs install git php71w php71w-cli php71w-common php71w-opcache php71w-mysql php71w-mbstring php71w-xml php71w-gd php71w-pdo

# Install imagick
RUN yum -y install php71w-pecl-imagick ImageMagick ImageMagick-devel ImageMagick-perl

# Install php composer
RUN curl -sS https://getcomposer.org/installer | php \
    && mv /composer.phar /usr/bin/composer \
    && chmod +x /usr/bin/composer

RUN yum -y update
RUN yum clean all

ADD docker/vhost.conf /etc/httpd/conf.d/vhost.conf

ADD docker/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

WORKDIR /var/www/html

COPY . .

RUN chown -R apache:apache /var/www/html

RUN composer install

ENTRYPOINT ["/entrypoint.sh"]

CMD ["/usr/sbin/httpd", "-DFOREGROUND"]

EXPOSE 80