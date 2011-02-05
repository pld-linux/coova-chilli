Summary:	CoovaChilli - Software access controller for hotspots
Name:		coova-chilli
Version:	1.2.5
Release:	0.1
License:	GPL
Group:		Applications
Source0:	http://ap.coova.org/chilli/%{name}-%{version}.tar.gz
# Source0-md5:	1b890cb043b4340e1f15c2b2cff742d3
Patch0:		link.patch
Patch1:		config.patch
URL:		http://coova.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	perl-base
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	skip_post_check_so	libchilli.so.0.0.0

%description
Coova-Chilli is a fork of the ChilliSpot project - an open source
captive portal or wireless LAN access point controller. It supports
web based login (Universal Access Method, or UAM), standard for public
HotSpots, and it supports Wireless Protected Access (WPA), the
standard for secure roamable networks. Authentication, Authorization
and Accounting (AAA) is handled by your favorite radius server. Read
more at http://coova.org/ and http://www.chillispot.org/.

%package captive-portal
Summary:	Default captive portal for Coova
Group:		Applications
Requires:	%{name} = %{version}-%{release}
Requires:	haserl

%description captive-portal
Default captive portal for Coova.

%package -n python-coova-chilli
Summary:	Python library for CoovaChilli
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	python-libs
Requires:	python-modules
Requires:	python-pycairo
Requires:	python-pygobject
Requires:	python-pygtk-gtk

%description -n python-coova-chilli
Python library for CoovaChilli.

%package devel
Summary:	Header files for coovachili library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki coovachilli
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for coovachilli library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki coovachilli.

%package static
Summary:	Static coovachilli library
Summary(pl.UTF-8):	Statyczna biblioteka coovachilli
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static coovachilli library.

%description static -l pl.UTF-8
Statyczna biblioteka coovachilli.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_sysconfdir}/init.d $RPM_BUILD_ROOT/etc/rc.d

%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean

install -d $RPM_BUILD_ROOT%{_datadir}/coova-chilli
rm $RPM_BUILD_ROOT%{_sysconfdir}/chilli/wwwsh
mv $RPM_BUILD_ROOT%{_sysconfdir}/chilli/www $RPM_BUILD_ROOT%{_datadir}/coova-chilli/www

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add chilli
%service chilli restart

%preun
if [ "$1" = "0" ]; then
	%service -q chilli stop
	/sbin/chkconfig --del chilli
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/chilli
%attr(755,root,root) %ghost %{_libdir}/libbstring.so.0
%attr(755,root,root) %{_libdir}/libbstring.so.0.0.0
%attr(755,root,root) %ghost %{_libdir}/libchilli.so.0
%attr(755,root,root) %{_libdir}/libchilli.so.0.0.0
%attr(754,root,root) /etc/rc.d/init.d/chilli
%doc AUTHORS COPYING ChangeLog INSTALL README doc/dictionary.chillispot doc/hotspotlogin.cgi
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/chilli.conf
%dir %{_sysconfdir}/chilli
%attr(755,root,root) %{_sbindir}/chilli_opt
%attr(755,root,root) %{_sbindir}/chilli_query
%attr(755,root,root) %{_sbindir}/chilli_radconfig
%attr(755,root,root) %{_sbindir}/chilli_response
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/chilli/*
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_mandir}/man8/*.8*

%files captive-portal
%defattr(644,root,root,755)
%attr(755,root,root) %{_datadir}/coova-chilli/www/*.sh
%{_datadir}/coova-chilli/www/*.chi
%{_datadir}/coova-chilli/www/*.gif
%{_datadir}/coova-chilli/www/*.html
%{_datadir}/coova-chilli/www/*.jpg
%{_datadir}/coova-chilli/www/*.js
%{_datadir}/coova-chilli/www/*.png
%{_datadir}/coova-chilli/www/*.tmpl

%files -n python-coova-chilli
%defattr(644,root,root,755)
%{_libdir}/python/CoovaChilliLib.py

%files devel
%defattr(644,root,root,755)
%{_libdir}/*.la
%{_libdir}/libbstring.so
%{_libdir}/libchilli.so
%{_includedir}/chilli

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
