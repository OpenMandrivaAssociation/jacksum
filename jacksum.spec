# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support 1
%define section free

Name:           jacksum
Version:        1.7.0
Release:        %mkrel 5
Epoch:          0
Summary:        Software for computing and verifying checksums, CRC's, and message digests
License:        GPL
URL:            http://www.jonelo.de/java/jacksum/
Group:          Development/Java
#Vendor:         JPackage Project
#Distribution:   JPackage
Source0:        http://osdn.dl.sourceforge.net/jacksum/jacksum-1.7.0.zip
Source1:        %{name}
Patch0:         %{name}-javadoc.patch
BuildRequires:  ant
BuildRequires:  jpackage-utils >= 0:1.5
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Jacksum is a free and platform independent software for computing and 
verifying checksums, CRC's, and message digests (known as hash values 
and fingerprints). "Jacksum" is a synthetic word made of JAva and 
ChecKSUM.

Jacksum supports 46 popular algorithms (Adler32, BSD sum, POSIX cksum, 
Bzip2's CRC, CRC-8, CRC-16, CRC-24, CRC-32 (FCS-32), CRC-64, ELF-32, 
eMule/eDonkey, FCS-16, GOST R 34.11-94, HAS-160, HAVAL (3/4/5 passes, 
128/160/192/224/256 bits), MD2, MD4, MD5, MPEG-2's CRC-32, RIPEMD-128, 
RIPEMD-160, RIPEMD-256, RIPEMD-320, SHA-0, SHA-1, SHA-224, SHA-256, 
SHA-384, SHA-512, Tiger-128, Tiger-160, Tiger, Tiger2, Unix System V 
sum, sum8, sum16, sum24, sum32, Whirlpool-0, Whirlpool-1, Whirlpool and 
xor8).

Jacksum supports the "Rocksoft (tm) Model CRC Algorithm", it can 
calculate customized CRC algorithms and it supports the combination of 
multiple algorithms.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -c
%{__perl} -pi -e 's/\r$//g' history.txt license.txt readme_de.txt readme.txt docs/*
pushd source
%{_bindir}/unzip -qq %{name}-src.zip
popd
%patch0 -p1
%{__perl} -pi -e 's|<javadoc|<javadoc source="1.4"|g' build.xml

%build
pushd source
%{ant} jar #javadoc
popd

%install
%{__rm} -rf %{buildroot}

# bin
%{__mkdir_p} %{buildroot}%{_bindir}
%{__cp} -a %{SOURCE1} %{buildroot}%{_bindir}/%{name}

# jars
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a source/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; do %{__ln_s} ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
#%{__cp} -a source/javadoc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc history.txt license.txt readme_de.txt readme.txt docs/*
%attr(0755,root,root) %{_bindir}/%{name}
%{_javadir}/%{name}*.jar
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}
%doc %{_javadocdir}/%{name}-%{version}
