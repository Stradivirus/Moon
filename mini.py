import os
import subprocess

def run_commands():
    # chmod 777 /tep 명령 실행
    try:
        os.chmod('/tmp', 0o777)
        print("chmod 777 /tmp 명령이 성공적으로 실행되었습니다.")
    except Exception as e:
        print(f"chmod 명령 실행 중 오류 발생: {e}")

    # mini start 명령 실행
    command = "/usr/local/bin/minikube start --cpus 3 --memory 3000 --force"
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("mini start 명령이 성공적으로 실행되었습니다.")
        print("출력:", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"mini start 명령 실행 중 오류 발생: {e}")
        print("오류 출력:", e.stderr)

if __name__ == "__main__":
    run_commands()

