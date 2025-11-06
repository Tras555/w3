from flask import Flask, render_template, jsonify
import time
import threading

app = Flask(__name__)

# 番茄鐘時間設定 (工作時間25分鐘, 休息時間5分鐘)
WORK_DURATION = 25 * 60  # 25分鐘轉換成秒
BREAK_DURATION = 5 * 60  # 5分鐘轉換成秒

# 當前狀態: '工作中' 或 '休息中'
current_state = "工作中"
time_left = WORK_DURATION

# 當前番茄鐘是否在計時中
timer_running = False

def timer():
    global time_left, current_state, timer_running

    while timer_running:
        time_left -= 1
        time.sleep(1)
        
        # 切換狀態: 工作時間結束，開始休息
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
        # 使用子執行緒來執行倒數計時
        threading.Thread(target=timer, daemon=True).start()
    return jsonify({"status": "timer_started"})

@app.route('/stop_timer', methods=['POST'])
def stop_timer():
    global timer_running
    timer_running = False
    return jsonify({"status": "timer_stopped"})

if __name__ == "__main__":
    app.run(debug=True)
