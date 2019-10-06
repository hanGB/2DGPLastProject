from pico2d import *
import os

open_canvas(1280, 720)

# 기본 디렉토리 저장
basic_dir = os.getcwd()

# 리소스가 있는 디렉토리 저장 및 이동
now_dir = os.path.join(basic_dir, "resource/map")
os.chdir(now_dir)

grass = load_image('grass.png')

grass.draw(640, 0)
update_canvas()

delay(1)

close_canvas()
