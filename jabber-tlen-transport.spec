Summary:	Tlen transport module for Jabber
Summary(pl):	Modu³ transportowy Tlen dla systemu Jabber
Name:		jabber-tlen-transport
Version:	0.3.6
Release:	2
License:	GPL v2
Group:		Applications/Communications
Source0:	http://dl.sourceforge.net/jtlentrans/tt-%{version}.tar.bz2
# Source0-md5:	b8683f36db7521cfc1a04ca86e90e5d8
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://sourceforge.net/projects/jtlentrans/
BuildRequires:	expat-devel
BuildRequires:	libtlen-devel
BuildRequires:	libxode-devel
BuildRequires:	openssl-devel
Requires(pre):	jabber-common
Requires(post,preun):	/sbin/chkconfig
Requires(post):	/usr/bin/perl
Requires:	jabber-common
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module allows Jabber to communicate with Tlen server.

%description -l pl
Modu³ ten umo¿liwia u¿ytkownikom Jabbera komunikowanie siê z
u¿ytkownikami komunikatora Tlen.

%prep
%setup -q -n tt-%{version}

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/jabber,/etc/rc.d/init.d,/etc/sysconfig,/var/lib/jabber/tlen}

%{__make} install \
	DESTDIR="$RPM_BUILD_ROOT"

mv $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{_sbindir}

install tt.example.xml $RPM_BUILD_ROOT%{_sysconfdir}/jabber/jabber-tlen-transport.xml
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/jabber-tlen-transport
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/jabber-tlen-transport

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/jabber/secret ] ; then
	SECRET=`cat /etc/jabber/secret`
	if [ -n "$SECRET" ] ; then
		echo "Updating component authentication secret in jabber-tlen-transport.xml..."
		perl -pi -e "s/>secret</>$SECRET</" /etc/jabber/jabber-tlen-transport.xml
	fi
fi
/sbin/chkconfig --add jabber-tlen-transport
if [ -r /var/lock/subsys/jabber-tlen-transport ]; then
	/etc/rc.d/init.d/jabber-tlen-transport restart >&2
else
	echo "Run \"/etc/rc.d/init.d/jabber-tlen-transport start\" to start Jabber Tlen transport."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/jabber-tlen-transport ]; then
		/etc/rc.d/init.d/jabber-tlen-transport stop >&2
	fi
	/sbin/chkconfig --del jabber-tlen-transport
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog DEBUG DONE README THANKS TODO
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,jabber) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/jabber/jabber-tlen-transport.xml
%attr(754,root,root) /etc/rc.d/init.d/jabber-tlen-transport
%attr(770,root,jabber) /var/lib/jabber/tlen
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/jabber-tlen-transport
