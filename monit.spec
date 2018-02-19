Name:           monit
Version:        5.25.1
Release:        4%{?dist}
Summary:        Manages and monitors processes, files, directories and devices

Group:          Applications/Internet
License:        AGPLv3
URL:            http://mmonit.com/monit/
Source0:        http://mmonit.com/monit/dist/%{name}-%{version}.tar.gz
Source2:        monit.logrotate
Source3:        monit.service
Source4:        monit-logging-conf

BuildRequires: flex
BuildRequires: openssl-devel
BuildRequires: pam-devel
BuildRequires: byacc
BuildRequires: systemd
BuildRequires: gcc

Requires(post): systemd-sysv
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd


%description
monit is a utility for managing and monitoring, processes, files, directories
and devices on a UNIX system. Monit conducts automatic maintenance and repair
and can execute meaningful causal actions in error situations.


%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

install -p -D -m0600 monitrc $RPM_BUILD_ROOT%{_sysconfdir}/monitrc
install -p -D -m0755 monit $RPM_BUILD_ROOT%{_bindir}/monit

# Log file & logrotate config
install -p -D -m0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/monit
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log
install -m0600 /dev/null $RPM_BUILD_ROOT%{_localstatedir}/log/monit.log

# systemd service file
mkdir -p ${RPM_BUILD_ROOT}%{_unitdir}
install -m0644 %{SOURCE3} ${RPM_BUILD_ROOT}%{_unitdir}/monit.service

# Let's include some good defaults
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/monit.d
install -p -D -m0644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/monit.d/logging

%{__sed} -i 's/# set daemon  120.*/set daemon 60  # check services at 1-minute intervals/' \
    $RPM_BUILD_ROOT%{_sysconfdir}/monitrc

%{__sed} -i 's/#  include \/etc\/monit.d\/\*/include \/etc\/monit.d\/\*/' \
    $RPM_BUILD_ROOT%{_sysconfdir}/monitrc

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post monit.service

# Moving old style configuration file to upstream's default location
[ -f %{_sysconfdir}/monit.conf ] &&
    touch -r %{_sysconfdir}/monitrc %{_sysconfdir}/monit.conf &&
    mv -f %{_sysconfdir}/monit.conf %{_sysconfdir}/monitrc 2> /dev/null || :

%preun
%systemd_preun monit.service

%postun
%systemd_postun_with_restart monit.service

%triggerun -- monit < 5.3.1-1
/usr/bin/systemd-sysv-convert --save monit > /dev/null 2>&1 || :
/bin/systemctl --no-reload enable monit.service > /dev/null 2>&1 || :
/sbin/chkconfig --del monit > /dev/null 2>&1 || :
/bin/systemctl try-restart monit.server > /dev/null 2>&1 || :

%files
%defattr(-,root,root,-)
%doc COPYING README
%config(noreplace) %{_sysconfdir}/monitrc
%config(noreplace) %{_sysconfdir}/monit.d/logging
%config(noreplace) %{_sysconfdir}/logrotate.d/monit
%config %ghost %{_localstatedir}/log/monit.log
%{_unitdir}/monit.service
%{_sysconfdir}/monit.d/
%{_bindir}/%{name}
%{_mandir}/man1/monit.1*


%changelog
* Mon Feb 06 2017 Danila Vershinin <ciapnz@gmail.com> - 5.20.0-4
- Update to 5.20

* Sat Sep 12 2015 Stewart Adam <s.adam@diffingo.com> - 5.14-1
- Upgrading to new upstream release 5.14.0

* Wed Dec 04 2013 Maxim Burgerhout <maxim@wzzrd.com> - 5.6.0-1
- Upgrading to new upstream release 5.6.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 9 2012 Maxim Burgerhout <wzzrd@fedoraproject.org> - 5.3.1-3
- Fix systemd unit file

* Sun Jan 8 2012 Maxim Burgerhout <wzzrd@fedoraproject.org> - 5.3.1-2
- Rebuild for gcc 4.7

* Sun Nov 13 2011 Maxim Burgerhout <wzzrd@fedoraproject.org> - 5.3.1-1
- New upstream release 5.3.1
- Added systemd unit file and dropped sysv init support
- Dropped the patch that changed the default name of the configuration file
- Dropped the patch that silenced daemon startup

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.5-2
- Rebuilt for glibc bug#747377

* Sat May 07 2011 Maxim Burgerhout <wzzrd@fedoraproject.org> - 5.2.5-1
- Sync to upstream bugfix release; most important new features:
- Memory footprint decreased by 10%
- Logfile default umask changed to 0640
- New CLI command to test regexps for process names
- And various bugfixes

* Thu Aug 05 2010 Maxim Burgerhout <wzzrd@fedoraproject.org> - 5.2.3-1
- Update to new upstream version 5.2.3; new features in 5.2.3 include:
- MySQL protocol now support version 5.5
- Support for monitoring swap usage
- Allow process monitoring based on output of ps and regexps
- Various bugfixes

* Thu Aug 05 2010 Maxim Burgerhout <wzzrd@fedoraproject.org> - 5.1.1-2
- Enabled PAM authentication (bz #621599)

* Mon Jul 05 2010 Maxim Burgerhout <wzzrd@fedoraproject.org> - 5.1.1-1
- Version bump to 5.1.1 (needed new version of monit-no-startup-msg.patch)
- Ghosted the logfile

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 5.0.3-2
- rebuilt with new openssl

* Fri Aug 14 2009 Stewart Adam <s.adam at diffingo.com> - 5.0.3-1
- Update to 5.0.3 (thanks to Lubomir Rintel of Good Data for the patch)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> 4.10.1-9
- rebuild with new openssl

* Mon Dec 22 2008 Stewart Adam <s.adam at diffingo.com> 4.10.1-8
- Tweak configuration defaults: include /etc/monit.d/*, log to /var/log/monit
  and set daemon time to 60s
- Don't use $desc in initscript
- Add patch to search for monit.conf by default (#475044)
- Add patch to remove redundant startup message

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.10.1-7
- Autorebuild for GCC 4.3

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 4.10.1-6
 - Rebuild for deps

* Wed Dec 5 2007 Stewart Adam <s.adam at diffingo.com> 4.10.1-5
- Rebuild to fix broken deps on libssl.so.6 and libcrypto.so.6

* Sat Nov 24 2007 Stewart Adam <s.adam at diffingo.com> 4.10.1-4
- Substitute RPM macros for their real values in monit.conf (#397671)

* Tue Nov 13 2007 Stewart Adam <s.adam at diffingo.com> 4.10.1-3
- Bump
- Fix changelog date for previous entry

* Mon Nov 12 2007 Stewart Adam <s.adam at diffingo.com> 4.10.1-2.1
- Switch back to OpenSSL since NSS isn't working too well with Monit

* Wed Nov 7 2007 Stewart Adam <s.adam at diffingo.com> 4.10.1-2
- License is actually GPLv3+
- s/%%{__install}/%%{__install} -p/
- NSS-ize

* Tue Nov 6 2007 Stewart Adam <s.adam at diffingo.com> 4.10.1-1
- Initial RPM release
