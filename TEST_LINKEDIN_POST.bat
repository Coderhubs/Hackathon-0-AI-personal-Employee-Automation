@echo off
chcp 65001 >nul
echo ============================================================
echo LINKEDIN SAFE POST
echo ============================================================
echo.
echo This will check safety and post to LinkedIn if safe.
echo.
echo IMPORTANT: This follows all safety rules automatically.
echo.
pause

python linkedin_safe_post.py

echo.
echo ============================================================
echo POST ATTEMPT COMPLETE
echo ============================================================
echo.
pause
