#  Copyright 2007-2011 GRAHAM DUMPLETON
# 
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

APXS = /usr/bin/apxs2
PYTHON = python

DESTDIR = 
LIBEXECDIR = /usr/lib/apache2/modules

CPPFLAGS =    
CFLAGS =  -Wc,-g -Wc,-O2 
LDFLAGS =  -L -L 
LDLIBS =  -lpython  

SRCFILES = src/server/mod_wsgi.c src/server/wsgi_*.c

all : src/server/mod_wsgi.la

src/server/mod_wsgi.la : $(SRCFILES)
	$(APXS) -c $(CPPFLAGS) $(CFLAGS) $(SRCFILES) $(LDFLAGS) $(LDLIBS)

$(DESTDIR)$(LIBEXECDIR) :
	mkdir -p $@

install : all $(DESTDIR)$(LIBEXECDIR)
	$(APXS) -i -S LIBEXECDIR=$(DESTDIR)$(LIBEXECDIR) -n 'mod_wsgi' src/server/mod_wsgi.la

clean :
	-rm -rf src/server/.libs
	-rm -f src/server/*.o
	-rm -f src/server/*.la
	-rm -f src/server/*.lo
	-rm -f src/server/*.slo
	-rm -f src/server/*.loT
	-rm -f config.log
	-rm -f config.status
	-rm -rf autom4te.cache
	-rm -rf mod_wsgi.egg-info
	-rm -rf build
	-rm -rf dist

distclean : clean
	-rm -f Makefile
	-rm -f apxs libtool
	-rm -rf .Python bin lib include
	-rm -rf .tox

realclean : distclean
	-rm -f configure
