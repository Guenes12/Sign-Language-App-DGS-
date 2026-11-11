@echo off

setlocal enabledelayedexpansion

mkdir output 2>nul

echo =====================================

echo Pose Dataset Augmentation gestartet

echo =====================================

for %%f in (*.mp4 *.mov *.avi) do (

    echo.

    echo Verarbeite Basis-Video: %%f

    rem 1 - Dunkler + leichter Zoom

    ffmpeg -y -i "%%f" -vf "scale=iw*1.03:ih*1.03,crop=iw/1.03:ih/1.03,eq=brightness=-0.08:contrast=1.05:saturation=1.1" -c:a copy "output\%%~nf_v01.mp4"

    rem 2 - Heller + mehr Sättigung

    ffmpeg -y -i "%%f" -vf "eq=brightness=0.10:contrast=1.05:saturation=1.3" -c:a copy "output\%%~nf_v02.mp4"

    rem 3 - Etwas schneller (10%)

    ffmpeg -y -i "%%f" -vf "setpts=0.90*PTS,eq=brightness=0.02:saturation=0.95" -c:a aac -filter:a "atempo=1.11" "output\%%~nf_v03.mp4"

    rem 4 - Etwas langsamer (12%)

    ffmpeg -y -i "%%f" -vf "setpts=1.12*PTS,eq=brightness=-0.03:saturation=1.15" -c:a aac -filter:a "atempo=0.89" "output\%%~nf_v04.mp4"

    rem 5 - Schatten / dunklere Umgebung

    ffmpeg -y -i "%%f" -vf "eq=brightness=-0.12:contrast=1.15:saturation=0.9,vignette=PI/5" -c:a copy "output\%%~nf_v05.mp4"

   rem 6 - Warmer Farbton (Innenraumlicht)

ffmpeg -y -i "%%f" -vf "eq=brightness=0.03:contrast=1.05:saturation=1.2,hue=h=10" -c:a copy "output\%%~nf_v06.mp4"

rem 7 - Kalter Farbton (LED / Tageslicht)

ffmpeg -y -i "%%f" -vf "eq=brightness=-0.02:contrast=1.05:saturation=1.1,hue=h=-10" -c:a copy "output\%%~nf_v07.mp4"
 

    rem 8 - Minimaler Crop / andere Kameraposition

    ffmpeg -y -i "%%f" -vf "crop=iw-20:ih-20,scale=iw+20:ih+20,eq=brightness=0.05:contrast=0.95" -c:a copy "output\%%~nf_v08.mp4"

    rem 9 - Klare Kamera-Variation (kein Blur)

    ffmpeg -y -i "%%f" -vf "eq=brightness=0.06:contrast=1.08:saturation=0.85" -c:a copy "output\%%~nf_v09.mp4"

    rem 10 - Kombination aus Zoom + Licht + Farbe

    ffmpeg -y -i "%%f" -vf "scale=iw*1.05:ih*1.05,crop=iw/1.05:ih/1.05,eq=brightness=-0.05:contrast=1.1:saturation=1.25,vignette=PI/6" -c:a copy "output\%%~nf_v10.mp4"

)

echo.

echo =====================================

echo Alle Varianten erstellt.

echo Starte Nummerierung...

echo =====================================

set count=1

for %%f in (output\*.mp4) do (

    set num=000!count!

    set num=!num:~-3!

    ren "%%f" "%%~nf_!num!.mp4"

    set /a count+=1

)

echo.

echo =====================================

echo Fertig!

echo Alle Videos wurden nummeriert.

echo =====================================

pause
 