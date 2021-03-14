#!/bin/bash
BUILDDIR=.aws-sam/build
FUNCTION=PrAutolabellerFunction
HANDLER=$BUILDDIR/$FUNCTION/handler.py

[ -d $BUILDDIR/$FUNCTION/ptvsd ] || pip install ptvsd -t $BUILDDIR/$FUNCTION

if ! grep -q ptvsd $HANDLER; then
    cat - $HANDLER > $HANDLER.temp <<EOF
import ptvsd
ptvsd.enable_attach(address=('0.0.0.0', 5890), redirect_output=True)
ptvsd.wait_for_attach()
EOF
    mv $HANDLER.temp $HANDLER
fi

sam local invoke -e events/basic.json -d 5890 $FUNCTION
