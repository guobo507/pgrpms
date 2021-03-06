%global sname hdfs_fdw
%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	PostgreSQL Foreign Data Wrapper (FDW) for the hdfs
Name:		%{sname}_%{pgmajorversion}
Version:	2.0.3
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/EnterpriseDB/%{sname}/archive/v%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/EnterpriseDB/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	libxml2-devel java-devel
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
the hdfs.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
export JDK_INCLUDE="/etc/alternatives/java_sdk_openjdk/include"
export JRE_LIBDIR="/usr/lib/jvm/jre-1.8.0-openjdk/lib/amd64/server"
export JVM_LIB="/usr/lib/jvm/jre-1.8.0-openjdk/lib/amd64/server"
#export JVM_LIB="/etc/alternatives/jre_1.8.0_exports/lib/amd64/server"
pushd libhive
%{__make} %{?_smp_mflags}
popd

%{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

pushd libhive
%{__mkdir} -p %{buildroot}%{pginstdir}/lib
%{__make} %{?_smp_mflags} install INSTALL_DIR=%{buildroot}/%{pginstdir}/lib
popd

pushd libhive/jdbc
	%javac MsgBuf.java
	%javac HiveJdbcClient.java
	%jar cf HiveJdbcClient-1.0.jar *.class
	%{__cp} HiveJdbcClient-1.0.jar %{buildroot}%{pginstdir}/lib
popd

%{__make} USE_PGXS=1 %{?_smp_mflags} install INSTALL_DIR=%{buildroot} DESTDIR=%{buildroot}

# Install README file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__install} -m 755 README.md %{buildroot}%{pginstdir}/share/extension/README-%{sname}
%{__rm} -f %{buildroot}%{_docdir}/pgsql/extension/README.md

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(755,root,root,755)
%doc %{pginstdir}/share/extension/README-%{sname}
%{pginstdir}/lib/libhive.so
%{pginstdir}/lib/HiveJdbcClient-1.0.jar
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Wed Jan 3 2018 - Devrim Gündüz <devrim@gunduz.org> 2.0.3-1
- Update to 2.0.3

* Thu Jun 22 2017 - Devrim Gündüz <devrim@gunduz.org> 2.0.1-1
- Update to 2.0.1

* Tue Jan 17 2017 - Devrim Gündüz <devrim@gunduz.org> 2.0.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
