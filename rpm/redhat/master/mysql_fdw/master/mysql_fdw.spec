%global sname mysql_fdw
%global mysqlfdwmajver 2
%global mysqlfdwmidver 2
%global mysqlfdwminver 0

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	PostgreSQL Foreign Data Wrapper (FDW) for the MySQL
Name:		%{sname}_%{pgmajorversion}
Version:	%{mysqlfdwmajver}.%{mysqlfdwmidver}.%{mysqlfdwminver}
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/EnterpriseDB/%{sname}/archive/REL-%{mysqlfdwmajver}_%{mysqlfdwmidver}_%{mysqlfdwminver}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/EnterpriseDB/mysql_fdw
BuildRequires:	postgresql%{pgmajorversion}-devel, mysql-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
This PostgreSQL extension implements a Foreign Data Wrapper (FDW) for
the MySQL.

%prep
%setup -q -n %{sname}-REL-%{mysqlfdwmajver}_%{mysqlfdwmidver}_%{mysqlfdwminver}
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
%{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__install} -m 755 README.md %{buildroot}%{pginstdir}/share/extension/README-%{sname}
%{__rm} -f %{buildroot}%{_docdir}/pgsql/extension/README.md

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%ifarch ppc64 ppc64le
	%{atpath}/sbin/ldconfig
%endif

%postun -p /sbin/ldconfig
%ifarch ppc64 ppc64le
	%{atpath}/sbin/ldconfig
%endif

%files
%defattr(755,root,root,755)
%doc %{pginstdir}/share/extension/README-%{sname}
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--1.0.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Tue Jan 17 2017 - Devrim Gündüz <devrim@gunduz.org> 2.1.2-1
- Update to 2.2.0

* Tue Feb 23 2016 - Devrim Gündüz <devrim@gunduz.org> 2.1.2-1
- Update to 2.1.2

* Thu Feb 05 2015 - Devrim Gündüz <devrim@gunduz.org> 2.0.1-1
- Update to 2.0.1

* Fri Oct 10 2014 - Devrim Gündüz <devrim@gunduz.org> 1.0.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
