#
# Makefile for OpenzWave Mac OS X applications
# Greg Satz

# GNU make only

# requires libudev-dev

.SUFFIXES:	.cpp .o .a .s

CC     := $(CROSS_COMPILE)gcc
CXX    := $(CROSS_COMPILE)g++
LD     := $(CROSS_COMPILE)g++
AR     := $(CROSS_COMPILE)ar rc
RANLIB := $(CROSS_COMPILE)ranlib

DEBUG_CFLAGS    := -Wall -Wno-format -g -DDEBUG
RELEASE_CFLAGS  := -Wall -Wno-unknown-pragmas -Wno-format -O3

DEBUG_LDFLAGS	:= -g

# Change for DEBUG or RELEASE
CFLAGS	:= -c $(DEBUG_CFLAGS)
LDFLAGS	:= $(DEBUG_LDFLAGS)

INCLUDES	:= -I ../source_library/src -I ../source_library/src/command_classes/ -I ../source_library/src/value_classes/ \
	-I ../source_library/src/platform/ -I ../source_library/h/platform/unix -I ../source_library/tinyxml/ -I ../source_library/hidapi/hidapi/
LIBS = $(wildcard ../source_library/lib/*.a)

%.o : %.cpp
	$(CXX) $(CFLAGS) $(INCLUDES) -o $@ $<

all: HomeZwave 

lib:
	$(MAKE) -C ../source_library/build/

HomeZwave:	Main.o lib
	$(LD) -o $@ $(LDFLAGS) $< $(LIBS) -pthread -ludev

clean:
	rm -f HomeZwave Main.o

XMLLINT := $(shell whereis -b xmllint | cut -c10-)

ifeq ($(XMLLINT),)
xmltest:	$(XMLLINT)
	$(error xmllint command not found.)
else
xmltest:	$(XMLLINT)
	@$(XMLLINT) --noout --schema ../source_library/config/zwcfg.xsd zwcfg_*.xml
	@$(XMLLINT) --noout --schema ../source_library/config/zwscene.xsd zwscene.xml
endif
