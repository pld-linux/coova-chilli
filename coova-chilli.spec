Summary:	CoovaChilli - Software access controller
Name:		coovachilli
Version:	1.0.11
Release:	0.1
License:	GPL
Group:		Applications
Source0:	http://ap.coova.org/chilli/coova-chilli-%{version}.tar.gz
# Source0-md5:	d932dc9ca42b90d56ef27552f049c44a
URL:		http://coova.org
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Coova-Chilli is a fork of the ChilliSpot project - an open source
captive portal or wireless LAN access point controller. It supports
web based login (Universal Access Method, or UAM), standard for public
HotSpots, and it supports Wireless Protected Access (WPA), the
standard for secure roamable networks. Authentication, Authorization
and Accounting (AAA) is handled by your favorite radius server. Read
more at http://coova.org/ and http://www.chillispot.org/.

%prep
%setup -q -n coova-chilli-%{version}

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/*.so*
%attr(754,root,root) /etc/init.d/chilli
%doc AUTHORS COPYING ChangeLog INSTALL README doc/dictionary.chillispot doc/hotspotlogin.cgi
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/chilli/*
%dir %{_sysconfdir}/chilli
%attr(755,root,root)%{_sysconfdir}/chilli/www/config.sh
%{_sysconfdir}/chilli/www/*
%{_sysconfdir}/chilli/wwwsh
%{_sysconfdir}/chilli/functions
%{_sysconfdir}/chilli/*.sh
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_mandir}/man8/*.8*
