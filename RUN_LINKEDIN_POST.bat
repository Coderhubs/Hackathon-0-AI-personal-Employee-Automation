@echo off
echo ================================================================================
echo LinkedIn Post - Publishing Approved Content
echo ================================================================================
echo.
echo This will publish the approved LinkedIn post using the improved posting system.
echo.
echo Improvements:
echo - Better session management
echo - Robust element detection
echo - Human-like typing
echo - Content verification
echo - Publication verification
echo.
echo ================================================================================
echo.
pause

cd /d "%~dp0"
python linkedin_scheduler_complete.py post-now

echo.
echo ================================================================================
echo Done!
echo ================================================================================
echo.
echo Check the output above to see if the post was published successfully.
echo.
echo If successful:
echo - Post is now live on LinkedIn
echo - Screenshot saved: linkedin_post_success.png
echo - Post moved to Done folder
echo.
echo If failed:
echo - Check error message above
echo - May need to run SETUP_LINKEDIN_SESSION.bat again
echo.
pause
