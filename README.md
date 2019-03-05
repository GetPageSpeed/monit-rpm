# Latest Monit on CentOS 7

[![Build Status](https://travis-ci.org/GetPageSpeed/monit-rpm.svg?branch=master)](https://travis-ci.org/GetPageSpeed/monit-rpm) [<img src="https://copr.fedorainfracloud.org/coprs/getpagespeed/monit/package/monit/status_image/last_build.png">](https://copr.fedorainfracloud.org/coprs/getpagespeed/monit/package/monit/) 

Install latest Monit on CentOS using the following commands:

    sudo yum -y install https://extras.getpagespeed.com/release-el7-latest.rpm
    sudo yum install monit

## Background

When I noticed that Monit in EPEL repository has not been updated in a year, I thought of a way to have most recent version at all times.

This repository contains spec file from [upstream](https://dl.fedoraproject.org/pub/epel/7/SRPMS/m/monit-5.14-1.el7.src.rpm) and rebuilds latest Monit version onto COPR, GetPageSpeed Repository and PackageCloud. 

## Technical

This git repository is a great sample of deployment automation using CircleCI (deploy to GetPageSpeed) and Travis (test status and deploy to PackageCloud). Those working configs can be found in `.circleci` and `.travis.yml`, respectively.

* [Travis](https://gist.github.com/abn/daf262e7e454509df1429c87068923d1) verifies that the SRPM can be built successfully and pushes the built package onto PackageCloud.
* COPR is set to fetch the `.spec` file from here and builds SRPM / RPM on its own.
* CircleCi tests SRPM build-ability and builds complete RPM and pushes that onto GetPageSpeed repo.

Now as to how we know when a new version of Monit is released: that's done with a special script that basically checks BitBucket repository of Monit for recent releases, then updates and pushes the `.spec` file.
