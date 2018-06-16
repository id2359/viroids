LB=:'('
RB=:')'
DOT=:'.'

NB. How "arc-y" is the shape - more arcs = more bulges

NB. explicit version
arc=: 3 : '(+/DOT=y) % #y'

NB. implicit version:wq
arc2 =: (+/ @ (DOT&=))  % #

shape=:'.((((((((.((.((((((((...((((.((((((...((((.((((((..((((....((((((((((((((.((...(((((((...((((((((.....(((((((((...(((...(((((..(((((((.(((.((.((((.((..(((((..((.((((..((((.(((((....)))))...))))..)))).))..)))))..)).)))).))..))).))))))).)))))..))).)))))))))......))))).))).....))))))))))))))..))))))))).....))))..)))))).))))...))))))..))))...)))))))))))))))))).'




