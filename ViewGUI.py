# -*- coding: utf-8 -*-
import sys
import tkinter as tk
from tkinter import ttk, filedialog
from ControlGUI import ControlGUI
import os

class ViewGUI():
    
    def __init__(self, window_root, default_path):
        
        # Controller Class生成
        self.control = ControlGUI(default_path)
        
        # 初期化
        self.dir_path         = default_path
        self.label_rotate     = [' 90°','180°','270°']
        self.label_flip       = ['U/D','L/R']
        self.speed_text       = ['x0.5','x1.0','x2.0','x4.0']
        # set callback for video playback status
        # update_timestamp or update_frameno
        self.update_playstat  = self.update_timestamp
        #self.update_playstat  = self.update_frameno
        
        # メインウィンドウ
        self.window_root = window_root
        # メインウィンドウサイズ指定
        self.window_root.geometry("800x600")
        # メインウィンドウタイトル
        self.window_root.title('GUI Image Editor v1.0.1')
        
        # サブウィンドウ
        self.window_sub_ctrl1     = tk.Frame(self.window_root, height=300, width=300)
        self.window_sub_ctrl2     = tk.Frame(self.window_root, height=500, width=300)
        
        # Nootebook, Tab生成
        self.window_sub_frame     = tk.Frame(self.window_root, height=590, width=540)
        self.notebook             = ttk.Notebook(self.window_sub_frame)
        self.tab1                 = tk.Frame(self.notebook, height=560, width=500)
        self.tab2                 = tk.Frame(self.notebook, height=560, width=500)
        self.notebook.add(self.tab1, text='[Photo]')
        self.notebook.add(self.tab2, text='[Video]')
        self.notebook.bind('<<NotebookTabChanged>>', self.event_tabchanged)
        #self.notebook.select(self.tab2)
        self.notebook.select(self.tab1)
        self.select_tab           = '[Photo]'
        
        # Photo[tab1]
        self.window_sub_ctrl3     = tk.Frame(self.tab1,  height=120, width=400)
        self.window_photo_canvas  = tk.Canvas(self.tab1, height=450, width=400, bg='gray')
        # Video[tab2]
        self.window_sub_ctrl4     = tk.Frame(self.tab2,  height=120, width=400)
        self.window_video_canvas1 = tk.Canvas(self.tab2, height=192, width=454, bg='gray')
        self.window_video_canvas2 = tk.Canvas(self.tab2, height=192, width=454, bg='gray')
        
        # オブジェクト
        # StringVar(ストリング)生成
        self.str_dir        = tk.StringVar()
        # IntVar生成 
        self.radio_intvar1  = tk.IntVar()
        self.radio_intvar2  = tk.IntVar()
        self.bar_position   = tk.IntVar()
    
        
        # GUIウィジェット・イベント登録
        # ラベル
        label_s2_blk1       = tk.Label(self.window_sub_ctrl2, text='')
        label_s3_blk1       = tk.Label(self.window_sub_ctrl3, text='')
        label_s3_blk2       = tk.Label(self.window_sub_ctrl3, text='')
        label_target        = tk.Label(self.window_sub_ctrl1, text='[Files]')
        label_rotate        = tk.Label(self.window_sub_ctrl2, text='[Rotate]')
        label_flip          = tk.Label(self.window_sub_ctrl2, text='[Flip]')
        label_clip          = tk.Label(self.window_sub_ctrl2, text='[Clip]')
        label_run           = tk.Label(self.window_sub_ctrl2, text='[Final Edit]')
        
        self.label_frame = []
        for n in range(2):
           self.label_frame.append(tk.Label(self.tab2, text=''))
        label_barunit = tk.Label(self.tab2, text='[%]')
        
        # フォルダ選択ボタン生成
        self.button_setdir  = tk.Button(self.window_sub_ctrl1,    text = 'Set Folder', width=10, command=self.event_set_folder) 
        #　テキストエントリ生成
        self.entry_dir      = tk.Entry(self.window_sub_ctrl1,     text = 'entry_dir',  textvariable=self.str_dir, width=40)
        self.str_dir.set(self.dir_path)
        # コンボBOX生成
        self.combo_file     = ttk.Combobox(self.window_sub_ctrl1, text = 'combo_file', value=[], state='readonly', width=30, postcommand=self.event_updatefile)
        self.combo_file.set('..[select file]')
        self.combo_file.bind('<<ComboboxSelected>>', self.event_selectfile)
        
        #　切替ボタン生成
        button_next         = tk.Button(self.window_sub_ctrl3, text = '>>Next',  width=10,command=self.event_next)
        button_prev         = tk.Button(self.window_sub_ctrl3, text = 'Prev<<',  width=10,command=self.event_prev)
        
        # クリップボタン生成
        button_clip_start   = tk.Button(self.window_sub_ctrl2, text = 'Try',     width=5, command=self.event_clip_try)
        button_clip_done    = tk.Button(self.window_sub_ctrl2, text = 'Done',    width=5, command=self.event_clip_done)
        
        # Save/Undoボタン生成
        button_save         = tk.Button(self.window_sub_ctrl2, text = 'Save',    width=5, command=self.event_save)
        button_undo         = tk.Button(self.window_sub_ctrl2, text = 'Undo',    width=5, command=self.event_undo)

        # Video 
        # Slide bar(Scale)
        self.bar_scale      = tk.Scale(self.tab2, from_=0, to_=100, orient='horizontal', resolution=1.0,
                                   variable=self.bar_position, length=400, command=self.event_update_bar)
        self.bar_position.set(0)
        
        # Play/Stop/Stepボタン生成
        self.button_play    = tk.Button(self.window_sub_ctrl4, text = 'Play',    width=7, command=self.event_play)
        self.button_step    = tk.Button(self.window_sub_ctrl4, text = 'Step',    width=7, command=self.event_step)
        self.button_capture = tk.Button(self.window_sub_ctrl4, text = 'Capture', width=7, command=self.event_capture)
        self.button_speed   = tk.Button(self.window_sub_ctrl4, text = self.speed_text[1], width=7, command=self.event_speed)
        
        
        # ボタン生成
        self.btn_rotate = []
        for idx, text in enumerate(self.label_rotate): # 1:rot90 2:rot180 3:rot270
            self.btn_rotate.append(tk.Button(self.window_sub_ctrl2, text=text, width=5, command=self.event_rotate(idx)))
            
        self.btn_flip = []
        for idx, text in enumerate(self.label_flip):   # 1:Flip U/L 2:Flip L/R
            self.btn_flip.append(tk.Button(self.window_sub_ctrl2,  text=text,  width=5, command=self.event_flip(idx)))
        
        # マウスイベント登録
        self.window_photo_canvas.bind   ('<ButtonPress-1>',   self.event_clip_start)
        self.window_photo_canvas.bind   ('<Button1-Motion>',  self.event_clip_keep)
        self.window_photo_canvas.bind   ('<ButtonRelease-1>', self.event_clip_end)
        
        self.window_video_canvas1.bind  ('<Double-Button-1>', self.event_mouse_select1)
        self.window_video_canvas2.bind  ('<Double-Button-1>', self.event_mouse_select2)
        
        self.window_video_canvas1.bind  ('<ButtonPress-1>',   self.event_clip_start)
        self.window_video_canvas1.bind  ('<Button1-Motion>',  self.event_clip_keep)
        self.window_video_canvas1.bind  ('<ButtonRelease-1>', self.event_clip_end)
        self.window_video_canvas2.bind  ('<ButtonPress-1>',   self.event_clip_start)
        self.window_video_canvas2.bind  ('<Button1-Motion>',  self.event_clip_keep)
        self.window_video_canvas2.bind  ('<ButtonRelease-1>', self.event_clip_end)
        
        
        ## ウィジェット配置
        # サブウィンドウ
        self.window_sub_ctrl1.place     (relx=0.68, rely=0.05)
        self.window_sub_ctrl2.place     (relx=0.68, rely=0.30)
        self.window_sub_ctrl3.place     (relx=0.30, rely=0.90)
        self.window_sub_ctrl4.place     (relx=0.25, rely=0.93)
        self.window_sub_frame.place     (relx=0.01, rely=0.01)
        self.notebook.place             (relx=0.001, rely=0.001)
        # Photo[tab1]
        self.window_photo_canvas.place  (relx=0.09,  rely=0.05)
        # Video[tab2]
        self.window_video_canvas1.place (relx=0.042, rely=0.01)
        self.window_video_canvas2.place (relx=0.042, rely=0.44)
        
        # window_sub_ctrl1
        self.button_setdir.grid  (row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.entry_dir.grid      (row=2, column=1, padx=5, pady=5, sticky=tk.W)
        label_target.grid        (row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.combo_file.grid     (row=4, column=1, padx=5, pady=5, sticky=tk.W)
        
        # window_sub_ctrl2
        label_s2_blk1.grid       (row=1, column=1, padx=5, pady=5, sticky=tk.W)
        label_rotate.grid        (row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.btn_rotate[0].grid  (row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.btn_rotate[1].grid  (row=3, column=2, padx=5, pady=5, sticky=tk.W)
        self.btn_rotate[2].grid  (row=3, column=3, padx=5, pady=5, sticky=tk.W)
        
        label_flip.grid          (row=4, column=1, padx=5, pady=5, sticky=tk.W)
        self.btn_flip[0].grid    (row=5, column=1, padx=5, pady=5, sticky=tk.W)
        self.btn_flip[1].grid    (row=5, column=2, padx=5, pady=5, sticky=tk.W)

        label_clip.grid          (row=6, column=1, padx=5, pady=5, sticky=tk.W)
        button_clip_start.grid   (row=7, column=1, padx=5, pady=5, sticky=tk.W)
        button_clip_done.grid    (row=7, column=2, padx=5, pady=5, sticky=tk.W)
        label_run.grid           (row=8, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)
        button_undo.grid         (row=9, column=1, padx=5, pady=5, sticky=tk.W)
        button_save.grid         (row=9, column=2, padx=5, pady=5, sticky=tk.W)
        
        # window_sub_ctrl3
        label_s3_blk1.grid       (row=1, column=1, columnspan=2, padx=5, pady=5, sticky=tk.EW)
        button_prev.grid         (row=1, column=1, padx=5, pady=5, sticky=tk.E)
        label_s3_blk2.grid       (row=1, column=4, columnspan=2, padx=5, pady=5, sticky=tk.EW)
        button_next.grid         (row=1, column=3, padx=5, pady=5, sticky=tk.W)

        # Video
        # Button
        self.button_play.grid    (row=1, column=1, padx=5, pady=5, sticky=tk.E)
        self.button_step.grid    (row=1, column=2, padx=5, pady=5, sticky=tk.E)
        self.button_capture.grid (row=1, column=3, padx=5, pady=5, sticky=tk.E)
        self.button_speed.grid   (row=1, column=4, padx=5, pady=5, sticky=tk.E)
        #
        self.label_frame[0].place(relx=0.44, rely=0.36)
        self.label_frame[1].place(relx=0.44, rely=0.79)
        label_barunit.place      (relx=0.90, rely=0.85)
        # Slide bar(Scale)
        self.bar_scale.place     (relx=0.08, rely=0.85)
        
        # Init
        canvas_dict = {'Photo':self.window_photo_canvas, 'Video1':self.window_video_canvas1, 'Video2':self.window_video_canvas2}
        self.control.InitCanvas(canvas_dict)
        self.control.SetTab(self.select_tab)
        self.control.SetCanvas('Video1')
        self.control.InitStateMachine()
        self.button_speed['text'] = self.control.InitSpeed(self.speed_text) 

    
    # Event Callback
    # Common
    def event_tabchanged(self, event):
        
        notebook = event.widget
        self.select_tab = notebook.tab(notebook.select(), 'text')
        self.control.SetTab(self.select_tab)
        self.combo_file['value'] = self.control.SetFilelist(self.dir_path)
        file_name = self.control.GetCurrentFile()
        self.combo_file.set(file_name)
        print('{}: {}'.format(sys._getframe().f_code.co_name, self.select_tab))
        
    
    def event_set_folder(self):
        
        if self.control.IsTranferToState('dir'):
            print(sys._getframe().f_code.co_name)
            self.dir_path = filedialog.askdirectory(initialdir=self.dir_path, mustexist=True)
            self.str_dir.set(self.dir_path)
            self.combo_file['value'] = self.control.SetFilelist(self.dir_path)
            file_name = self.control.GetCurrentFile()
            self.combo_file.set(file_name)

        
    def event_updatefile(self):
        
        if self.control.IsTranferToState('dir'):
            print(sys._getframe().f_code.co_name)
            self.combo_file['value'] = self.control.SetFilelist(self.dir_path)
            file_name = self.control.GetCurrentFile()
            self.combo_file.set(file_name)

        
    def event_selectfile(self, event):
        
        if self.control.IsTranferToState('set'):
            print(sys._getframe().f_code.co_name)
            set_pos = self.combo_file.current()
            callback = None
            if self.select_tab == '[Video]':
                self.button_speed['text'] = self.control.InitSpeed(self.speed_text)
                callback = self.update_playstat
            self.control.Set(self.select_tab, set_pos, callback)

        
    def event_rotate(self, idx):

        def check_event():
            if self.control.IsTranferToState('edit'):
                cmd = 'rotate-' + str(idx+1)
                self.control.Edit(self.select_tab, cmd)
                print('{} {} {}'.format(sys._getframe().f_code.co_name, idx, cmd))
                return check_event
            
        return check_event
        
    
    def event_flip(self, idx):
        
        def check_event():
            if self.control.IsTranferToState('edit'):
                cmd = 'flip-' + str(idx+1)
                self.control.Edit(self.select_tab, cmd)
                print('{} {} {}'.format(sys._getframe().f_code.co_name, idx, cmd))
                return check_event
            
        return check_event
        
        
    def event_clip_try(self):
        
        if self.control.IsTranferToState('clip'):
            print(sys._getframe().f_code.co_name)
        
        
    def event_clip_done(self):
        
        if self.control.IsTranferToState('done'):
            print(sys._getframe().f_code.co_name)
            self.control.Edit(self.select_tab, 'clip_done')
    
    
    def event_clip_start(self, event):
        
        if self.control.IsTranferToState('rect'):
            print(sys._getframe().f_code.co_name, event.x, event.y)
            self.control.DrawRectangle(self.select_tab,'clip_start', event.y, event.x)
    
        
    def event_clip_keep(self, event):
        
        if self.control.IsTranferToState('rect'):
            self.control.DrawRectangle(self.select_tab,'clip_keep', event.y, event.x)

        
    def event_clip_end(self, event):
        
        if self.control.IsTranferToState('rect'):
            print(sys._getframe().f_code.co_name, event.x, event.y)
            self.control.DrawRectangle(self.select_tab,'clip_end', event.y, event.x)
        
        
    def event_save(self):
        
        if self.control.IsTranferToState('save|undo'):
            print(sys._getframe().f_code.co_name)
            self.control.Save(self.select_tab)
        
    
    def event_undo(self):
        
        if self.control.IsTranferToState('save|undo'):
            print(sys._getframe().f_code.co_name)
            self.control.Undo(self.select_tab,'None')
            
    # Photo        
    def event_prev(self):
        
        if self.control.IsTranferToState('prev'):
            print(sys._getframe().f_code.co_name)
            self.control.DrawPhoto('prev')
            file_name = self.control.GetCurrentFile()
            self.combo_file.set(file_name)
        
        
    def event_next(self):
        
        if self.control.IsTranferToState('next'):
            print(sys._getframe().f_code.co_name)
            self.control.DrawPhoto('next')
            file_name = self.control.GetCurrentFile()
            self.combo_file.set(file_name)


    # Video
    def update_timestamp(self, is_play_status, frame_no, h,m,s, video_tag):
        
        idx = int(video_tag.replace('Video','')) - 1
        if is_play_status:
            self.label_frame[idx]['text']   = 'Time:{:02}:{:02}:{:02}'.format(h,m,s)  
        else:
            self.button_play['text']        = 'Play'
            self.label_frame[0]['text']     = 'Time:{:02}:{:02}:{:02}'.format(h,m,s)
            self.label_frame[1]['text']     = 'Time:{:02}:{:02}:{:02}'.format(h,m,s)
            self.control.ForceToState('stop')
            
    
    def update_frameno(self, is_play_status, frame_no, h,m,s, video_tag):
        
        idx = int(video_tag.replace('Video','')) - 1
        if is_play_status:
            self.label_frame[idx]['text']   = 'frame:{}'.format(frame_no)
        else:
            self.button_play['text']        = 'Play'
            self.label_frame[0]['text']     = 'frame:{}'.format(0)
            self.label_frame[1]['text']     = 'frame:{}'.format(0)
            self.control.ForceToState('stop') 
            
    
    def event_update_bar(self, val):
        
        if self.control.IsTranferToState('speed|bar'):
            self.bar_position.set(int(val))
            pos = self.bar_position.get()
            print('{} :{}'.format(sys._getframe().f_code.co_name, pos))
            command = 'setpos-' + str(pos)
            self.control.Video(command)
        
        
    def event_mouse_select1(self, event):

        if self.control.IsTranferToState('dclick'):
            x, y = event.x, event.y
            print('{} :(x,y)=({},{})'.format(sys._getframe().f_code.co_name, x, y))
            self.control.SetCanvas('Video1')
        
    
    def event_mouse_select2(self, event):

        if self.control.IsTranferToState('dclick'):
            x, y = event.x, event.y
            print('{} :(x,y)=({},{})'.format(sys._getframe().f_code.co_name, x, y))
            self.control.SetCanvas('Video2')

        
    def event_play(self):

        if self.control.IsTranferToState('play'):
            self.control.Video('play')
            self.button_play['text'] = 'Stop'
            
        elif self.control.IsTranferToState('stop'):
            self.control.Video('stop')
            self.button_play['text'] = 'Play'           
            
        print('{} :{}'.format(sys._getframe().f_code.co_name, self.button_play['text']))
            

    def event_step(self):
        
        if self.control.IsTranferToState('step'):
            print(sys._getframe().f_code.co_name)
            self.control.Video('step')
        
    
    def event_capture(self):
        
        if self.control.IsTranferToState('cap'):
            print(sys._getframe().f_code.co_name)
            self.control.Video('capture')
        
    
    def event_speed(self):
        
        if self.control.IsTranferToState('speed|bar'):
            self.button_speed['text'] = self.control.UpSpeed(self.speed_text)
            print('{} :{}'.format(sys._getframe().f_code.co_name, self.button_speed['text']))
            command = 'speed-' + self.button_speed['text']
            self.control.Video(command)


def main():
    
    #　Tk MainWindow 生成
    main_window = tk.Tk()
    
    # Viewクラス生成
    current_dir = os.getcwd()
    print(current_dir)
    ViewGUI(main_window, current_dir)
    
    #　フレームループ処理
    main_window.mainloop()
    

if __name__ == '__main__':
    
    main()

   