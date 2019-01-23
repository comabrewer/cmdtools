## TODO

### Command line tools

- avoid crash because of premature get position
  - buffer unexpected input, read until end of position

- add prompt to readline
  - everything for "complete line" will be up to prompt only

- later: add read_line with notion of token
  - find next space or endline
  - can be used for navigatable drop-down menu

- Finish autocomplete
  - Implement options
  	- bash-like
  	  - expand on tab to first guess
  	  - show alternives on second tab
    - cycle
      - expand on tab to first guess
      - cycle through guess


    - google-like
      - expand auto to first guess (set counter)
      - show alteratives auto (arrows+enter)
      - send on enter
    - sublime-like 
      - expand auto
      - show alternatives immediatly (arrows+enter)
  
  - completion after some idle time, or triggered by tab
  - handle CTRL+C and other control characters

  - kbhit enables ctrl+c?
