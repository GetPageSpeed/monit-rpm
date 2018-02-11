# Latest Monit on CentOS 7

[![Build Status](https://travis-ci.org/GetPageSpeed/monit-rpm.svg?branch=master)](https://travis-ci.org/GetPageSpeed/monit-rpm) [<img src="https://copr.fedorainfracloud.org/coprs/getpagespeed/monit/package/monit/status_image/last_build.png">](https://copr.fedorainfracloud.org/coprs/getpagespeed/monit/package/monit/) 

Install latest Monit on CentOS using the following commands:

    sudo yum install https://extras.getpagespeed.com/redhat/7/noarch/RPMS/getpagespeed-extras-7-0.el7.gps.noarch.rpm
    sudo yum install monit

Should you find that there is a more recent (our built version can be found in repository's latest tag), please open a ticket.

## Background

Monit in EPEL repository has not been updated in a year, but we want a more recent version at all times.

This repository contains spec file from [upstream](https://dl.fedoraproject.org/pub/epel/7/SRPMS/m/monit-5.14-1.el7.src.rpm) and rebuilds latest Monit version onto COPR. The result is a special YUM repository you can add to your system in order to install fresh Monit.

# Technical

Using [Travis](https://gist.github.com/abn/daf262e7e454509df1429c87068923d1) to verify that the SRPM can be built successfully. The rest is done by COPR itself: it fetches the .spec file and builds SRPM on its own.

