# TODO
# - FHS, currently everything is packaged under /usr/share/APP
# - fix files, do not need to package stuff as dedicated user (http should be fine, if any)
Summary:	Systems Management web application
Name:		puppet-dashboard
Version:	1.2.23
Release:	0.1
License:	Apache v2.0
Group:		Applications/System
Source0:	http://yum.puppetlabs.com/sources/%{name}-%{version}.tar.gz
# Source0-md5:	ff3e02c3ddc834459cbd1fb7f209a1eb
URL:		http://www.puppetlabs.com/
Requires:	ruby-mysql
Requires:	ruby-rake
Requires:	ruby-rubygems
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Puppet Dashboard is a systems management web application for managing
Puppet installations and is written using the Ruby on Rails framework.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/{log,public,tmp,vendor,certs,spool,examples}
install -p -d $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

cp -a app bin config db ext lib public Rakefile script spec examples vendor $RPM_BUILD_ROOT%{_datadir}/%{name}
install -Dp config/database.yml.example $RPM_BUILD_ROOT%{_datadir}/%{name}/config/database.yml
install -Dp config/settings.yml.example $RPM_BUILD_ROOT%{_datadir}/%{name}/config/settings.yml
install -Dp VERSION $RPM_BUILD_ROOT%{_datadir}/%{name}/VERSION
chmod a+x $RPM_BUILD_ROOT%{_datadir}/%{name}/script/*

# Add sysconfig and init script
install -Dp ext/redhat/%{name}.init $RPM_BUILD_ROOT/etc/rc.d/init.d/puppet-dashboard
install -Dp ext/redhat/puppet-dashboard-workers.init $RPM_BUILD_ROOT/etc/rc.d/init.d/puppet-dashboard-workers
install -Dp ext/redhat/%{name}.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/puppet-dashboard
install -Dp ext/redhat/%{name}.logrotate $RPM_BUILD_ROOT/etc/logrotate.d/puppet-dashboard

# Put logs in /var/log and symlink in %{_datadir} (FHS work)
%if 0
install -d $RPM_BUILD_ROOT/var/log/%{name}
if stat $RPM_BUILD_ROOT%{_datadir}/%{name}/log/*; then
	rsync -avx $RPM_BUILD_ROOT%{_datadir}/%{name}/log/* $RPM_BUILD_ROOT/var/log/%{name}
fi
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/log
ls -l $RPM_BUILD_ROOT%{_datadir}/%{name}
cd $RPM_BUILD_ROOT/var/log
ln -sf %{name} ../..%{_datadir}/%{name}/log
%endif

rm -r $RPM_BUILD_ROOT%{_datadir}/%{name}/ext/{redhat,debian,build_defaults.yaml,project_data.yaml}

%clean
rm -rf $RPM_BUILD_ROOT

%if 0
%pre
%groupadd -r puppet-dashboard
%useradd -r -g puppet-dashboard -d %{_datadir}/puppet-dashboard -s /sbin/nologin -c "Puppet Dashboard" puppet-dashboard
%endif

%post
/sbin/chkconfig --add puppet-dashboard
/sbin/chkconfig --add puppet-dashboard-workers

%preun
if [ "$1" = 0 ] ; then
	%service puppet-dashboard stop
	%service puppet-dashboard-workers stop
	/sbin/chkconfig --del puppet-dashboard
	/sbin/chkconfig --del puppet-dashboard-workers
fi

%postun
if [ "$1" -ge 1 ]; then
	%service puppet-dashboard condrestart
	%service puppet-dashboard-workers condrestart
fi

%files
%defattr(644,root,root,755)
%doc LICENSE README.markdown README_PACKAGES.markdown
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/puppet-dashboard
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/puppet-dashboard
%attr(754,root,root) /etc/rc.d/init.d/puppet-dashboard
%attr(754,root,root) /etc/rc.d/init.d/puppet-dashboard-workers
%dir %{_datadir}/puppet-dashboard
%attr(-,puppet-dashboard,puppet-dashboard) %dir %{_datadir}/%{name}/config
%attr(-,puppet-dashboard,puppet-dashboard) %config(noreplace) %verify(not md5 mtime size) %{_datadir}/%{name}/config/*
%attr(-,puppet-dashboard,puppet-dashboard) %doc %{_datadir}/%{name}/VERSION
%attr(-,puppet-dashboard,puppet-dashboard) %{_datadir}/%{name}/Rakefile
%attr(-,puppet-dashboard,puppet-dashboard) %{_datadir}/%{name}/app
%attr(-,puppet-dashboard,puppet-dashboard) %{_datadir}/%{name}/bin
%attr(-,puppet-dashboard,puppet-dashboard) %{_datadir}/%{name}/db
%attr(-,puppet-dashboard,puppet-dashboard) %{_datadir}/%{name}/ext
%attr(-,puppet-dashboard,puppet-dashboard) %{_datadir}/%{name}/lib
%attr(-,puppet-dashboard,puppet-dashboard) %{_datadir}/%{name}/log
%attr(-,puppet-dashboard,puppet-dashboard) %{_datadir}/%{name}/public
%attr(-,puppet-dashboard,puppet-dashboard) %{_datadir}/%{name}/script
%attr(-,puppet-dashboard,puppet-dashboard) %{_datadir}/%{name}/spec
%attr(-,puppet-dashboard,puppet-dashboard) %dir %{_datadir}/%{name}/spool
%attr(-,puppet-dashboard,puppet-dashboard) %dir %{_datadir}/%{name}/tmp
%attr(-,puppet-dashboard,puppet-dashboard) %{_datadir}/%{name}/vendor
%attr(-,puppet-dashboard,puppet-dashboard) %{_datadir}/%{name}/certs
%attr(-,puppet-dashboard,puppet-dashboard) %{_datadir}/%{name}/examples
#%attr(-,puppet-dashboard,puppet-dashboard) %dir /var/log/%{name}
