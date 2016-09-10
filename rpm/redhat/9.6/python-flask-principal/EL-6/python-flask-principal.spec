%if 0%{?fedora} > 21
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%else
%{!?with_python3:%global with_python3 0}
%global __ospython %{_bindir}/python2
%endif

%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

%global	pypi_name Flask-Principal
%global	sum Identity management for Flask applications
Name:		python-flask-principal
Version:	0.4.0
Release:	11%{?dist}
Summary:	%{sum}

Group:		Development/Languages
License:	MIT
URL:		https://pypi.python.org/pypi/%{pypi_name}
Source0:	https://pypi.python.org/packages/source/F/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# patch adding LICENSE to release tarball accepted upstream, will be included in the next version
Source1:	LICENSE

BuildArch:	noarch

%if 0%{?with_python2}
BuildRequires:	python2-devel
BuildRequires:	python2-setuptools
%endif

%if 0%{?with_python3}
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
%endif

%description
Flask-Principal provides a very loose framework to tie in authentication
and user information providers, often located in different parts of a web
application.

%if 0%{?with_python2}
%package -n python2-flask-principal
Summary:	%{sum}
Requires:	python-flask
Requires:	python-blinker
%{?python_provide:%python_provide python2-flask-principal}

%description -n python2-flask-principal
Flask-Principal provides a very loose framework to tie in authentication
and user information providers, often located in different parts of a web
application.
%endif

%if 0%{?with_python3}
%package -n python3-flask-principal
Summary:	%{sum}
Requires:	python3-flask
Requires:	python3-blinker
%{?python_provide:%python_provide python3-flask-principal}

%description -n python3-flask-principal
Flask-Principal provides a very loose framework to tie in authentication
and user information providers, often located in different parts of a web
application.
%endif

%prep
%setup -q -n %{pypi_name}-%{version}
%{__rm} -rf %{pypi_name}.egg-info
%{__cp} %{SOURCE1} .

%build
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install --skip-build --root %{buildroot}

%clean
%{__rm} -rf %{buildroot}

%if 0%{?with_python2}
%files -n python2-flask-principal
%doc LICENSE README.rst
%{python2_sitelib}/*
%endif

%if 0%{?with_python3}
%files -n python3-flask-principal
%doc LICENSE README.rst
%{python3_sitelib}/*
%endif

%changelog
* Fri Sep 2 2016 Devrim Gündüz <devrim@gunduz.org> 0.4.0-11
- Update spec for pgadmin4 dependency

* Tue Jul 26 2016 Athos Coimbra Ribeiro <ribeiro@fedoraproject.org> - 0.4.0-10
- Add python 2 and 3 subpackages

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-9
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 12 2013  Richard Marko <rmarko@fedoraproject.org> - 0.4.0-5
- Added missing LICENSE file

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 07 2013 Richard Marko <rmarko@fedoraproject.org> - 0.4.0-3
- Removed upstream egg

* Thu Jul 04 2013 Richard Marko <rmarko@fedoraproject.org> - 0.4.0-2
- Added python-setuptools to BuildRequires
- Added python-blinker to Requires
- Fixed Summary

* Tue Jul 02 2013 Richard Marko <rmarko@fedoraproject.org> - 0.4.0-1
- Initial packaging attempt