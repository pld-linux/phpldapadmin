Summary:	phpldapadmin - a web-based LDAP client
Summary(pl):	phpldapadmin - klient WWW dla LDAP
Name:		phpldapadmin
Version:	0.9.4b
Release:	0.1
Epoch:		0
License:	GPL
Group:		Applications/Networking
Source0:	http://dl.sourceforge.net/phpldapadmin/%{name}-%{version}.tar.gz
# Source0-md5:	0aa6021da066c637e56354980dccddbe
Source1:	%{name}.conf
URL:		http://phpldapadmin.sourceforge.net/
Requires:	apache
Requires:	php
Requires:	php-ldap
Requires:	php-pcre
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _phpldapadmindir	%{_datadir}/%{name}
%define         _sysconfdir     	/etc/%{name}

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
	$RPM_BUILD_ROOT{%{_sysconfdir},/etc/httpd} \
	$RPM_BUILD_ROOT%{_phpldapadmindir}/{doc,images,lang/recoded,templates/{creation,modification}}

install	%{SOURCE1}			$RPM_BUILD_ROOT/etc/httpd
install	doc/*				.
install	doc/*				$RPM_BUILD_ROOT%{_phpldapadmindir}/doc
install	images/*.{png,jpg}		$RPM_BUILD_ROOT%{_phpldapadmindir}/images
install	lang/*.php			$RPM_BUILD_ROOT%{_phpldapadmindir}/lang
install	lang/recoded/*.php		$RPM_BUILD_ROOT%{_phpldapadmindir}/lang/recoded
install	templates/*.php			$RPM_BUILD_ROOT%{_phpldapadmindir}/templates
install	templates/creation/*.php	$RPM_BUILD_ROOT%{_phpldapadmindir}/templates/creation
install	templates/modification/*.php	$RPM_BUILD_ROOT%{_phpldapadmindir}/templates/modification
install	*.{css,js,php}	 		$RPM_BUILD_ROOT%{_phpldapadmindir}
install	{ldap_error_codes.txt,VERSION}	$RPM_BUILD_ROOT%{_phpldapadmindir}
install	config.php.example		$RPM_BUILD_ROOT%{_sysconfdir}/config.php

ln -sf	%{_sysconfdir}/config.php 	$RPM_BUILD_ROOT%{_phpldapadmindir}/config.php

rm -f	$RPM_BUILD_ROOT%{_phpldapadmindir}/config.php.example

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*phpldapadmin.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/phpldapadmin.conf" >> /etc/httpd/httpd.conf
elif [ -d /etc/httpd/httpd.conf ]; then
	mv -f /etc/httpd/%{name}.conf /etc/httpd/httpd.conf/99_%{name}.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
	/usr/sbin/apachectl restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	umask 027
	if [ -d /etc/httpd/httpd.conf ]; then
	    rm -f /etc/httpd/httpd.conf/99_%{name}.conf
	else
		grep -v "^Include.*phpldapadmin.conf" /etc/httpd/httpd.conf > \
			/etc/httpd/httpd.conf.tmp
		mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
		if [ -f /var/lock/subsys/httpd ]; then
		    	/usr/sbin/apachectl restart 1>&2
		fi
	fi
fi

%files
%defattr(644,root,root,755)
%doc CREDITS ChangeLog pla-test-i18n.ldif ROADMAP README-translation.txt
%dir %{_sysconfdir}
%attr(640,root,http) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*
%config(noreplace) %verify(not size mtime md5) /etc/httpd/%{name}.conf
%{_phpldapadmindir}
