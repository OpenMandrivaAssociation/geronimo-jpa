%{?_javapackages_macros:%_javapackages_macros}
%global spec_ver 3.0
%global spec_name geronimo-jpa_%{spec_ver}_spec

Name:           geronimo-jpa
Version:        1.1.1
Release:        13.0%{?dist}
Summary:        Java persistence API implementation

License:        ASL 2.0
URL:            http://geronimo.apache.org/
# Unfortunately no source release was created in
# http://repo2.maven.org/maven2/org/apache/geronimo/specs/geronimo-jpa_3.0_spec/1.1.1/
# so we do:
# svn export http://svn.apache.org/repos/asf/geronimo/specs/tags/geronimo-jpa_3.0_spec-1.1.1
# tar caf geronimo-jpa_3.0_spec-1.1.1.tar.xz geronimo-jpa_3.0_spec-1.1.1
Source0:       %{spec_name}-%{version}.tar.xz

BuildArch:     noarch

# This pulls in all of the required java and maven stuff
BuildRequires:  maven-local
BuildRequires:  geronimo-parent-poms
BuildRequires:  maven-resources-plugin

Provides:       jpa_api = %{spec_ver}
Provides:       javax.persistence = %{spec_ver}


%description
The Java Persistence API is a new programming model under EJB 3.0
specification (JSR220) for the management of persistence and
object/relational mapping with Java EE and Java SE. Geronimo JPA is
one implementation of this specification.


%package javadoc
Summary:   API documentation for %{name}

%description javadoc
%{summary}.

%prep
%setup -q -n %{spec_name}-%{version}

%build
%mvn_file  : %{name} %{spec_name}-%{version} jpa
%mvn_alias : javax.persistence:persistence-api
%mvn_build

%install
%mvn_install

install -d -m 755 %{buildroot}%{_javadir}/javax.persistence/
ln -sf ../%{name}.jar %{buildroot}%{_javadir}/javax.persistence/

%files -f .mfiles
%doc LICENSE.txt NOTICE.txt
%{_javadir}/javax.persistence/

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt


%changelog
* Mon Aug 12 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1.1-13
- Add javax.mail provides and directory

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.1.1-10
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jan 17 2013 Michal Srb <msrb@redhat.com> - 1.1.1-9
- Build with xmvn

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1.1-6
- Build with Maven 3
- Fix packaging problems

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 30 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1.1-4
- Add geronimo-parent-poms to Requires

* Mon Jul 26 2010  <sochotnicky@redhat.com> - 1.1.1-3
- Fix whitespace warnings
- Use unversioned Requires on jpackage-utils

* Thu Jul 22 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1.1-2
- Add jpa.jar symlink
- Change persistance-api maven depmap version to %%{spec_ver}
- Renamed provides to jpa_api

* Tue Jul 20 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1.1-1
- Initial package
