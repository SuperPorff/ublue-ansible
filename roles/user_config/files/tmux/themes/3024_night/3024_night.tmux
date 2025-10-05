# 3024 Night Theme for tmux

# status bar
set-option -g status-style bg="#090300",fg="#a5a2a2"

# window titles
set-window-option -g window-status-style fg="#807d7c",bg=default,dim
set-window-option -g window-status-current-style fg="#01a252",bg=default,bright

# pane borders
set-option -g pane-border-style fg="#4a4543"
set-option -g pane-active-border-style fg="#01a0e4"

# message text
set-option -g message-style bg="#01a0e4",fg="#090300"

# pane number display
set-option -g display-panes-active-colour "#db2d20"
set-option -g display-panes-colour "#01a0e4"

# clock
set-window-option -g clock-mode-colour "#fded02"
