import os
import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"명령어 실행 중 오류 발생: {e}")
        print(f"오류 메시지: {e.stderr.strip()}")
        return None

def git_upload(path):
    # 파일인 경우 해당 파일의 디렉토리로 변경
    if os.path.isfile(path):
        folder_path = os.path.dirname(path)
        file_name = os.path.basename(path)
    else:
        folder_path = path
        file_name = None

    # 현재 작업 디렉토리를 지정된 폴더로 변경
    os.chdir(folder_path)
    print(f"{folder_path}로 작업 디렉토리를 변경했습니다.")

    # Git 저장소 상태 확인
    if not os.path.exists('.git'):
        print("Git 저장소 초기화 중...")
        run_command(["git", "init"])
    else:
        print("기존 Git 저장소를 사용합니다.")

    # 파일 또는 모든 파일 스테이징
    if file_name:
        run_command(["git", "add", file_name])
        print(f"{file_name} 파일이 스테이징 영역에 추가되었습니다.")
    else:
        run_command(["git", "add", "-A"])
        print("모든 파일이 스테이징 영역에 추가되었습니다.")

    # 변경사항 확인
    status = run_command(["git", "status", "--porcelain"])
    
    if status:
        commit_message = input("커밋 메시지를 입력하세요: ")
        run_command(["git", "commit", "-m", commit_message])
        print("변경사항이 커밋되었습니다.")
    else:
        print("커밋할 변경사항이 없습니다.")

    # 현재 브랜치 확인
    current_branch = run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    
    # 원격 저장소 설정
    remote_url = input("원격 저장소 URL을 입력하세요 (없으면 Enter를 누르세요): ").strip()
    if remote_url:
        remotes = run_command(["git", "remote"])
        if "origin" in remotes:
            run_command(["git", "remote", "set-url", "origin", remote_url])
            print("기존 원격 저장소 URL이 업데이트되었습니다.")
        else:
            run_command(["git", "remote", "add", "origin", remote_url])
            print("새 원격 저장소가 추가되었습니다.")

        # GitHub로 푸시
        print(f"'{current_branch}' 브랜치를 GitHub로 푸시 중...")
        push_result = run_command(["git", "push", "-u", "origin", current_branch])
        
        if push_result is not None:
            print("업로드가 완료되었습니다.")
        else:
            print("푸시에 실패했습니다. 원격 저장소 설정을 확인해주세요.")
    else:
        print("원격 저장소 URL이 제공되지 않았습니다. 로컬 변경사항만 저장되었습니다.")

if __name__ == "__main__":
    path = input("Git 저장소 폴더 경로 또는 파일 경로를 입력하세요: ").strip()
    
    if not os.path.exists(path):
        print("유효한 폴더 또는 파일 경로를 입력해주세요.")
    else:
        git_upload(path)
