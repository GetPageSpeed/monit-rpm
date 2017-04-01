# Latest Monit on CentOS 7

[<img src="https://copr.fedorainfracloud.org/coprs/getpagespeed/monit/package/monit/status_image/last_build.png">](https://copr.fedorainfracloud.org/coprs/getpagespeed/monit/package/monit/)

Install latest Monit on CentOS using the following commands:

    sudo curl -sL -o /etc/yum.repos.d/getpagespeed-monit.repo https://copr.fedoraproject.org/coprs/getpagespeed/monit/repo/epel-7/getpagespeed-monit-epel-7.repo
    sudo yum install monit

Should you find that there is a more recent (our built version can be found in repository's latest tag), please open a ticket.

## Background

Monit in EPEL repository has not been updated in a year, but we want a more recent version at all times.
This repository contains spec file from [upstream](https://dl.fedoraproject.org/pub/epel/7/SRPMS/m/monit-5.14-1.el7.src.rpm) and rebuilds latest Monit version onto COPR. The result is a special YUM repository you can add to your system in order to install fresh Monit.

What follows, is notes to myself on how it's done, aka "A playground of RPM builder" :)

Using https://github.com/dgoodwin/tito
https://m0dlx.com/blog/Reproducible_builds_on_Copr_with_tito_and_git_annex.html
http://miroslav.suchy.cz/blog/archives/2013/12/29/how_to_build_in_copr/index.html
http://miroslav.suchy.cz/blog/archives/2013/12/17/how_to_create_new_release_of_rpm_package_in_5_seconds/

## Create COPR project

    copr-cli create --chroot epel-7-x86_64 \
    --description 'demo repository' \
    --instructions 'do not try this, I am just doing demo for blogpost' \
    demo
    
    
## Setup tito

    git config --global user.email ciapnz@gmail.com
    // create github repo, then:
    git init
    git annex init # for large source tarballs
    tito init
    # for large tarballs: open tito.props and change builder to GitAnnexBuilder
    # for small tarballs: open tito.props and change builder to GitAnnexBuilder
    git annex addurl --file=monit-5.19.0.tar.gz https://mmonit.com/monit/dist/monit-5.19.0.tar.gz
    git commit -am "Add foo 1.2.3"
    git remote add origin https://github.com/dvershinin/monit-epel-rpm.git
    git push -u origin master
    tito tag --keep-version

https://linux.die.net/man/8/tito

1. Save user preferences as described in titorc(5)
2. Initialize a rel-eng directory
3. Test
1. Make changes to source
2. Use git to commit changes
3. Build: tito build --rpm --test
4. Finalize a release
1. Tag: tito tag
2. Push: git push && git push $ORIGIN $TAG
3. Build: tito build [OPTIONS]    
