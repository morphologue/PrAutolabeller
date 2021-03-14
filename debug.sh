#!/bin/bash
BUILDDIR=.aws-sam/build
FUNCTION=PrAutolabellerFunction

pip install ptvsd -t $BUILDDIR/$FUNCTION

for SCRIPTFILE in $BUILDDIR/$FUNCTION/*.py; do
    awk '{ if ($0 !~ /^# Insert ptvsd debug magic here/) { print } else { print "import ptvsd\nptvsd.enable_attach(address=(\"0.0.0.0\", 5890), redirect_output=True)\nptvsd.wait_for_attach()" }}' $SCRIPTFILE > $SCRIPTFILE.temp
    mv $SCRIPTFILE.temp $SCRIPTFILE
done

sam local invoke -d 5890 -t $BUILDDIR/template.yaml -e events/basic.json $FUNCTION
