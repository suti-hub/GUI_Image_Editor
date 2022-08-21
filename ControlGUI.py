# -*- coding: utf-8 -*-
import os
from ModelImage import ModelImage

class ControlGUI():
    
    def __init__(self, default_path):

        self.dir_path = default_path
        self.ext_keys = {'[Photo]':['.png', '.jpg', '.jpeg', '.JPG', '.PNG'], '[Video]':['.mp4']}
        self.target_files = {}
        self.file_pos = 0
        self.file_pos_video = 0
        self.speed_val = 1
        
        self.clip_sx = 0
        self.clip_sy = 0
        self.clip_ex = 0
        self.clip_ey = 0
        self.canvas = {}
        self.frame = {}
        
        self.state_machine = {'Photo':None, 'Video':None}
        
        self.output_path = os.path.join(default_path,'output')
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
            
        # Model Class生成
        self.model = ModelImage(self.output_path)
    
        
    # Common(Private)
    def is_target(self, name, key_list):
        
        valid = False
        for ks in key_list:
            if ks in name:
                valid = True
        
        return valid
    
    
    def get_file(self, command, set_pos=-1):
        
        tab = self.select_tab
        num = len(self.target_files[tab])
        
        if tab == '[Photo]':
            
            if command == 'prev':
                self.file_pos = self.file_pos - 1            
            elif command == 'next':
                self.file_pos = self.file_pos + 1            
            elif command == 'set':
                self.file_pos = set_pos            
            else:   # current
                self.file_pos = self.file_pos
            
            if self.file_pos < 0:
                self.file_pos = num -1
                
            elif self.file_pos >= num:
                self.file_pos = 0
                
            cur_pos = self.file_pos
                
        else: # '[Video]'
        
            if command == 'set':
                self.file_pos_video = set_pos  
            cur_pos = self.file_pos_video
        
        cur_file = os.path.join(self.dir_path, self.target_files[tab][cur_pos])
        print('{}/{} {} '.format(cur_pos, num-1, cur_file))
        return cur_file
    
    # Common(Public)
    def InitCanvas(self, window_canvas_dict):
        
        for ks, canvas in window_canvas_dict.items():      
            self.canvas[ks] = canvas
            
        self.photo_canvas = self.canvas['Photo']
        self.video_canvas = self.canvas['Video1']
        self.frame['Video1'] = 0
        self.frame['Video2'] = 0
        
        
    def SetTab(self, select_tab):
        
        self.select_tab = select_tab
        
    
    def InitStateMachine(self):
        # (1/0:有効/無効, 0-5:遷移先)
        stm_video = [
            #0:IDLE
            {'dir':(1,1),'set':(0,0),'play':(0,0),'stop':(0,0),'step':(0,0),'speed|bar':(0,0),'cap':(0,0),
             'edit':(0,0),'clip':(0,0),'rect':(0,0),'done':(0,0),'dclick':(0,0),'save|undo':(0,0)},
            #1:SET
            {'dir':(1,1),'set':(1,2),'play':(0,1),'stop':(0,1),'step':(0,1),'speed|bar':(0,1),'cap':(0,1),
             'edit':(0,1),'clip':(0,1),'rect':(0,1),'done':(0,1),'dclick':(0,1),'save|undo':(0,1)},  
            #2:STOP    
            {'dir':(1,1),'set':(1,2),'play':(1,3),'stop':(0,2),'step':(1,2),'speed|bar':(1,2),'cap':(1,2),
             'edit':(1,4),'clip':(1,5),'rect':(0,2),'done':(0,2),'dclick':(1,2),'save|undo':(1,2)},  
            #3:PLAY    
            {'dir':(0,3),'set':(0,3),'play':(0,3),'stop':(1,2),'step':(0,3),'speed|bar':(1,3),'cap':(0,3),
             'edit':(0,3),'clip':(0,3),'rect':(0,3),'done':(0,3),'dclick':(0,3),'save|undo':(0,3)},  
            #4:EDIT    
            {'dir':(0,4),'set':(0,4),'play':(0,4),'stop':(0,4),'step':(0,4),'speed|bar':(0,4),'cap':(1,4),
             'edit':(1,4),'clip':(1,5),'rect':(0,4),'done':(0,4),'dclick':(0,4),'save|undo':(1,2)},  
            #5:EDIT_CLIP    
            {'dir':(0,5),'set':(0,5),'play':(0,5),'stop':(0,5),'step':(0,5),'speed|bar':(0,5),'cap':(1,5),
             'edit':(0,5),'clip':(1,5),'rect':(1,5),'done':(1,6),'dclick':(0,5),'save|undo':(1,2)}, 
            #6:EDIT_LOCK    
            {'dir':(0,6),'set':(0,6),'play':(0,6),'stop':(0,6),'step':(0,6),'speed|bar':(0,6),'cap':(1,6),
             'edit':(0,6),'clip':(0,6),'rect':(0,6),'done':(0,6),'dclick':(0,6),'save|undo':(1,2)}, 
        ]
        
        # (1/0:有効/無効, 0-3:遷移先)
        stm_photo = [
            #0:IDLE
            {'dir':(1,1),'set':(0,0),'prev':(0,0),'next':(0,0),'edit':(0,0),'clip':(0,0),'rect':(0,0),
             'done':(0,0),'save|undo':(0,0)}, 
            #1:SET    
            {'dir':(1,1),'set':(1,1),'prev':(1,1),'next':(1,1),'edit':(1,2),'clip':(1,3),'rect':(0,1),
             'done':(0,1),'save|undo':(0,1)}, 
            #2:EDIT    
            {'dir':(0,2),'set':(1,1),'prev':(1,1),'next':(1,1),'edit':(1,2),'clip':(1,3),'rect':(0,2),
             'done':(0,2),'save|undo':(1,1)}, 
            #3:EDIT_CLIP    
            {'dir':(0,2),'set':(1,1),'prev':(1,1),'next':(1,1),'edit':(1,3),'clip':(1,3),'rect':(1,3),
             'done':(1,2),'save|undo':(1,1)}, 
        ]
        
        self.state_table = {'[Photo]':stm_photo, '[Video]':stm_video}
        self.cur_state = {'[Photo]':0, '[Video]':0}
          

    def GetEventState(self, command):
       
        tab = self.select_tab
        cur_state = self.cur_state[tab]
        is_valid, next_state = self.state_table[tab][cur_state][command]
        print('state_change:{}, {}->{}'.format(is_valid, cur_state, next_state))
        self.cur_state[tab] = next_state
        res = True if is_valid == 1 else False
        return res  
    
    
    def SetEventState(self, next_state):
        
        tab = self.select_tab
        print('state_change:{}->{}'.format(self.cur_state[tab], next_state))
        self.cur_state[tab] = next_state
        
    
    def GetCurrentState(self):
        
        tab = self.select_tab
        return self.cur_state[tab]


    def SetDirlist(self, dir_path):
                
        self.dir_path = dir_path
        tab = self.select_tab
        target_files = []
        
        file_list = os.listdir(self.dir_path)
        target_ext = self.ext_keys[self.select_tab]
        print(tab, target_ext)
        
        for fname in file_list:
            if self.is_target(fname, target_ext):
                target_files.append(fname)        
        
        self.target_files[self.select_tab] = target_files

        cur_file = 'None'
        if len(target_files) > 0:
            cur_file = self.get_file('current')
            print(cur_file)

        return self.target_files[self.select_tab], os.path.basename(cur_file)

    
    def DrawRectangle(self, select_tab, command, pos_y, pos_x):
                
        if command == 'clip_start':
            self.clip_sy, self.clip_sx = pos_y, pos_x
            self.clip_ey, self.clip_ex = pos_y+1, pos_x+1
            
        elif command == 'clip_keep':      
            self.clip_ey, self.clip_ex = pos_y, pos_x
            
        elif command == 'clip_end':
            self.clip_ey, self.clip_ex = pos_y, pos_x
            self.clip_sy, self.clip_sx = self.model.GetValidPos(select_tab, self.clip_sy, self.clip_sx)
            self.clip_ey, self.clip_ex = self.model.GetValidPos(select_tab, self.clip_ey, self.clip_ex)
            
        if select_tab == '[Photo]':
            self.model.DrawRectangle(self.photo_canvas, self.clip_sy, self.clip_sx, self.clip_ey, self.clip_ex)
        else:
            self.model.DrawRectangle(self.canvas['Video1'], self.clip_sy, self.clip_sx, self.clip_ey, self.clip_ex)
            self.model.DrawRectangle(self.canvas['Video2'], self.clip_sy, self.clip_sx, self.clip_ey, self.clip_ex)

    
    def Set(self, select_tab, set_pos, callback):
                
        if select_tab == '[Photo]':
            fname = self.get_file('set', set_pos)
            self.model.DrawPhoto(fname, self.photo_canvas, 'None')
        else:
            fname = self.get_file('set', set_pos)
            self.model.DeleteRectangle(self.canvas['Video1'])
            self.model.DeleteRectangle(self.canvas['Video2'])
            self.video_tag = 'Video1'
            self.video_canvas = self.canvas[self.video_tag]                     
            self.model.SetVideo(fname, self.video_canvas, self.video_tag, 'set', callback)
            _, self.frame['Video1'] = self.model.GetVideo('status')
            _, self.frame['Video2'] = self.model.GetVideo('status')   
            print('tag, fno1, fno2',self.video_tag, self.frame['Video1'], self.frame['Video2'])
    
        
    def Edit(self, select_tab, command):
                
        args = {}
        if command == 'clip_done':
            args['sx'], args['sy'] = self.clip_sx, self.clip_sy
            args['ex'], args['ey'] = self.clip_ex, self.clip_ey
                
        if select_tab == '[Photo]':                 
            fname = self.get_file('current')
            self.model.DrawPhoto(fname, self.photo_canvas, command, args=args)
        else:
            self.play_status, self.frame[self.video_tag] = self.model.GetVideo('status')
            print('tag, fno1, fno2',self.video_tag, self.frame['Video1'], self.frame['Video2'])
            self.model.EditVideo(self.canvas['Video1'], 'Video1', command, self.frame['Video1'], args=args, update=False)
            self.model.EditVideo(self.canvas['Video2'], 'Video2', command, self.frame['Video2'], args=args, update=True)

        
    def Save(self, select_tab):
                
        if select_tab == '[Photo]':        
            fname = self.get_file('current')
            self.model.SavePhoto(fname)
        else:
            _, self.frame[self.video_tag] = self.model.GetVideo('status')
            fname = self.get_file('current')
            self.model.SaveVideo(fname, self.frame['Video1'], self.frame['Video2'])
            print('tag, fno1, fno2',self.video_tag, self.frame['Video1'], self.frame['Video2'])
            self.model.EditVideo(self.canvas['Video1'], 'Video1', 'Undo', self.frame['Video1'])
            self.model.EditVideo(self.canvas['Video2'], 'Video2', 'Undo', self.frame['Video2'])
            self.model.DeleteRectangle(self.canvas['Video1'])
            self.model.DeleteRectangle(self.canvas['Video2'])
            
            
    def Undo(self, select_tab, command):
                
        if select_tab == '[Photo]':
            fname = self.get_file('current')
            self.model.DrawPhoto(fname, self.photo_canvas, command)
        else:
            _, self.frame[self.video_tag] = self.model.GetVideo('status')
            print('tag, fno1, fno2',self.video_tag, self.frame['Video1'], self.frame['Video2'])
            self.model.EditVideo(self.canvas['Video1'], 'Video1', 'Undo', self.frame['Video1'])
            self.model.EditVideo(self.canvas['Video2'], 'Video2', 'Undo', self.frame['Video2'])
            self.model.DeleteRectangle(self.canvas['Video1'])
            self.model.DeleteRectangle(self.canvas['Video2'])
    
    # Photo(Public)
    def DrawPhoto(self, command, set_pos=-1):
                
        fname = self.get_file(command, set_pos)
        self.model.DrawPhoto(fname, self.photo_canvas, 'None')
        return self.file_pos
        
    # Video(Public)
    def InitSpeed(self, speed_text):
        
        self.speed_val = 1
        return speed_text[self.speed_val]    
    
    
    def UpSpeed(self, speed_text):     
        
        self.speed_val += 1
        if self.speed_val >= len(speed_text):
            self.speed_val = 0
        return speed_text[self.speed_val]
    
    
    def SetCanvas(self, command, select_canvas):

        if command == 'set_canvas':
            self.video_tag = select_canvas
            self.video_canvas = self.canvas[self.video_tag]
            self.play_status, self.frame['Video1'] = self.model.GetVideo('status')
            self.play_status, self.frame['Video2'] = self.model.GetVideo('status')
            print('canvas->{}, play_status:{}, frame:{}'.format(select_canvas, self.play_status, self.frame[select_canvas]))          
            
    
    def GetVideo(self, command):
        
        return self.model.GetVideo(command)       
            
            
    def Video(self, command, set_pos=-1):
        #play/stop/setpos/speed
        res = self.model.Video(self.video_canvas, self.video_tag, command)
        return res 
