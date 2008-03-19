Summary:	phpldapadmin - a web-based LDAP client
Summary(pl.UTF-8):	phpldapadmin - klient WWW dla LDAP
Name:		phpldapadmin
Version:	1.1.0.5
Release:	0.6
License:	GPL
Group:		Applications/Networking
Source0:	http://dl.sourceforge.net/phpldapadmin/%{name}-%{version}.tar.gz
# Source0-md5:	5ea78a6758e347c77ef291882675f266
Patch0:		%{name}-paths.patch
URL:		http://phpldapadmin.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	php(gettext)
Requires:	php(ldap)
Requires:	php(pcre)
Requires:	php(xml)
Requires:	webapps
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
phpLDAPadmin is a web-based LDAP client. It provides easy,
anywhere-accessible, multi-language administration for your LDAP
server. Its hierarchical tree-viewer and advanced search functionality
make it intuitive to browse and administer your LDAP directory. Since
it is a web application, this LDAP browser works on many platforms,
making your LDAP server easily manageable from any location.
phpLDAPadmin is the perfect LDAP browser for the LDAP professional and
novice alike.

%description -l pl.UTF-8
phpLDAPadmin jest opartym o WWW klientem LDAP. Dostarcza łatwego,
ogólnie dostępnego, wielojęzykowego interfejsu administracyjnego do
serwera LDAP. Jego hierarchiczna przeglądarka struktur drzewiastych i
zaawansowane możliwosci wyszukiwania czynią go intuicyjnym dla
przeglądania i administrowania katalogami LDAP. Ponieważ jest
aplikacja webową, działa na wielu platformach, czyniąc serwer LDAP
łatwym do zarządzania z dowolnej lokalizacji. phpLDAPadmin jest
doskonałą przeglądarka LDAP zarówno dla profesjonalistów jak i
nowicjuszy.

%prep
%setup -q
%patch0 -p1

cat > apache.conf <<'EOF'
Alias /ldapadmin %{_appdir}/htdocs
<Directory %{_appdir}/htdocs>
	allow from all
</Directory>
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}

cp -a htdocs $RPM_BUILD_ROOT%{_appdir}
cp -a lib locale templates $RPM_BUILD_ROOT%{_appdir}
cp -a VERSION $RPM_BUILD_ROOT%{_appdir}
cp -a config/config.php.example	$RPM_BUILD_ROOT%{_sysconfdir}/config.php
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc doc/*
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%{_appdir}
