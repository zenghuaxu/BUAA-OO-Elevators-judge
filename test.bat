echo test begin
set MAX_EPOCH=100
for /L %%i in (1,1,%MAX_EPOCH%) do (
     python generate.py
     .\datainput_student_win64.exe | java -jar .\homework_5~7.jar > stdout.txt
     python check.py > check_%%i.txt
     echo epoch_%%i PASS
)
pause