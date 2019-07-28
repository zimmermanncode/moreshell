*** Settings ***

Library   Collections
Library   String

Resource   ./ipython.robot


*** Test Cases ***

Run %test_moreshell w/o flags
   ${result}   ${output} =   Run IPython Process
   ...   %load_ext moreshell.test
   ...   %test_moreshell
   @{expected test modules} =   Create List
   ...   magic.py
   ...   test_magic.py
   ...   test_module.py
   @{matches} =   Get Regexp Matches   ${output}
   ...   moreshell[/\\\\](?P<module>\\S+) \\.+\\s+\\[\\s?\\d+%\\]
   ...   module
   Should Be Equal   ${expected test modules}   ${matches}

Run %test_moreshell --verbose
   ${result}   ${output} =   Run IPython Process
   ...   %load_ext moreshell.test
   ...   %test_moreshell --verbose
   @{expected test modules} =   Create List
   ...   magic.py
   ...   test_magic.py
   ...   test_module.py
   ${regexp} =   Catenate   SEPARATOR=
   ...   moreshell[/\\\\](?P<module>[^\\s:]+)::\\S+
   ...   \\s+PASSED\\s+\\[\\s?\\d+%\\]
   @{matches} =   Get Regexp Matches   ${output}   ${regexp}   module
   ${matches} =   Remove Duplicates   ${matches}
   Should Be Equal   ${expected test modules}   ${matches}

Run %test_moreshell --coverage
   ${result}   ${output} =   Run IPython Process
   ...   %load_ext moreshell.test
   ...   %test_moreshell --coverage
   @{expected test modules} =   Create List
   ...   magic.py
   ...   test_magic.py
   ...   test_module.py
   @{matches} =   Get Regexp Matches   ${output}
   ...   moreshell[/\\\\](?P<module>\\S+) \\.+\\s+\\[\\s?\\d+%\\]
   ...   module
   Should Be Equal   ${expected test modules}   ${matches}
   Should Match Regexp   ${output}
   ...   TOTAL\\s+\\d+\\s+0\\s+100%

Run %test_moreshell --verbose --coverage
   ${result}   ${output} =   Run IPython Process
   ...   %load_ext moreshell.test
   ...   %test_moreshell --verbose --coverage
   @{expected test modules} =   Create List
   ...   magic.py
   ...   test_magic.py
   ...   test_module.py
   ${regexp} =   Catenate   SEPARATOR=
   ...   moreshell[/\\\\](?P<module>[^\\s:]+)::\\S+
   ...   \\s+PASSED\\s+\\[\\s?\\d+%\\]
   @{matches} =   Get Regexp Matches   ${output}   ${regexp}   module
   ${matches} =   Remove Duplicates   ${matches}
   Should Be Equal   ${expected test modules}   ${matches}
   Should Match Regexp   ${output}
   ...   TOTAL\\s+\\d+\\s+0\\s+100%
