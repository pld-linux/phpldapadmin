Summary:	phpldapadmin - a web-based LDAP client
Summary(pl):	phpldapadmin - klient WWW dla LDAP
Name:		phpldapadmin
Version:	0.9.6
Release:	0.1
Epoch:		0
License:	GPL
Group:		Applications/Networking
Source0:	http://dl.sourceforge.net/phpldapadmin/%{name}-%{version}.tar.gz
# Source0-md5:	db5eb502697712ebdaeb34766b6a7760
URL:		http://phpldapadmin.sourceforge.net/
Requires:	apache
Requires:	php-ldap
Requires:	php-pcre
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_datadir}/%{name}
%define		_confdir	%{_sysconfdir}/%{name}

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
serwera LDAP. Jego hierarchiczna przegl±darka struktur drzewiastych
i zaawansowane mo¿liwosci wyszukiwania czyni± go intuicyjnym dla
przegl±dania i administrowania katalogami LDAP. Poniewa¿ jest
aplikacja webow±, dzia³a na wielu platformach, czyni±c serwer LDAP
³atwym do zarz±dzania z dowolnej lokalizacji. phpLDAPadmin jest
doskona³± przegl±darka LDAP zarówno dla profesjonalistów jak 
i nowicjuszy.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT

install -d \
	$RPM_BUILD_ROOT{%{_confdir},%{_sysconfdir}/httpd} \
	$RPM_BUILD_ROOT%{_appdir}/{doc,images,lang/recoded,templates/{creation,modification}}

echo "Alias /ldapadmin %{_appdir}" >	$RPM_BUILD_ROOT%{_sysconfdir}/httpd/%{name}.conf
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
install	config.php.example		$RPM_BUILD_ROOT%{_confdir}/config.php

ln -sf	%{_confdir}/config.php 	$RPM_BUILD_ROOT%{_appdir}/config.php

rm -f	$RPM_BUILD_ROOT%{_appdir}/config.php.example

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f %{_sysconfdir}/httpd/httpd.conf ] && ! grep -q "^Include.*%{name}.conf" %{_sysconfdir}/httpd/httpd.conf; then
	echo "Include %{_sysconfdir}/httpd/%{name}.conf" >> %{_sysconfdir}/httpd/httpd.conf
elif [ -d %{_sysconfdir}/httpd/httpd.conf ]; then
	 ln -sf %{_sysconfdir}/httpd/%{name}.conf %{_sysconfdir}/httpd/httpd.conf/99_%{name}.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
	%{_sbindir}/apachectl restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	umask 027
	if [ -d %{_sysconfdir}/httpd/httpd.conf ]; then
		rm -f %{_sysconfdir}/httpd/httpd.conf/99_%{name}.conf
	else
		grep -v "^Include.*%{name}.conf" %{_sysconfdir}/httpd/httpd.conf > \
			%{_sysconfdir}/httpd/httpd.conf.tmp
		mv -f %{_sysconfdir}/httpd/httpd.conf.tmp %{_sysconfdir}/httpd/httpd.conf
		if [ -f /var/lock/subsys/httpd ]; then
			%{_sbindir}/apachectl restart 1>&2
		fi
	fi
fi

%files
%defattr(644,root,root,755)
%doc CREDITS ChangeLog pla-test-i18n.ldif README-translation.txt
%dir %{_confdir}
%attr(640,root,http) %config(noreplace) %verify(not size mtime md5) %{_confdir}/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd/%{name}.conf
%{_appdir}
