param(
    [Parameter(Mandatory)][string]$Source,
    [Parameter(Mandatory)][string]$Dest
)

$content = [System.IO.File]::ReadAllText($Source, [System.Text.Encoding]::UTF8)
$ext     = [System.IO.Path]::GetExtension($Source).ToLower()

if ($ext -eq '.css') {
    # Remove /* */ comments
    $content = [regex]::Replace($content, '/\*[\s\S]*?\*/', '')
    # Collapse whitespace to single space
    $content = [regex]::Replace($content, '[\r\n\t ]+', ' ')
    # Remove spaces around structural characters
    $content = $content -replace ' *\{ *', '{'
    $content = $content -replace ' *\} *', '}'
    $content = $content -replace ' *; *', ';'
    $content = $content -replace ' *: *', ':'
    $content = $content -replace ',\s+', ','
    # Remove trailing semicolons before closing brace
    $content = $content -replace ';}', '}'
    $content = $content.Trim()
}
elseif ($ext -eq '.js') {
    # Remove single-line comments (skip URLs)
    $content = [regex]::Replace($content, '(?<![:/])//[^\n]*', '')
    # Remove /* */ comments
    $content = [regex]::Replace($content, '/\*[\s\S]*?\*/', '')
    # Collapse whitespace
    $content = [regex]::Replace($content, '[\r\n\t ]+', ' ')
    $content = $content.Trim()
}

[System.IO.File]::WriteAllText($Dest, $content, (New-Object System.Text.UTF8Encoding $false))
Write-Host "Minified: $([System.IO.Path]::GetFileName($Source)) -> $([System.IO.Path]::GetFileName($Dest))"
