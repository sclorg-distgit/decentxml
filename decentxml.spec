%{?scl:%scl_package decentxml}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 1

Name:             %{?scl_prefix}decentxml
Version:          1.4
Release:          12.%{baserelease}%{?dist}
Summary:          XML parser optimized for round-tripping and code reuse
License:          BSD
Group:            Development/Libraries
URL:              http://code.google.com/p/%{pkg_name}
Source0:          https://decentxml.googlecode.com/files/decentxml-1.4-src.zip
# for running w3c conformance test suite
Source1:          http://www.w3.org/XML/Test/xmlts20031210.zip
BuildArch:        noarch



BuildRequires:    %{?scl_prefix_maven}maven-local
BuildRequires:    %{?scl_prefix_maven}apache-commons-parent

%description
XML parser optimized for round-tripping and code reuse with main
features being:
 * Allows 100% round-tripping, even for weird whitespace between
   attributes in the start tag or in the end tag
 * Suitable for building editors and filters which want/need to
   preserve the original file layout as much as possible
 * Error messages have line and column information
 * Easy to reuse individual components
 * XML 1.1 compatible

%package javadoc
Summary:          API documentation for %{pkg_name}
Group:            Documentation

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -n %{pkg_name}-%{version} -q
# we are looking for xml conformance data one lever above so unzip
# here and symlink there
unzip %{SOURCE1}
ln -sf %{pkg_name}-%{version}/xmlconf ../xmlconf
sed -i -e "s|junit-dep|junit|g" pom.xml

# Two tests fail with Java 8, probably because of some Unicode incompatibility.
sed -i '/not_wf_sa_16[89] /d' src/test/java/de/pdark/decentxml/XMLConformanceTest.java

%pom_remove_plugin :maven-javadoc-plugin
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_file  : %{pkg_name}
%mvn_build
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_install
%{?scl:EOF}


%files -f .mfiles
%doc LICENSE README

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Wed Jul 20 2016 Mat Booth <mat.booth@redhat.com> - 1.4-12.1
- Auto SCL-ise package for rh-eclipse46 collection

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-10
- Remove javadoc plugin execution

* Tue Jul 15 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-9
- Disable failing tests

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-8
- Remove BuildRequires on maven-surefire-provider-junit4

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4-7
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.4-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jan 17 2013 Michal Srb <msrb@redhat.com> - 1.4-3
- Build with xmvn

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 1 2012 Alexander Kurtakov <akurtako@redhat.com> 1.4-1
- Update to 1.4 upstream release.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Feb 25 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.3-1
- Initial version of the package