%global sname passlib

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} > 25
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif
%if 0%{?rhel} == 6
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif
%if 0%{?rhel} == 7
%{!?with_python3:%global with_python3 0}
%global __ospython %{_bindir}/python2
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%if 0%{?with_python3}
Name:		pgadmin4-python3-%{sname}
%else
Name:		pgadmin4-python-%{sname}
%endif
Version:	1.7.1
Release:	1%{?dist}
Summary:	Comprehensive password hashing framework supporting over 20 schemes

License:	BSD and Beerware and Copyright only
URL:		http://%{sname}.googlecode.com
Source0:	https://files.pythonhosted.org/packages/source/p/%{sname}/%{sname}-%{version}.tar.gz

BuildArch:	noarch

%if 0%{?fedora} > 25
BuildRequires:	python3-devel python3-setuptools
%endif

%if 0%{?rhel} == 6
Obsoletes:	pgadmin4-python-%{sname} <= 1.6.2
BuildRequires:	python34-devel python34-setuptools
%endif

%if 0%{?rhel} == 7
BuildRequires:	python2-devel python-setuptools
%endif

%description
%{sname} is a password hashing library for Python 2 & 3, which provides
cross-platform implementations of over 20 password hashing algorithms,
as well as a framework for managing existing password hashes. It's
designed to be useful for a wide range of tasks, from verifying a hash
found in /etc/shadow, to providing full-strength password hashing for
multi-user application.


%prep
%setup -q -n %{sname}-%{version}

%build
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}

%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%if 0%{?with_python3}
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/%{sname} %{buildroot}%{python3_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
%else
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/%{sname} %{buildroot}%{python2_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
%endif

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE README
%else
%license LICENSE
%doc README
%endif
%if 0%{?with_python3}
%{pgadmin4py3instdir}/*%{sname}*.egg-info
%{pgadmin4py3instdir}/%{sname}
%else
%{pgadmin4py2instdir}/*%{sname}*.egg-info
%{pgadmin4py2instdir}/%{sname}
%endif

%changelog
* Tue Apr 10 2018 Devrim Gündüz <devrim@gunduz.org> - 1.7.1-1
- Update to 1.7.1

* Thu Apr 5 2018 Devrim Gündüz <devrim@gunduz.org> - 1.6.2-4
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the dependencies for that.

* Wed Apr 12 2017 Devrim Gündüz <devrim@gunduz.org> - 1.6.2-3
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Thu Mar 16 2017 Devrim Gündüz <devrim@gunduz.org> - 1.6.2-2
- Initial packaging for PostgreSQL YUM repository, to satisfy
  dependency of pgadmin4. Spec file is from EPEL 7.
