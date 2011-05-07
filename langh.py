#/usr/bin/env python
# -*- coding: utf-8 -*-

# First real implementation of Language's transcoder

### Enter Input code here
Input = \
""" {  < a+ >  =  ( b )  } """

### Parsing the Input

# Split in words
import re

#testing here
regex = re.compile(""" ( \s+ ) """)

#im trying to browse the input associating a brace with its nemesis along with raw text between…
#should look like this: { … } -> { <…> … } -> { <a+> = … } -> { <a+> = (b) } -> done
#i know i should make a loop and count the braces, but what if you'd like to use some odd-unicode brace ?
##uho, i thought python wouldn't be enough unicodish to let to the end-user the possibility to really use
##whatever unicode char he'd dream of.. or maybe it's my PHP past experiences that made me believe this!
##er.... in PHP, PCRE are like unicode-proof to PHP's string handling shit.. just look at my last try in PHP. END
test_1 =    """
        (  ######################################
            ( \(                    # ( : 2
                ( \[                # [ : 2 3
                    ( \{            # { : 2 3 4
                        ( \<        # < : 2 3 4 5
            )   )   )   )
 
            (.+)

# (?x … | …… )
# if x then … else ……

            (?2
                (?3
                    (?4
                        (?5 # 2 3 4 5
                            \>
                        | # 2 3 4
                            \}
                        )
                    | # 2 3
                        \]
                    )
                | # 2
                    \)
                )
            | # nothing - everything else
                [^\(\)\[\]\{\}\<\>]+
            )
        )*  #####################################
        #(?1 (a) | (\s+) )+
    """

tree = regex.findall(Input, re.S | re.X)

# Tree-ing the input
#isBlock = False
#
#for i in len(Input):
#    pass#

### Printing the Output
print Input
print '•••'
print tree

Output = ''
