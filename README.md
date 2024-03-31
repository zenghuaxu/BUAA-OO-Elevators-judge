## 准备
* 将“datainput_student_win64.exe”和“Homework.jar”添加到此文件夹中。
## 生成
* 运行“python generate.py”以生成输入。
* 你会在文件夹中看到“stdin.txt”和“passengers.json”。
## 运行
* 运行“.\datainput_student_win64.exe | java -jar .\Homework.jar > stdout.txt”，可能需要1-4分钟
## 检查
* 运行“python check.py”以检查结果。如果输出正确，你将收到“pass!”。
* 如果你想检查其他输入，可以将它们保存到“stdin.txt”中，然后运行“python read_stdin.py”以保存乘客信息，然后运行并检查你的答案。
# 检查多个输入
你可以直接运行“test.bat”来跑MAX_EPOCH条输入数据，这个数字可以在bat文件里面改。

## Preparations
* Add "datainput_student_win64.exe" and "Homework.jar" to this folder.
## Generate
* Run "python generate.py" to generate inputs.
* You can see "stdin.txt" and "passengers.json" in your folder.
## Run
* Run ".\datainput_student_win64.exe | java -jar .\Homework.jar > stdout.txt", it may take 1-4 mins
## Check
* Run "python check.py" to check outputs. You will receive "pass!" if outputs are correct.
* If you want to check other inputs, you can save them to "stdin.txt" and run "python read_stdin.py" to save passengers' infomation, and then run and check your answers.
## Check multiple inputs
* You may want to run "test.bat" to directly finish the upper procesure MAX_EPOCH times.
