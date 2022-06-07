import tkinter as tk
import pygame as pg
import pygame
from PIL import Image, ImageTk, ImageOps
import random
import os

main_dir = os.path.split(os.path.abspath(__file__))[0]

VIEW_WIDTH = 800  #スクリーンの横サイズ
VIEW_HEIGHT = 500 #スクリーンの縦サイズ
GAME_WIDTH = 2000 #ゲーム画面のサイズ

UPDATE_TIME = 70  #ゲームのコマ数

BG_IMAGE_PATH = "fig/hell.jpg"     #背景用の写真
PLAYER_IMAGE_PATH = "fig/dash.PNG" #自機キャラの写真

def load_sound(file):      #音楽ファイルの読み込み　　大野歩夢
    """because pygame can be be compiled without mixer."""
    if not pg.mixer:
        return None
    file = os.path.join(main_dir, "data1", file)
    try:
        sound = pg.mixer.Sound(file)
        return sound
    except pg.error:
        print("Warning, unable to load, %s" % file)
    return None

class Character:
    DIRECTION_LEFT = 0  #左を入力している状態
    DIRECTION_RIGHT = 1 #右を入力している状態
    DIRECTION_UP = 2    #上方向を入力している状態
    JUMP_NO = 0         #ジャンプをしていない状態
    JUMP_UP = 1         #ジャンプをして上昇している状態
    JUMP_DOWN = 2       #ジャンプして落下中の状態
    JUMP_TRAMPLE = 3    #敵を踏んで跳ねている状態
    STATE_NORMAL = 0    #通常の状態
    STATE_CLEAR = 1     #ゲームクリア時の状態
    STATE_DEFEATED = 2  #ゲームオーバー時の状態


    def prepareImage(self, path, size, is_right=True):  #自機キャラ画像の拡大縮小
        image = Image.open(path)                        #画像の読み込み

        width, height = size
        ratio = min(width / image.width, height/ image.height)
        resize_size = (round(ratio * image.width), round(ratio * image.height))  #自機キャラ画像のサイズを設定
        resized_image = image.resize(resize_size)
        crop_rect = resized_image.getbbox()   #不要な透明の部分を削る
        resized_image = resized_image.crop(crop_rect)   
        mirrored_image = ImageOps.mirror(resized_image) #自機キャラが反転した画像の作成
        if is_right:                                              #自機キャラが右を向いていたら
            self.right_image = ImageTk.PhotoImage(resized_image)  #自機キャラが右向きの時の画像の設定
            self.left_image = ImageTk.PhotoImage(mirrored_image)  #自機キャラが左向きの時の画像の設定
        else:                                                     #それ以外ならば
            self.left_image = ImageTk.PhotoImage(resized_image)   #自機キャラが左向きの時の画像の設定
            self.right_image = ImageTk.PhotoImage(mirrored_image) #自機キャラが右向きの時の画像の設定


        self.width = self.right_image.width()   #自機キャラの画像の幅
        self.height = self.right_image.height() #自機キャラの画像の高さ

    def getImage(self):
        if self.direction == Character.DIRECTION_RIGHT:  #右を入力されている状態だったら
            return self.right_image                      #右用のイメージを返す
        elif self.direction == Character.DIRECTION_LEFT: #左を入力されている状態だったら
            return self.left_image                       #左用イメージを返す

    def __init__(self, path, size, is_right=True):
        self.prepareImage(path, size, is_right)  #画像生成場所の設定

        self.base_y = VIEW_HEIGHT - self.right_image.height()
        self.x = 0                #自機キャラの横の位置を0設定
        self.y = self.base_y      #自機キャラの縦の位置を画面の一番下に設定
        self.speed_x = 45         #自機キャラの左右の移動速度
        self.speed_y = 50         #自機キャラのジャンプ時の上昇・下降速度
        self.jump_state = Character.JUMP_NO
        self.jump_height = 200    #自機キャラのジャンプの高さ
        self.direction = Character.DIRECTION_RIGHT  #自機キャラが右方向に移動している状態
        self.state = Character.STATE_NORMAL         #通常の状態
        self.trample_height = 70  #敵を踏んだ時のジャンプの高さ
        self.trample_y = 0

    def move(self, direction):
        if self.state == Character.STATE_CLEAR or self.state == Character.STATE_DEFEATED:  #ゲームクリア状態かゲームオーバー状態ならばそのまま返す
            return

        if direction == Character.DIRECTION_LEFT:      #左に入力されている状態だったら
            self.x = max(0, self.x - self.speed_x)     #自機キャラのxを０からゲーム幅-キャラクターの画像の幅の間で減少させる
            self.direction = Character.DIRECTION_LEFT  #自機キャラが左方向に移動している状態
        elif direction == Character.DIRECTION_RIGHT:   #右に入力されている状態だったら
            self.x = min(GAME_WIDTH - self.right_image.width(), self.x + self.speed_x)  #自機キャラのxを０からゲーム幅-キャラクターの画像の幅の間で増加させる
            self.direction = Character.DIRECTION_RIGHT #自機キャラが右方向に移動している状態
            
        elif direction == Character.DIRECTION_UP:      #上に入力されている状態の時に
            if self.jump_state == Character.JUMP_NO:   #ジャンプをしていない状態だったら
                self.jump_state = Character.JUMP_UP    #ジャンプ中かつ上昇をしている状態に変化させる

    def update(self):
        if self.state == Character.STATE_CLEAR or self.state == Character.STATE_DEFEATED:  #ゲームクリアかゲームオーバの状態の時はそのまま返す
            return

        if self.jump_state == Character.JUMP_UP:               #自機キャラがジャンプ中かつ上昇中だったら
            self.y -= self.speed_y                             #yの速度を減少させる
            if self.y <= self.base_y - self.jump_height:       #self.yがself.base_y - self.jump_heightよりも小さかったら
                self.jump_state = Character.JUMP_DOWN          #自機キャラをジャンプ中かつ降下中の状態にする
                self.y = self.base_y - self.jump_height
        elif self.jump_state == Character.JUMP_TRAMPLE:        #敵を踏んで跳ねている状態だったら
            self.y -= self.speed_y                             #seif.yからself.spped_yを引く
            if self.y <= self.trample_y - self.trample_height: #self.yがself.trample_y - self.trample_heightよりも小さかったら
                self.jump_state = Character.JUMP_DOWN          #自機キャラをジャンプ中かつ降下中の状態にする
                self.y = self.trample_y - self.trample_height
        elif self.jump_state == Character.JUMP_DOWN:           #自機キャラがジャンプ中かつ降下中だったら
            self.y += self.speed_y                             #self.yにself.speed_yを足す 
            if self.y >= self.base_y:                          #self.yがself.base_yよりも大きかったら
                self.jump_state = Character.JUMP_NO            #自機キャラをジャンプしていない状態にする
                self.y = self.base_y

    def isCollided(self, opponent):
        if self.state == Character.STATE_CLEAR or self.state == Character.STATE_DEFEATED:         #ゲームクリアかゲームオーバーの状態だったら
            return False                                                                          #Falseを返す
        if opponent.state == Character.STATE_CLEAR or opponent.state == Character.STATE_DEFEATED: #ゲームクリアかゲームオーバーの状態だったら
            return False                                                                          #Falseを返す

        sx = max(self.x, opponent.x)
        sy = max(self.y, opponent.y)
        ex = min(self.x + self.width, opponent.x + opponent.width)
        ey = min(self.y + self.height, opponent.y + opponent.height)

        if sx < ex and sy < ey: #オブジェクトに自機キャラが当たったら
            return True         #Trueを返す
        else:                   #そうでないなら
            return False        #Falseを返す
            
    def isTrampling(self, opponent):              #敵を踏みつけたかどうかの判断
        if self.jump_state == Character.JUMP_NO:  #ジャンプをしていない状態だったら
            return False                          #Falseを返す

        sy = max(self.y, opponent.y)              #自機キャラの下半分の座標

        if self.y + self.height / 2 < sy:         #敵を踏んだ場合は
            return True                           #Trueを返す
        else:                                     #そうでなければ
            return False                          #Falseを返す

    def defeated(self):                          
        self.state = Character.STATE_DEFEATED     #ゲームオーバーの状態にする

    def trample(self):
        self.jump_state = Character.JUMP_TRAMPLE  #敵を踏んで跳ね返っている状態
        self.trample_y = self.y


class Player(Character):
    def __init__(self):
        super().__init__(PLAYER_IMAGE_PATH, (100, 100))

    def gameClear(self):
        self.state = Character.STATE_CLEAR #ゲームクリアの状態
        self.jump_height = 200 


class Enemy(Character):
    def update(self):
        self.move(self.direction)             #敵キャラクターの移動
        if random.randrange(10) % 10 == 0:    #10回に1回の割合でジャンプをする
            self.move(Character.DIRECTION_UP) #上方向に入力されている状態にする

        if self.x == 0:                                #敵キャラのxが0になったら
            self.direction = Character.DIRECTION_RIGHT #右向きに移動する
        elif self.x == GAME_WIDTH - self.width:        #そうでなかったら
            self.direction = Character.DIRECTION_LEFT  #左向きに移動する
        super().update()

    def __init__(self, path, size, is_right=True):
        super().__init__(path, size, is_right)

        self.x = random.randrange(300, GAME_WIDTH - 300)
        self.direction = Character.DIRECTION_LEFT


class pythonEnemy(Enemy):       #pythonの教科書
    def __init__(self):
        super().__init__("fig/python.JPG", (90, 90))            #python教科書の描画設定

        self.jump_height = 100  #pythonのジャンプの高さ
        self.speed_x = 15       #pythonの速さ


class kaisekiEnemy(Enemy):
    def __init__(self):
        super().__init__("fig/kaiseki.JPG", (80, 80), False)    #解析学の教科書の描画設定

        self.jump_height = 50   #解析学のジャンプの高さ
        self.speed_x = 20       #解析学の速さ


class toukeigakuEnemy(Enemy):
    def __init__(self):
        super().__init__("fig/toukeigaku.JPG", (80, 80), False) #統計学の教科書の描画設定

        self.jump_height = 70   #統計学のジャンプの高さ
        self.speed_x = 10       #統計学の速さ


class Goal(Character):
    def __init__(self):
        super().__init__("fig/goal.PNG", (250, 250), False)   #ゴールの画像の描画設定

        self.direction = Character.DIRECTION_LEFT #ゴールを左向きに設定
        self.x = GAME_WIDTH - self.width          #ゴールを右端に描画させる


class Screen:
    TYPE_GAMECLEAR = 0  #ゲームクリアになった状態
    TYPE_GAMEOVER = 1   #ゲームオーバーになった状態

    def message(self, type, player_x):
        if player_x < self.view_width / 2:
            # 表示領域が左端にある
            x = self.view_width // 2
        elif player_x >= self.game_width - self.view_width / 2:
            # 表示領域が右端にある
            x = self.game_width - self.view_width // 2
        else:
            # 表示領域が端以外にある
            x = player_x
        y = self.game_height // 2

        if type == Screen.TYPE_GAMECLEAR: #ゲームクリアの状態になったら
            self.canvas.create_text(      #キャンバスに文字を描画
                x, y,
                font=("", 120),           #描画する文字の大きさ
                fill="Yellow",            #描画する文字の色
                text="フル単",             #フル単と表示
                anchor=tk.CENTER          #描画する文字を画面の中央に設定
            )

        elif type == Screen.TYPE_GAMEOVER: #ゲームオーバの状態になったら
            self.canvas.create_text(       #キャンバスに文字を描画
                x, y,
                font=("", 120),            #敵に当たった際に表示される文字の大きさ
                fill="red",                #描画する文字の色
                text="落単",                #敵に当たった際に落単と表示
                anchor=tk.CENTER           #描画する文字を画面の中央に設定
            )

    def __init__(self, master):
        self.master = master
        self.view_width = VIEW_WIDTH    #画面の横幅
        self.view_height = VIEW_HEIGHT  #画面の縦幅
        self.game_width = GAME_WIDTH    #ゲーム画面の大きさ
        self.game_height = self.view_height
        self.draw_images = []

        self.createWidgets()  #キャンバスの作成
        self.drawBackground() #ゲームの背景を描画

    def update(self, image_infos, player_x):
        for draw_image in self.draw_images:  #画像を一度削除した後に新しく画像を描画する
            self.canvas.delete(draw_image)

        self.draw_images.clear()
        
        for image, x, y in image_infos:  #image_infos内の画像オブジェクトを描画する

            draw_image = self.canvas.create_image(   #画像の描画
                x, y,     #xとyに応じて自機キャラ画像の描画位置が自動的に変化するように設定
                anchor=tk.NW,            #画像の基準位置を画像の左上に設定
                image=image
            )
            self.draw_images.append(draw_image)
        scroll_x = (player_x - self.view_width / 2) / self.game_width  #表示領域の幅とゲーム画面の幅の設定
        self.canvas.xview_moveto(max(0, scroll_x))      #表示領域の移動

    def createWidgets(self):
        self.canvas = tk.Canvas(     #キャンバスの作成
            self.master,
            width=self.view_width,
            height=self.view_height,
            scrollregion= (                             #スクロールできる画面の設定
                0,0,self.game_width,self.game_height
            ),
            highlightthickness=0
        )
        self.canvas.grid(column=0, row=0)  #キャンバスをメインウィンドウ上に配置

    def drawBackground(self):
        image = Image.open("fig/hell.jpg")                #背景画像の読み込み

        size = (self.game_width, self.game_height)        #背景画像のサイズをゲーム画面の縦と横に合わせる
        resized_image = image.resize(size)                #背景画像の拡大縮小
        self.bg_image = ImageTk.PhotoImage(resized_image) #画像オブジェクトの変換
        self.canvas.create_image(                         #背景画像の描画
            0, 0,                                         #キャンバスの左上に背景画像を合わせる
            anchor=tk.NW,                                 #背景画像の基準位置を画像の左上に設定
            image=self.bg_image
        )


class Game:
    def collisionDetect(self, character):
        for opponent in self.characters:
            if opponent is character:    #opponentがcharacterだった場合
                continue                 #continueする
            
            if character.isCollided(opponent):    #キャラが他のキャラと当たった場合
                self.collide(character, opponent) #当たり判定の処理

    def __init__(self, master):
        self.master = master
        self.screen = Screen(self.master)

        self.characters = []
        self.player = Player()
        self.characters.append(self.player)  #自機キャラを追加
        goal = Goal()
        self.characters.append(goal)         #ゴールの描画
        for _ in range(3):                   #pythonの教科書の数
            enemy = pythonEnemy()
            self.characters.append(enemy)    #pythonの教科書の描画

        for _ in range(3):                   #解析学の教科書の数
            enemy = kaisekiEnemy()
            self.characters.append(enemy)    #解析学の教科書の描画

        for _ in range(2):                   #統計学の教科書の数
            enemy = toukeigakuEnemy()
            self.characters.append(enemy)    #統計学の教科書の描画
        self.master.bind("<KeyPress-Left>", self.press)  #左キーを入力したらpressメソッドを実行
        self.master.bind("<KeyPress-Right>", self.press) #右キーを入力したらpressメソッドを実行
        self.master.bind("<KeyPress-Up>", self.press)    #上キーを入力したらpressメソッドを実行

        self.update()

    def press(self, event):
        if event.keysym == "Left":         #左に入力されたら
            self.player.move(Character.DIRECTION_LEFT)  #自機キャラを左を入力されている状態にする
               
        elif event.keysym == "Right":      #右に入力されたら
            self.player.move(Character.DIRECTION_RIGHT) #自機キャラを右を入力されている状態にする

        elif event.keysym == "Up":         #上に入力されたら
            self.player.move(Character.DIRECTION_UP)    #自機キャラを上に入力されている状態にする
            self.collisionDetect(self.player)

    def update(self):
        if self.player.state == Character.STATE_NORMAL:  #プレイヤーの状態が通常なら
            self.master.after(UPDATE_TIME, self.update)  #UPDATE_TIMEを元にゲームを更新し続ける
        else:                                            #そうでないなら
            self.master.unbind("<KeyPress-Left>")        #左キー入力の受付停止
            self.master.unbind("<KeyPress-Right>")       #右キー入力の受付停止
            self.master.unbind("<KeyPress-Up>")          #上キー入力の受付停止

        for character in self.characters:   #キャラクターの縦方向及び状態の更新
            character.update()              #更新後のキャラクターの描画
            self.collisionDetect(character) #定期処理の中での当たり判定を確認

        image_infos = []
        for character in self.characters:
            if character.state != Character.STATE_DEFEATED: #キャラクターがゲームオーバー状態になったら
                image = character.getImage()                #キャラの描画を停止
                image_info = (image, character.x, character.y)
                image_infos.append(image_info)

        self.screen.update(image_infos, self.player.x + self.player.width / 2)  #自機キャラを画面の中央になるように指定
        if self.player.state == Character.STATE_CLEAR:      #ゲームクリアの状態になったら
            self.screen.message(Screen.TYPE_GAMECLEAR, self.player.x + self.player.width // 2) #ゲームクリアの際のメッセージを画面の中央に描画するように設定
            pygame.mixer.music.stop()       #音楽のストップ　大野歩夢
        elif self.player.state == Character.STATE_DEFEATED: #ゲームオーバーの状態になったら
            self.screen.message(Screen.TYPE_GAMEOVER, self.player.x + self.player.width // 2)  #ゲームオーバーの際のメッセージを画面の中央に描画するように設定
            pygame.mixer.music.stop()       #音楽のストップ　大野歩夢

    def collide(self, character, opponent):
        if isinstance(character, Player) and isinstance(opponent, Goal):   #自機キャラがゴールにたどり着いたら
            character.gameClear()                                          #キャラクターをゲームクリアの状態にする
        elif isinstance(character, Goal) and isinstance(opponent, Player): #ゴールに自機キャラがたどり着いたら
            opponent.gameClear()                                           #ゲームクリアの状態にする

        elif isinstance(character, Enemy) and isinstance(opponent, Enemy): #敵キャラ同士が衝突したら
            if character.direction != opponent.direction:                  #お互いに離れる方向に移動する
                if character.direction == Character.DIRECTION_LEFT:        #敵キャラが左方向に移動していたら
                    character.move(Character.DIRECTION_RIGHT)              #右方向に移動させる
                    opponent.move(Character.DIRECTION_LEFT)                #もう一方のキャラを左方向に移動させる
                else:                                                      #そうでないなら
                    character.move(Character.DIRECTION_LEFT)               #左方向に移動させる
                    opponent.move(Character.DIRECTION_RIGHT)               #もう一方のキャラを右方向に移動させる

            else:
                if character.direction == Character.DIRECTION_LEFT:  #敵キャラが左方向に移動していた際に
                    if character.x < opponent.x:                     #敵キャラのx座標がもう一方の敵キャラのx座標より小さければ
                        opponent.move(Character.DIRECTION_RIGHT)     #もう一方の敵キャラを右方向に移動させる
                    else:                                            #そうでないなら
                        character.move(Character.DIRECTION_RIGHT)    #敵キャラを右方向に移動させる
                else:                                                #そうでないなら
                    if character.x > opponent.x:                     #敵キャラのx座標がもう一方の敵キャラのx座標より大きければ
                        opponent.move(Character.DIRECTION_LEFT)      #敵キャラを左方向に移動させる
                    else:                                            #そうでないなら
                        character.move(Character.DIRECTION_LEFT)     #もう一方の敵キャラを左方向に移動させる

        elif isinstance(character, Enemy) and isinstance(opponent, Goal): #敵キャラがゴールに当たった際に
            if character.direction == Character.DIRECTION_LEFT:           #左方向に移動していたら
                character.move(Character.DIRECTION_RIGHT)                 #右方向に移動させる
            else:                                                         #そうでないなら
                character.move(Character.DIRECTION_LEFT)                  #左方向に移動させる
        elif isinstance(character, Goal) and isinstance(opponent, Enemy): #もう一方の敵キャラがゴールに当たった際に
            if opponent.direction == Character.DIRECTION_LEFT:            #左方向に移動していたら
                opponent.move(Character.DIRECTION_RIGHT)                  #右方向に移動させる
            else:                                                         #そうでないなら
                opponent.move(Character.DIRECTION_LEFT)                   #左方向に移動させる

        elif isinstance(character, Player) and isinstance(opponent, Enemy):   #敵キャラクターを倒す処理
            if character.isTrampling(opponent): #自機キャラが敵キャラを踏んだら
                opponent.defeated()             #敵キャラを倒された状態にする
                character.trample()             #自機キャラを敵を踏んで跳ね返っている状態にする
            else:                               #そうでないなら
                character.defeated()            #自機キャラを倒された状態にする
        elif isinstance(character, Enemy) and isinstance(opponent, Player):
            if opponent.isTrampling(character): #敵キャラが自機キャラを踏んだら
                character.defeated()            #自機キャラを倒された状態にする
                opponent.trample()              #敵キャラを自機キャラを踏んで跳ね返っている状態にする
            else:                               #そうでないなら
                opponent.defeated()             #敵キャラを倒された状態にする

def main():
    if pg.mixer:
        music = os.path.join(main_dir, "data1", "zigoku.mp3")#音楽の読み込み　大野歩夢
        pg.mixer.music.load(music)#音楽ロード
        pg.mixer.music.play(-1)#ループ再生
    app = tk.Tk()
    game = Game(app)
    app.mainloop()

if __name__ == "__main__":
    pg.init() 
    main()
    pg.quit()