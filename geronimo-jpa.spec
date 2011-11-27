%global spec_ver 3.0
%global spec_name geronimo-jpa_%{spec_ver}_spec

Name:           geronimo-jpa
Version:        1.1.1
Release:        7
Summary:        Java persistence API implementation

Group:          Development/Java
License:        ASL 2.0
URL:            http://geronimo.apache.org/
# Unfortunately no source release was created in
# http://repo2.maven.org/maven2/org/apache/geronimo/specs/geronimo-jpa_3.0_spec/1.1.1/
# so we do:
# svn export http://svn.apache.org/repos/asf/geronimo/specs/tags/geronimo-jpa_3.0_spec-1.1.1
# tar caf geronimo-jpa_3.0_spec-1.1.1.tar.xz geronimo-jpa_3.0_spec-1.1.1
Source0:       %{spec_name}-%{version}.tar.xz

BuildRoot:     %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:     noarch

# This pulls in all of the required java and maven stuff
BuildRequires:  geronimo-parent-poms
BuildRequires:  maven-resources-plugin

Provides:       jpa_api = %{spec_ver}

Requires:       java >= 0:1.6.0
Requires:       geronimo-parent-poms

Requires(post): jpackage-utils
Requires(postun): jpackage-utils


%description
The Java Persistence API is a new programming model under EJB 3.0
specification (JSR220) for the management of persistence and
object/relational mapping with Java EE and Java SE. Geronimo JPA is
one implementation of this specification.


%package javadoc
Summary:   API documentation for %{name}
Group:     Development/Java
Requires:  jpackage-utils

%description javadoc
%{summary}.

%prep
%setup -q -n %{spec_name}-%{version}

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mvn-jpp \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install javadoc:javadoc


%install
rm -rf $RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{_javadir}

install -m 644 target/%{spec_name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar

(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# Also provide compat symlinks
pushd $RPM_BUILD_ROOT%{_javadir}
ln -sf %{name}-%{version}.jar %{spec_name}-%{version}.jar
ln -sf %{name}-%{version}.jar jpa.jar
popd

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
(cd $RPM_BUILD_ROOT%{_javadocdir} && ln -sf %{name}-%{version} %{name})

install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-%{name}.pom

%add_to_maven_depmap org.apache.geronimo.specs %{spec_name} %{version} JPP %{name}
%add_to_maven_depmap javax.persistence persistence-api %{spec_ver} JPP %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap

%postun
%update_maven_depmap


%files
%defattr(-,root,root,-)
%doc LICENSE.txt NOTICE.txt
%{_javadir}/*.jar
%config(noreplace) %{_mavendepmapfragdir}/%{name}
%{_mavenpomdir}/*.pom

%files javadoc
%defattr(-,root,root,-)
%doc LICENSE.txt NOTICE.txt
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}



