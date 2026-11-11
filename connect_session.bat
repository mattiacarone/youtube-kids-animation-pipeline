@echo off
title Connect Google AI Pro
cls
echo ========================================================
echo Launching Google Chrome for Google AI Pro...
echo ========================================================
echo.
echo 1. Chrome will open with a dedicated session.
echo 2. Sign into your Google account (with Google AI Pro).
echo 3. Once you reach Google Labs / VideoFX, you can close Chrome.
echo.

"C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="C:\Users\Mattia\YouTubeKids\.browser_session" "https://labs.google/fx/tools/videofx"

echo.
echo ========================================================
echo Session successfully saved to .browser_session!
echo ========================================================
pause

