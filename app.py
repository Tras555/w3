from flask import Flask, render_template, jsonify
import threading
import time

app = Flask(__name__)

# 番茄鐘時間設定（25分鐘工作，5分鐘休息）
WORK_DURATION = 25 * 60  # 25分鐘，轉換為秒
BREAK_DURATION = 5 * 60  # 5分鐘，轉換為秒

# 當前番茄鐘狀態
time_left = WORK_DURATION
current_state = "工作中"
timer_running = False


# 計時邏輯
def timer():
    global time_left, current_state, timer_running

    while timer_running:
        time_left -= 1
        time.sleep(1)

        if time_left <= 0:
            if current_state == "工作中":
                current_state = "休息中"
                time_left = BREAK_DURATION
            else:
                current_state = "工作中"
                time_left = WORK_DURATION


@app.route('/')
def index():
    return render_template('index.html', time_left=time_left, current_state=current_state)


@app.route('/start_timer', methods=['POST'])
def start_timer():
    global timer_running
    if not timer_running:
        timer_running = True
        # 在背景啟動計時器
        threading.Thread(target=timer, daemon=True).start()
    return jsonify({"status": "timer_started"})


@app.route('/stop_timer', methods=['POST'])
def stop_timer():
    global timer_running
    timer_running = False
    return jsonify({"status": "timer_stopped"})


if __name__ == "__main__":
    app.run(debug=True)
