param (
    [string]$TargetFile,
    [string]$IconFile
)

try {
    $WshShell = New-Object -comObject WScript.Shell
    $DesktopPath = [Environment]::GetFolderPath("Desktop")
    $ShortcutPath = Join-Path $DesktopPath "Aria Bot.lnk"

    $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
    $Shortcut.TargetPath = $TargetFile
    $Shortcut.WorkingDirectory = Split-Path $TargetFile

    if ($IconFile -and (Test-Path $IconFile)) {
        $Shortcut.IconLocation = $IconFile
    }

    $Shortcut.Save()
    Write-Host "Shortcut created at $ShortcutPath"
} catch {
    Write-Error "Failed to create shortcut: $_"
}
