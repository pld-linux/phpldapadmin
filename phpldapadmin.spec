Summary:	phpldapadmin - a web-based LDAP client
Summary(pl):	phpldapadmin - klient WWW dla LDAP
Name:		phpldapadmin
Version:	0.9.6c
Release:	0.3
License:	GPL
Group:		Applications/Networking
Source0:	http://dl.sourceforge.net/phpldapadmin/%{name}-%{version}.tar.gz
# Source0-md5:	8404fa6f0ad3185cc9353c94bf44ae56
URL:		http://phpldapadmin.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	php-ldap
Requires:	php-pcre
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

%description -l pl
phpLDAPadmin jest opartym o WWW klientem LDAP. Dostarcza ³atwego,
ogólnie dostêpnego, wielojêzykowego interfejsu administracyjnego do
serwera LDAP. Jego hierarchiczna przegl±darka struktur drzewiastych i
zaawansowane mo¿liwosci wyszukiwania czyni± go intuicyjnym dla
przegl±dania i administrowania katalogami LDAP. Poniewa¿ jest
aplikacja webow±, dzia³a na wielu platformach, czyni±c serwer LDAP
³atwym do zarz±dzania z dowolnej lokalizacji. phpLDAPadmin jest
doskona³± przegl±darka LDAP zarówno dla profesjonalistów jak i
nowicjuszy.

%prep
%setup -q
cat > apache.conf <<'EOF'
Alias /ldapadmin %{_appdir}
<Directory %{_appdir}>
	allow from all
</Directory>
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}/{doc,images,lang/recoded,templates/{creation,modification}}}

install	doc/*				.
install	doc/*				$RPM_BUILD_ROOT%{_appdir}/doc
install	images/*.{png,jpg}		$RPM_BUILD_ROOT%{_appdir}/images
install	lang/*.php			$RPM_BUILD_ROOT%{_appdir}/lang
install	lang/recoded/*.php		$RPM_BUILD_ROOT%{_appdir}/lang/recoded
install	templates/*.php			$RPM_BUILD_ROOT%{_appdir}/templates
install	templates/creation/*.php	$RPM_BUILD_ROOT%{_appdir}/templates/creation
install	templates/modification/*.php	$RPM_BUILD_ROOT%{_appdir}/templates/modification
install	*.{css,js,php}	 		$RPM_BUILD_ROOT%{_appdir}
install	{ldap_error_codes.txt,VERSION}	$RPM_BUILD_ROOT%{_appdir}
install	config.php.example		$RPM_BUILD_ROOT%{_sysconfdir}/config.php
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
ln -sf	%{_sysconfdir}/config.php 	$RPM_BUILD_ROOT%{_appdir}/config.php

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1
%webapp_register apache %{_webapp}

%triggerun -- apache1
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc CREDITS ChangeLog pla-test-i18n.ldif README-translation.txt
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%{_appdir}
