# Hero GIF: create a project and show the result.
# Regenerate with: ./docs/demo/record.sh  (from the repo root)

Output docs/assets/demo-create.gif

Set FontSize 15
Set Width 1100
Set Height 460
Set Padding 18
Set Theme "Catppuccin Mocha"
Set TypingSpeed 45ms

# Work in a throwaway directory so the recording is reproducible.
Hide
Type "rm -rf /tmp/forge-demo && mkdir -p /tmp/forge-demo && cd /tmp/forge-demo && clear"
Enter
Show

Type "latex-forge create --name my-report --template project-report-en"
Sleep 800ms
Enter
Sleep 3s
# Decline the "Open project in VS Code?" prompt.
Enter
Sleep 1s

Type "ls my-report"
Sleep 500ms
Enter
Sleep 4s
