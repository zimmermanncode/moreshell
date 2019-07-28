*** Settings ***

Library   Process


*** Keywords ***

Run IPython Process
   [Arguments]   @{expressions}
   ${stdin} =   Catenate   SEPARATOR=\n   @{expressions}
   ${result} =   Run Process   python   -m   IPython   -c   ${stdin}
   ...   stdout=stdout.txt   stderr=stderr.txt
   Should Be Equal As Integers   ${result.rc}   0
   [Return]   ${result}   ${result.stdout}
