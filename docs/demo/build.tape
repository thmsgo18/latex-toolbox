# Feature GIF: compile a project to PDF from the terminal.
# Regenerate with: ./docs/demo/record.sh  (from the repo root)

Output docs/assets/demo-build.gif

Set FontSize 15
Set Width 1100
Set Height 460
Set Padding 18
Set Theme "Catppuccin Mocha"
Set TypingSpeed 45ms

# Prepare a project off-camera.
Hide
Type "rm -rf /tmp/forge-demo2 && mkdir -p /tmp/forge-demo2 && cd /tmp/forge-demo2 && latex-forge create --name my-doc --template blank >/dev/null 2>&1 && clear"
Enter
Sleep 5s
Show

Type "latex-forge build my-doc"
Sleep 600ms
Enter
Sleep 25s
Sleep 4s
