$pshost = get-host
$pswindow = $pshost.ui.rawui

<#
$newsize = $pswindow.buffersize
$newsize.height = 3000
$newsize.width = 120
$pswindow.buffersize = $newsize

$newsize = $pswindow.windowsize
$newsize.height = 50
$newsize.width = 120
$pswindow.windowsize = $newsize

cls
#>

$pswindow.windowtitle = ('ASP.NET vNext: {0} {1}' -f $args[0], $args[1])
$pswindow.foregroundcolor = 'DarkYellow'
$pswindow.backgroundcolor = 'DarkMagenta'

$run =  $args[0] + " " + $args[1]
Invoke-Expression $run