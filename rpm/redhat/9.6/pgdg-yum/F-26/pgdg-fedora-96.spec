Name:		pgdg-fedora96
Version:	9.6
Release:	4
Summary:	PostgreSQL 9.6.X PGDG RPMs for Fedora - Yum Repository Configuration
Group:		System Environment/Base
License:	BSD
URL:		https://yum.postgresql.org
Source0:	https://yum.postgresql.org/RPM-GPG-KEY-PGDG-96
Source2:	pgdg-96-fedora.repo
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
Requires:	fedora-release

%description
This package contains yum configuration for Fedora, and also the GPG
key for PGDG RPMs.

%prep
%setup -q  -c -T

%build

%install
%{__rm} -rf %{buildroot}

%{__install} -Dpm 644 %{SOURCE0} \
	%{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG-96

%{__install} -dm 755 %{buildroot}%{_sysconfdir}/yum.repos.d
%{__install} -pm 644 %{SOURCE2}  \
	%{buildroot}%{_sysconfdir}/yum.repos.d/

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/yum.repos.d/*
%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/*

%changelog
* Thu Dec 28 2017 Devrim Gündüz <devrim@gunduz.org> - 9.6-4
- Add separate repo for -debuginfo and -debugsource packages

* Sun Sep 25 2016 Devrim Gündüz <devrim@gunduz.org> - 9.6-3
- Website is now https, per #1742

* Tue Sep 20 2016 Devrim Gündüz <devrim@gunduz.org> - 9.6-2
- Add updates testing repo for RPMs and SRPMS. They are disabled
  by default.

* Fri Nov 13 2015 Devrim Gündüz <devrim@gunduz.org> - 9.6-1
- Initial set for 9.6

