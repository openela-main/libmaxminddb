Name:           libmaxminddb
Summary:        C library for the MaxMind DB file format
Version:        1.2.0
Release:        10%{?dist}.1
URL:            https://maxmind.github.io/libmaxminddb
Source0:        https://github.com/maxmind/%{name}/releases/download/%{version}/%{name}-%{version}.tar.gz

# original libmaxminddb code is Apache Licence 2.0
# src/maxminddb-compat-util.h is BSD
License:        ASL 2.0 and BSD

BuildRequires:  perl-interpreter
Recommends:		geolite2-city, geolite2-country

Patch0000: 0000-CVE-2020-28241.patch

%description
The package contains libmaxminddb library.

%package devel
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig
#the only binary in -devel subpackage has been moved to the main package
#this means that the -devel-debuginfo pkg is missing and it would interrupt update path
Obsoletes:      libmaxminddb-devel-debuginfo < 1.2.0-8
Summary:        Development header files for libmaxminddb

%description devel
The package contains development header files for the libmaxminddb library
and the mmdblookup utility which allows IP address lookup in a MaxMind DB file.

%prep
%setup -q

%patch0000 -p1 -b .cve-2020-28241

%build
%configure --disable-static
# remove embeded RPATH
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# link only requried libraries
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
make %{?_smp_mflags}

%check
# tests are linked dynamically, preload the library as we have removed RPATH
LD_PRELOAD=%{buildroot}%{_libdir}/libmaxminddb.so make check

%install
%make_install
rm -fv %{buildroot}%{_libdir}/*.la

#fix multilib install of devel pkg
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


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license LICENSE
%{_libdir}/libmaxminddb.so.*
%{_bindir}/mmdblookup
%{_mandir}/man1/mmdblookup.1.gz

%files devel
%license NOTICE
%doc Changes.md
%{_includedir}/maxminddb.h
%{_includedir}/maxminddb_config*.h
%{_libdir}/libmaxminddb.so
%{_libdir}/pkgconfig/libmaxminddb.pc
%{_mandir}/man3/*

%changelog
* Thu Jan 04 2024 Michal Ruprich <mruprich@redhat.com> - 1.2.0-10.1
- Resolves: RHEL-20594 - improper initialization in dump_entry_data_list() in maxminddb.c

* Mon Jun 08 2020 Michal Ruprich <michalruprich@gmail.com> - 1.2.0-10
- Related: #1642001 - Obsoleting -devel-debuginfo to enable clean update path

* Mon May 25 2020 Michal Ruprich <michalruprich@gmail.com> - 1.2.0-9
- Related: #1642001 - moving manpage of mmdblookup from -devel subpackage

* Fri May 15 2020 Michal Ruprich <michalruprich@gmail.com> - 1.2.0-8
- Resolves: #1642001 - binary mmdblookup is in libmaxminddb-devel

* Thu Jan 09 2020 Michal Ruprich <mruprich@redhat.com> - 1.2.0-7
- Resolves: #1788956 - conflicts with multilib install

* Thu Aug 02 2018 Michal Ruprich <mruprich@redhat.com> - 1.2.0-6
- Adding libmaxminddb as a new package to RHEL-8 (rhbz#1607927)
- Adding Recommends tag for geolite2 databases

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
