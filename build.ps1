$ErrorActionPreference = "Stop"

Write-Host "Activating Virtual Environment..."
.\venv\Scripts\activate

Write-Host "Wiping Global Claude CLI History to prevent context snowballing..."
Remove-Item -Path "$env:USERPROFILE\.claude\projects\*" -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Triggering Claude Code for Resume Generation..."
$LatexOutput = claude -p "Follow @instructions.md exactly. Read @job_listing.txt and @master.md. Use @template/template.tex as the read-only blueprint. Output ONLY the raw LaTeX code for the finalized resume. Do not output markdown formatting, backticks, code blocks, or conversational text. Output the raw text starting directly with \documentclass."
if ($LASTEXITCODE -ne 0) { Write-Host "Fatal Error: Claude generation failed."; exit 1 }

Write-Host "Writing LaTeX to Disk..."
$JoinedLatex = $LatexOutput -join "`n"
$CleanLatex =$JoinedLatex -replace "^```(latex|tex)?\s*", "" -replace "\s*```$", ""
[IO.File]::WriteAllText("$PWD\output\Zain_Usmani_Resume.tex", $CleanLatex, [System.Text.Encoding]::UTF8)

Write-Host "Extracting Metadata in RAM..."
$MetadataJson = claude -p "Read @job_listing.txt. Output strict JSON with keys 'Company' (short brand name only), 'Position' (minimal keywords for distinction only + 'Intern'), 'ReqID' (alphanumeric string only). Output raw JSON only. No markdown, no conversational text."
if ($LASTEXITCODE -ne 0) { Write-Host "Fatal Error: Claude metadata extraction failed."; exit 1 }
$JoinedJson =$MetadataJson -join "`n"

Write-Host "Saving Metadata..."
Write-Output $JoinedJson | python scripts\generate.py
if ($LASTEXITCODE -ne 0) { Write-Host "Fatal Error: generate.py failed."; exit 1 }

Write-Host "Generating Token Telemetry Dashboard..."
python scripts\track_tokens.py

Write-Host "`n========================================================="
Write-Host "LaTeX generated at .\output\Zain_Usmani_Resume.tex"
Read-Host "Make any manual edits now, save the file, then press ENTER to compile"

Write-Host "Compiling and Archiving Resume..."
python scripts\compile.py
if ($LASTEXITCODE -ne 0) { Write-Host "Fatal Error: compile.py failed."; exit 1 }