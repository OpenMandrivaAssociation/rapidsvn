%define	major 3
%define	libname %mklibname svncpp %{major}
%define	oldlibname %mklibname rapidsvn 0
%define	develname %mklibname svncpp -d

Summary:	A cross-platform GUI for the Subversion concurrent versioning system
Name:		rapidsvn
Version:	0.12.0
Release:	14
License:	GPLv2+
Group:		Development/Other
URL:		http://rapidsvn.tigris.org
Source0:	http://www.rapidsvn.org/download/release/%{version}/%{name}-%{version}-1.tar.gz
Source1:	rapidsvn_logo.png
Patch1:		rapidsvn-0.12.0-linkage_fix.patch
BuildRequires:	apache-devel
BuildRequires:	doxygen
BuildRequires:	subversion-devel >= 1.2
BuildRequires:	subversion >= 1.2
BuildRequires:	libtool >= 1.4.2
BuildRequires:	wxgtku-devel
BuildRequires:	libxslt-proc
BuildRequires:	docbook-style-xsl
BuildRequires:	pkgconfig(neon)
BuildRequires:	imagemagick
BuildRequires:	pkgconfig(cppunit)
Requires(post):	%{libname} = %{version}-%{release}
Requires(preun): %{libname} = %{version}-%{release}
Requires:	subversion

%description
RapidSVN is a platform independent GUI client for the Subversion
revision system written in C++ using the wxWindows framework.

%package -n %{libname}
Summary:	RapidSVN shared SvnCpp C++ API libraries
Group:		System/Libraries

%description -n %{libname}
RapidSVN is a platform independent GUI client for the Subversion
revision system written in C++ using the wxWindows framework.

This package contains shared SvnCpp C++ API libraries for
RapidSVN.

%package -n %{develname}
Summary:	RapidSVN SvnCpp C++ API development libraries
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	libsvncpp-devel = %{version}-%{release}
Provides:	%{oldlibname}-devel = %{version}-%{release}

%description -n %{develname}
As part of the RapidSVN effort it became clear that it would make
the code easier to update and manage if the Subversion client C
API were wrapped in C++. This is where SvnCpp comes from. Right
now it has the following aspects of the C API have been
abstracted: authentication, logging, status, notification, and
properties. SvnCpp should provide an object-oriented programming
interface to any project that uses C++ or a SWIG-compatible
language like Python or Java. 

%prep
%setup -qn %{name}-%{version}-1
%patch1 -p1

cp %{SOURCE1} rapidsvn_logo.png

%build
#mkdir src/tests/svncpp; touch src/tests/svncpp/Makefile.in
aclocal; autoconf; libtoolize --automake --force; aclocal; automake -a

export CFLAGS="%{optflags} -fno-strict-aliasing"
export CXXFLAGS=$CFLAGS

%configure2_5x \
    --enable-shared \
    --disable-static \
    --with-svn-include=%{_includedir} \
    --with-svn-lib=%{_libdir} \
    --with-xsltproc=%{_bindir}/xsltproc \
    --with-apr-config=%{_bindir}/apr-1-config \
    --with-apu-config=%{_bindir}/apu-1-config

%make

%install
%makeinstall_std

# Mandriva Icons
%__install -d %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps

convert rapidsvn_logo.png -resize 16x16 %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
convert rapidsvn_logo.png -resize 32x32 %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert rapidsvn_logo.png -resize 48x48 %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

%__mkdir_p %{buildroot}%{_datadir}/applications
%__cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=RapidSVN
Comment=%{summary}
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Development;RevisionControl;
EOF

%__mv doc/svncpp/html .

%find_lang %{name}

%files -f %{name}.lang
%doc html AUTHORS ChangeLog NEWS README
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%{_includedir}/svncpp
%{_libdir}/*.so

%changelog
* Fri Jan 13 2012 Andrey Bondrov <abondrov@mandriva.org> 0.12.0-5mdv2012.0
+ Revision: 760741
- Fix BuildRequires and drop no longer needed patch2
- Rebuild against utf8 wxGTK2.8, spec cleanup

* Fri May 06 2011 Funda Wang <fwang@mandriva.org> 0.12.0-4
+ Revision: 669806
- db-devel is not needed

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Thu Dec 02 2010 Paulo Andrade <pcpa@mandriva.com.br> 0.12.0-3mdv2011.0
+ Revision: 605043
- Rebuild with apr with workaround to issue with gcc type based alias analysis

* Sun Jan 03 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 0.12.0-2mdv2010.1
+ Revision: 485920
- rebuild against db4.8

* Sun Nov 08 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 0.12.0-1mdv2010.1
+ Revision: 463068
- update to new version 0.12.0
- bump major from 1 to 3
- package translations
- spec file clean

* Sat Aug 08 2009 Oden Eriksson <oeriksson@mandriva.com> 0.10.0-2mdv2010.0
+ Revision: 411786
- rebuild

* Sun Jul 19 2009 Oden Eriksson <oeriksson@mandriva.com> 0.10.0-1mdv2010.0
+ Revision: 397469
- fix build
- 0.10.0
- rediffed one patch

* Sat Apr 11 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.8-3mdv2009.1
+ Revision: 366356
- rebuild

* Sun Mar 22 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.8-2mdv2009.1
+ Revision: 360321
- rebuilt against subversion-1.6.0

* Fri Mar 20 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.8-1mdv2009.1
+ Revision: 359228
- 0.9.8
- rediffed and dropped some patches

* Fri Feb 27 2009 Emmanuel Andry <eandry@mandriva.org> 0.9.6-6mdv2009.1
+ Revision: 345672
- use default neon
- build against db4.7

* Wed Jan 28 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 0.9.6-5mdv2009.1
+ Revision: 334705
- Patch2: fix build with -Werror=format-security (thx for patch neoclust)
- use Werror_cflags %%nil because providing a patch would took some time

* Fri Jul 11 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.6-5mdv2009.0
+ Revision: 233721
- fix linkage
- rebuild
- added a gcc43 patch from fedora

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue Apr 29 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 0.9.6-3mdv2009.0
+ Revision: 199327
- fix a typo in scriplets

* Tue Apr 29 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 0.9.6-2mdv2009.0
+ Revision: 198943
- fix scriplets (#40455)

* Sat Mar 29 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 0.9.6-1mdv2009.0
+ Revision: 191090
- update the tarball (upstream has messed it up)
- add missing buildrequires on libcppunit-devel
- install icons into fd.o compiliant directory
- bump %%major
- do not package INSTALL file
- disable static libraries
- disable strict-aliasing as it breaks the building
- spec file clean
- new version

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Wed Dec 26 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9.4-4mdv2008.1
+ Revision: 137972
- rebuilt against openldap-2.4.7 libs

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

* Tue Jul 17 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9.4-3mdv2008.0
+ Revision: 52874
- fix deps

  + Emmanuel Andry <eandry@mandriva.org>
    - drop debian menu


* Wed Jan 24 2007 Emmanuel Andry <eandry@mandriva.org> 0.9.4-2mdv2007.0
+ Revision: 113060
- build against wxGTK2.8 (upstream patch for this)

* Mon Dec 11 2006 Emmanuel Andry <eandry@mandriva.org> 0.9.4-1mdv2007.1
+ Revision: 94562
- New version 0.9.4

* Wed Aug 30 2006 Andreas Hasenack <andreas@mandriva.com> 0.9.3-0.r7466.3mdv2007.0
+ Revision: 58732
- bump release

* Wed Aug 30 2006 Andreas Hasenack <andreas@mandriva.com> 0.9.3-0.r7466.2mdv2007.0
+ Revision: 58726
- added docbook-style-xsl to buildrequires
- Import rapidsvn

* Mon Aug 28 2006 Emmanuel Andry <eandry@mandriva.org> 0.9.3-0.r7466.2mdv2007.0
- xdg menu

* Fri Jun 23 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.3-0.r7466.1mdv2007.0
- use a snap (r7466)

* Tue May 23 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-1mdk
- 0.9.2 (Major bugfixes)
- use their logo as the icon
- make it backportable (arp,apr-util)

* Mon Feb 13 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-2mdk
- make it buildrequire subversion so that the libsvn package is pulled in

* Sat Feb 11 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-1mdk
- 0.9.1
- build it against wxGTK2.6

* Mon Feb 06 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.0-4mdk
- actually make it compile, he he...

* Mon Feb 06 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.0-3mdk
- rebuild

* Wed Nov 30 2005 Oden Eriksson <oeriksson@mandriva.com> 0.9.0-2mdk
- rebuilt against openssl-0.9.8a

* Thu Oct 27 2005 Oden Eriksson <oeriksson@mandriva.com> 0.9.0-1mdk
- 0.9.0 (Major feature enhancements)
- fix deps

* Wed Aug 31 2005 Oden Eriksson <oeriksson@mandriva.com> 0.8.0-2mdk
- rebuilt against new openldap-2.3.6 libs

* Sun May 22 2005 Oden Eriksson <oeriksson@mandriva.com> 0.8.0-1mdk
- 0.8.0
- fix deps
- use new rpm-4.4.x pre,post magic

* Tue Feb 08 2005 Buchan Milne <bgmilne@linux-mandrake.com> 0.7.2-3mdk
- rebuild for ldap2.2_7

* Sat Feb 05 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.7.2-2mdk
- rebuilt against new openldap libs
- fix deps

* Mon Jan 17 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.7.2-1mdk
- 0.7.2
- fix deps

* Sat Jan 01 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.7.1-1mdk
- 0.7.1
- misc spec file fixes

* Wed Sep 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.6.0-2mdk
- make it compile on 10.0

* Thu Jul 29 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.6.0-1mdk
- 0.6.0
- reenable libtoolize

* Mon Feb 23 2004 Ben Reser <ben@reser.org> 0.5.0-1mdk
- 0.5.0 which works with subversion 0.37 and newer (including 1.0.0)
- Fix menu section.
- Drop patch for building against subversion 0.29.
- Change the name of the lib package to match the libname.

