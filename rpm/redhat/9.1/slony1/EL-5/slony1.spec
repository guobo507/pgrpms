%global pginstdir /usr/pgsql-9.1
%global pgmajorversion 91
%global sname	slony1
%{!?docs:%global docs 0}

Summary:	A "master to multiple slaves" replication system with cascading and failover
Name:		%{sname}-%{pgmajorversion}
Version:	2.0.8
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
URL:		http://main.slony.info/
Source0:	http://main.slony.info/downloads/2.0/source/%{sname}-%{version}.tar.bz2
Source2:	filter-requires-perl-Pg.sh
BuildRoot:	%{_tmppath}/%{sname}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	postgresql%{pgmajorversion}-devel, postgresql%{pgmajorversion}-server, initscripts, byacc, flex
Requires:	postgresql%{pgmajorversion}-server, perl-DBD-Pg
Conflicts:	slony1

%if %docs
BuildRequires:	docbook-style-dsssl postgresql_autodoc docbook-utils
%endif

%description
Slony-I is a "master to multiple slaves" replication 
system for PostgreSQL with cascading and failover.

The big picture for the development of Slony-I is to build
a master-slave system that includes all features and
capabilities needed to replicate large databases to a
reasonably limited number of slave systems.

Slony-I is a system for data centers and backup
sites, where the normal mode of operation is that all nodes
are available

%if %docs
%package docs
Summary:	Documentation for Slony-I
Group:		Applications/Databases
Requires:	%{sname}-%{pgmajorversion}
BuildRequires:	libjpeg, netpbm-progs, groff, docbook-style-dsssl, ghostscript
Obsoletes:	slony1-docs

%description docs
The slony1-docs package includes some documentation for Slony-I.
%endif

%global __perl_requires %{SOURCE2}

%prep
%setup -q -n %{sname}-%{version}
%build

# Fix permissions of docs.
%if %docs
find doc/ -type f -exec chmod 600 {} \;
%endif

CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS
CPPFLAGS="${CPPFLAGS} -I%{_includedir}/et -I%{_includedir}" ; export CPPFLAGS
CFLAGS="${CFLAGS} -I%{_includedir}/et -I%{_includedir}" ; export CFLAGS

export LIBNAME=%{_lib}
%configure --prefix=%{pginstdir} --includedir %{pginstdir}/include --with-pgconfigdir=%{pginstdir}/bin --libdir=%{pginstdir}/lib \
	--with-perltools=%{pginstdir}/bin \
%if %docs
	--with-docs --with-docdir=%{_docdir}/%{sname}-%{version} \
%endif
	--datadir=%{pginstdir}/share --with-pglibdir=%{pginstdir}/lib 

make %{?_smp_mflags}
make %{?_smp_mflags} -C tools

%install
rm -rf %{buildroot}
make %{?_smp_mflags} DESTDIR=%{buildroot} install

# Install sample slon.conf file
install -m 0644 share/slon.conf-sample %{buildroot}%{_sysconfdir}/slon.conf
install -m 0644 tools/altperl/slon_tools.conf-sample %{buildroot}%{_sysconfdir}/slon_tools.conf

# change file modes of docs.
/bin/chmod 644 COPYRIGHT UPGRADING SAMPLE HISTORY-1.1 RELEASE

# Install init script
install -d %{buildroot}%{_initrddir}
install -m 755 redhat/slony1.init %{buildroot}%{_initrddir}/%{sname}-%{pgmajorversion}

# Temporary measure for 1.2.X
%if %docs
	rm -f doc/implementation/.cvsignore
	rm -f doc/concept/.cvsignore
%endif

cd tools
make %{?_smp_mflags} DESTDIR=%{buildroot} install
/bin/rm -f %{buildroot}%{_sysconfdir}/slon_tools.conf-sample
# Perform some cleanup
/bin/rm -f %{buildroot}%{_datadir}/pgsql/*.sql
/bin/rm -f %{buildroot}%{_libdir}/slony1_funcs.so

%clean
rm -rf %{buildroot}

%post
chkconfig --add slony1-91
if [ ! -e "/var/log/slony1-91" -a ! -h "/var/log/slony1-91" ]
then
        mkdir /var/log/slony1-91
        chown postgres:postgres /var/log/slony1-91
fi

%preun
if [ $1 = 0 ] ; then
	/sbin/service slony1-91 condstop >/dev/null 2>&1
	chkconfig --del slony1-91
fi

%postun
if [ $1 -ge 1 ]; then
	/sbin/service slony1-91 condrestart >/dev/null 2>&1
fi

%files
%defattr(-,root,root,-)
%attr(644,root,root) %doc COPYRIGHT UPGRADING HISTORY-1.1 INSTALL SAMPLE RELEASE
%{pginstdir}/bin/slon*
%{pginstdir}/lib/slon*
%{pginstdir}/share/slon*
%config(noreplace) %{_sysconfdir}/slon.conf
%config(noreplace) %{_sysconfdir}/slon_tools.conf
%attr(755,root,root) %{_initrddir}/slony1-%{pgmajorversion}

%if %docs
%files docs
%attr(644,root,root) %doc doc/adminguide  doc/concept  doc/howto  doc/implementation  doc/support
%endif

%changelog
* Wed May 21 2014 Devrim Gündüzz <devrim@gunduz.org> 2.0.8-1
- Update to 2.0.8 

* Sun Feb 10 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 2.0.7-3
- Rebuilt.

* Wed Oct 05 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 2.0.7-2
- Use correct pgmajorversion number, per report from Ger Timmens. .

* Fri Aug 12 2011 Devrim Gunduz <devrim@gunduz.org> 2.0.7-1
- Update to 2.0.7.

* Thu Dec 9 2010 Devrim Gunduz <devrim@gunduz.org> 2.0.6-1
- Update to 2.0.6

* Fri Oct 8 2010 Devrim Gunduz <devrim@gunduz.org> 2.0.5-1
- Update to 2.0.5

* Sat Sep 18 2010 Devrim Gunduz <devrim@gunduz.org> 2.0.4-1
- Update to 2.0.4, and perform a major cleanup and bugfix.
- Apply changes for 9.0+
- Update source2, to supress weird dependency for slon_tools.conf.

* Sat Apr 10 2010 Devrim Gunduz <devrim@gunduz.org> 2.0.3-1
- Update to 2.0.3
- Updated doc patch
- Rename log directory to slony, to match upstream default
- Apply many fixes to support multiple postmaster installation.

* Sat May 9 2009 Devrim Gunduz <devrim@gunduz.org> 2.0.2-1
- Update to 2.0.2
- Removed patch0 -- it is no longer needed.
- Added a temp patch to get rid of sgml error.
- Re-enable doc builds

* Sat Mar 14 2009 Devrim Gunduz <devrim@gunduz.org> 2.0.1-1
- Update to 2.0.1
- Create log directory,	per pgcore #77.

* Thu Jan 29 2009 Devrim Gunduz <devrim@gunduz.org> 2.0.0-3
- Add docbook-utils to BR.

* Sat Dec 13 2008 Devrim Gunduz <devrim@gunduz.org> 2.0.0-2
- Add a patch to fix build errors
- Temporarily update Source2, so that it will silence a dependency error.

* Tue Dec 2 2008 Devrim Gunduz <devrim@gunduz.org> 2.0.0-1
- Update to 2.0.0

* Mon Sep 22 2008 Devrim Gunduz <devrim@gunduz.org> 1.2.15-3
- Add dependency for perl-DBD-Pg, paer Xavier Bergade.

* Sun Sep 21 2008 Devrim Gunduz <devrim@gunduz.org> 1.2.15-2
- Fix dependency issues caused by latest commit.

* Fri Sep 12 2008 Devrim Gunduz <devtrim@CommandPrompt.com> 1.2.15-1
- Update to 1.2.15
- Install tools written in perl, too.

* Fri May 16 2008 Devrim Gunduz <devrim@gunduz.org> 1.2.14-1
- Update to 1.2.14

* Wed Apr 2 2008 Devrim Gunduz <devrim@gunduz.org> 1.2.13-2
- Fix init script name.

* Sun Feb 10 2008 Devrim Gunduz <devrim@gunduz.org> 1.2.13-1
- Update to 1.2.13

* Mon Dec 17 2007 Devrim Gunduz <devrim@gunduz.org> 1.2.12-2
- Add flex and byacc to buildrequires, per Michael Best

* Tue Nov 13 2007 Devrim Gunduz <devrim@gunduz.org> 1.2.12-1
- Update to 1.2.12

* Wed Aug 29 2007 Devrim Gunduz <devrim@gunduz.org> 1.2.11-1
- Update to 1.2.11
- Remove the word "engine" from init script name.

* Mon Aug 6 2007 Devrim Gunduz <devrim@gunduz.org> 1.2.10-2
- Fix Source0
- Spec file cleanup (removed macro for perltools)
- Added initscripts as BR.
- Fix doc package installation path (and ownership issue)

* Wed Jun 13 2007 Devrim Gunduz <devrim@gunduz.org> 1.2.10-1
- Update to 1.2.10

* Mon Jun 11 2007 Devrim Gunduz <devrim@gunduz.org> 1.2.9-3
- Add BuildRequires for docs subpackage, per #199154 (Thanks Ruben).

* Sun Jun 3 2007 Devrim Gunduz <devrim@gunduz.org> 1.2.9-2
- Some more fixes for Fedora review.
- Remove executable bits from docs.

* Thu May 17 2007 Devrim Gunduz <devrim@gunduz.org>
- Install init script with rpm.
- Fix --with-pgconfigdir parameter.
- Fix rpm build problem when the system has pg_config in both under
  /usr/local/pgsql/bin and /usr/bin

* Wed Mar 22 2007 Christopher Browne <cbbrowne@ca.afilias.info>
- Added more recent release notes

* Wed Mar 7 2007 Christopher Browne <cbbrowne@ca.afilias.info>
- Added more recent release notes

* Thu Jan 4 2007 Devrim Gunduz <devrim@gunduz.org>
- Add docs package (It should be added before but...)

* Wed Nov 8 2006 Devrim Gunduz <devrim@gunduz.org>
- On 64-bit boxes, both 32 and 64 bit -devel packages may be installed. 
  Fix version check script
- Revert tar name patch
- Macros cannot be used in various parts of the spec file. Revert that commit
- Spec file cleanup

* Tue Oct 31 2006 Trevor Astrope <astrope@sitesell.com>
- Fixup tar name and install slon-tools as slon-tools.pm

* Mon Jul 17 2006 Devrim Gunduz <devrim@gunduz.org> postgresql-slony1-engine
- Updated spec and cleaned up rpmlint errors and warnings

* Wed Dec 21 2005 Devrim Gunduz <devrim@gunduz.org> postgresql-slony1-engine
- Added a buildrhel3 macro to fix RHEL 3 RPM builds
- Added a kerbdir macro

* Wed Dec 14 2005 Devrim Gunduz <devrim@gunduz.org> postgresql-slony1-engine
- Fixed the spec file so that during upgrade, conf files will not be replaced, and a .rpmnew will be created.

* Thu Nov 24 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Created bindir

* Wed Oct 26 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Modify CPPFLAGS and CFLAGS to fix builds on RHEL -- Per Philip Yarra

* Tue Oct 18 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Created a new package : -docs and moved all the docs there.

* Tue Oct 18 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Fixed the problem in http://gborg.postgresql.org/pipermail/slony1-general/2005-October/003105.html

* Sat Oct 01 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Upgrade to 1.1.1

* Tue Jul 12 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Added a line to check postgresql RPM version and tag SlonyI RPM with it.
- Updated Requires files so that it checks correct PostgreSQL version
- Moved autoconf line into correct place.

* Thu Jun 08 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Added UPGRADING, HISTORY-1.1, INSTALL, SAMPLE among installed files, reflecting the change in GNUMakefile.in

* Thu Jun 02 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Apply a new %docs macro and disable building of docs by default.
- Remove slon-tools.conf-sample from bindir.
- Removed --bindir and --libdir, since they are not needed.

* Mon Apr 10 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- More fixes on RPM builds

* Thu Apr 07 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- More fixes on RPM builds

* Tue Apr 04 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Fix RPM build errors, regarding to tools/ .

* Thu Apr 02 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Added docs to installed files list.
- Added perltools, so that tools/altperl may be compiled.
- Updated the spec file

* Thu Mar 17 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Update to 1.1.0beta1
- Remove PostgreSQL source dependency

* Thu Mar 17 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Fix RPM builds

* Thu Mar 18 2004 Daniel Berrange <berrange@redhat.com> postgresql-slony1-engine
- Initial RPM packaging

