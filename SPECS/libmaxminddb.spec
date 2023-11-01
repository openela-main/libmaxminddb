Name:           libmaxminddb
Summary:        C library for the MaxMind DB file format
Version:        1.5.2
Release:        3%{?dist}
URL:            https://maxmind.github.io/libmaxminddb
Source:         https://github.com/maxmind/libmaxminddb/releases/download/%{version}/%{name}-%{version}.tar.gz

# original libmaxminddb code is Apache Licence 2.0
# src/maxminddb-compat-util.h is BSD
License:        ASL 2.0 and BSD

BuildRequires:  gcc
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  perl-interpreter
BuildRequires:  perl(FindBin)
BuildRequires:  make

%description
The package contains libmaxminddb library.

%package devel
Summary:        Development header files for libmaxminddb
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
The package contains development header files for the libmaxminddb library
and the mmdblookup utility which allows IP address lookup in a MaxMind DB file.

%prep
%autosetup
sed -i -e '/AM_CFLAGS=/d' common.mk
sed -i -e '/CFLAGS=/d' configure.ac

%build
autoreconf -vfi
%configure --disable-static
%make_build

%check
# tests are linked dynamically, preload the library as we have removed RPATH
LD_PRELOAD=%{buildroot}%{_libdir}/libmaxminddb.so make check

%install
%make_install
rm -v %{buildroot}%{_libdir}/*.la

#downstream fix for multilib install of devel pkg
mv %{buildroot}%{_includedir}/maxminddb_config.h \
   %{buildroot}%{_includedir}/maxminddb_config-%{__isa_bits}.h
cat > %{buildroot}%{_includedir}/maxminddb_config.h << EOF
#include <bits/wordsize.h>

#if __WORDSIZE == 32
#include <maxminddb_config-32.h>
#elif __WORDSIZE == 64
#include <maxminddb_config-64.h>
#else
#error "Unknown word size"
#endif
EOF

%files
%license LICENSE
%{_libdir}/libmaxminddb.so.0*
%{_bindir}/mmdblookup
%{_mandir}/man1/*.1*

%files devel
%license NOTICE
%doc Changes.md
%{_includedir}/maxminddb.h
%{_includedir}/maxminddb_config*.h
%{_libdir}/libmaxminddb.so
%{_libdir}/pkgconfig/libmaxminddb.pc
%{_mandir}/man3/*.3*

%changelog
* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 1.5.2-3
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 1.5.2-2
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Mar 16 2021 Michal Ruprich <mruprich@redhat.com> - 1.5.2-1
- Update to 1.5.2

* Tue Jan 26 2021 Michal Ruprich <mruprich@redhat.com> - 1.5.0-1
- Update to 1.5.0

* Thu Dec 10 2020 Michal Ruprich <mruprich@redhat.com> - 1.4.3-1
- Update to 1.4.3
- Resolves: #1758843 - libmaxminddb-devel i686 can't be installed in parallel to x86_64
- Fix for CVE-2020-28241

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 02 2020 Michal Ruprich <michalruprich@gmail.com> - 1.4.2-2
- Move manpage for mmdblookup from -devel to the main package

* Tue May 12 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.4.2-1
- Update to 1.4.2

* Mon Mar 30 2020 Michal Ruprich <mruprich@redhat.com> - 1.3.2-3
- Move mmdblookup binary from -devel to the main package

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct 21 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.2-1
- Update to 1.3.2

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Mar 27 2016 Jan Vcelak <jvcelak@fedoraproject.org> 1.2.0-1
- rebase to new version

* Mon Mar 21 2016 Jan Vcelak <jvcelak@fedoraproject.org> 1.1.5-1
- rebase to new version

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Sep 15 2015 Jan Vcelak <jvcelak@fedoraproject.org> 1.1.1-5
- add pkg-config file from the upcoming upstream version

* Mon Sep 14 2015 Jan Vcelak <jvcelak@fedoraproject.org> 1.1.1-4
- remove utils subpackage and place mmdblookup into devel subpackage
- remove Group from the spec file
- move NOTICE and Changes.md to devel subpackage

* Thu Sep 03 2015 Jan Vcelak <jvcelak@fedoraproject.org> 1.1.1-3
- updated package licence
- added --as-needed linker flag

* Tue Sep 01 2015 Jan Vcelak <jvcelak@fedoraproject.org> 1.1.1-1
- initial version of the package
