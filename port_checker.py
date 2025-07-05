import socket
import json
import os
from datetime import datetime
import subprocess

def check_port(host, port):
    """주어진 호스트와 포트의 상태를 확인합니다."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)  # 5초 타임아웃
            s.connect((host, int(port)))
        return "UP"
    except (socket.timeout, ConnectionRefusedError, OSError):
        return "DOWN"

def send_notification(message):
    """알림 메시지를 보냅니다."""
    python_executable = "/app/miniconda3/envs/simpleClient/bin/python"
    script_path = "/app/mng/push_msg.py"
    
    # 실제 운영 환경에서는 아래 주석을 해제하여 사용하세요.
    subprocess.run([python_executable, script_path, message])
    
    # 테스트 목적으로 print 문으로 대체합니다.
    # print(f"Notification: {message}")

def main():
    """메인 로직을 수행합니다."""
    check_list_file = "/app/mng/port_check.lst"
    status_file = "/app/mng/port_check_status.json"

    # 상태 파일이 없으면 빈 JSON 객체로 초기화
    if not os.path.exists(status_file):
        with open(status_file, 'w') as f:
            json.dump({}, f)

    # 이전 상태 로드
    try:
        with open(status_file, 'r') as f:
            last_statuses = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        last_statuses = {}

    current_statuses = {}

    try:
        with open(check_list_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                parts = line.split()
                if len(parts) < 2:
                    continue
                
                host, port = parts[0], parts[1]
                description = " ".join(parts[2:]) if len(parts) > 2 else ""

                status = check_port(host, port)
                current_statuses[f"{host}:{port}"] = status

                last_status = last_statuses.get(f"{host}:{port}")

                now = datetime.now().strftime("%Y.%m.%d %H:%M:%S")

                if last_status != status:
                    if status == "DOWN":
                        message = f"{description} ({host}:{port}) 장애 ({now})" if description else f"{host}:{port} 장애 ({now})"
                        send_notification(message)
                    elif status == "UP":
                        message = f"{description} ({host}:{port}) 복구 ({now})" if description else f"{host}:{port} 복구 ({now})"
                        send_notification(message)
    except FileNotFoundError:
        print(f"Error: Check list file not found at {check_list_file}")
        return

    # 현재 상태를 파일에 저장
    with open(status_file, 'w') as f:
        json.dump(current_statuses, f, indent=4)

if __name__ == "__main__":
    main()
