# プロジェクト演習Ⅰ・テーマD
## 第2回
### tkinterで電卓実装
####　追加機能
- オールクリアボタン：entryに入力されている数字、数式の文字列全体をdeleteする
- 四則演算:"+","-","*","/"ボタンを押すことによってそれぞれの四則演算ができる
import tkinter as tk
import tkinter.messagebox as tkm

def click_equal(event):
    eqn = entry.get()
    res = eval(eqn)
    entry.delete(0, tk.END)
    entry.insert(tk.END, str(res))

def button_click(event):
    btn = event.widget
    txt = btn["text"]
    #tkm.showinfo(txt, f"{txt}ボタンクリックされました")
    entry.insert(tk.END,txt)
    if txt == "C":
        entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("tk")
    root.geometry("300x450")
    r, c = 1, 1
    for i, num in enumerate(range(9, -1, -1), 1):
        btn = tk.Button(root,text=num,command=button_click, font=("Times New Roman", 50))
        btn.bind("<1>", button_click)
        btn.grid(row=r, column=c, padx=3, pady=3)
        if i%3 == 0:
            r += 1
            c = 0
        c += 1

    btn = tk.Button(root,text="+", font=("Times New Roman", 50))
    btn.bind("<1>", button_click)
    btn.grid(row=1, column=4, padx=3,pady=3)

    btn = tk.Button(root,text="=", font=("Times New Roman", 50))
    btn.bind("<1>", click_equal)
    btn.grid(row=4, column=3, padx=3,pady=3)

    btn = tk.Button(root,text="C", font=("Times New Roman", 50))
    btn.bind("<1>", button_click)
    btn.grid(row=4, column=2, padx=3,pady=3)

    btn = tk.Button(root,text="-", font=("Times New Roman", 50))
    btn.bind("<1>", button_click)
    btn.grid(row=2, column=4, padx=4,pady=3)

    btn = tk.Button(root,text="*", font=("Times New Roman", 50))
    btn.bind("<1>", button_click)
    btn.grid(row=3, column=4, padx=4,pady=3)

    btn = tk.Button(root,text="/", font=("Times New Roman", 50))
    btn.bind("<1>", button_click)
    btn.grid(row=4, column=4, padx=4,pady=3)



entry = tk.Entry(root, justify="right", width=10, font=("Times New Roman", 50))
entry.grid(row=0, column=1, columnspan=4)

root.mainloop()

## 第3回
### tkinterで迷路ゲーム実装
#### 3限:基本機能
- こうかとんを矢印キーで動かす迷路
- 壁などを出現させ壁にはぶつからないようにした
#### ４限:追加機能
- 敵キャラの力士を２人配置し、ランダムに出現するような機能を追加した。
- 敵キャラの力士が壁に埋まらないようにしようとしたが時間がなくて追加できなかった。

#### ToDo
-[ ]自動で動くような機能の追加
-[ ]力士が壁に埋まらないようにする機能の追加

## 第4回
### pygameでゲーム実装
#### ３限 : 基本機能
- ゲーム概要 :
   - rensyu04/dodge_bomb.pyを実行すると、1440, 790のスクリーンに青空と草原が描画され、こうかとんを移動させ飛び回る爆弾から逃げるゲーム
   - こうかとんが爆弾に接触するとゲームオーバーで終了する
- 操作方法 : 矢印キーでこうかとんを上下左右に移動する
- プログラムの説明
   - dodge_bomb.pyを実行すると、pygameの初期化、main関数の順に処理が進む
   - ゲームオーバーによりmain関数から抜けると、pygameの初期化を解除し、プログラムが終了する
   - main関数では、clockの生成、スクリーンの生成、背景画像の描画、こうかとんの描画、爆弾の描画を行う
   - main関数の無限ループでは、キー操作に応じたこうかとんの移動、指定速度に応じた爆弾の移動を行う
   - Rectクラスのcolliderectメソッドにより、こうかとんと爆弾の接触を判定する
   - check_bound関数では、こうかとんや爆弾の座標がスクリーン外にならないようにチェックする
#### 4限 : 追加機能
 - 新たに、大きさと色と速さが違う2つの爆弾を追加した
 - 新たに追加された爆弾は大きさと速さが違うのでよりゲーム難易度が上がっている
 ### ToDo
 - [ ]こうかとんに爆弾が当たるとこうかとんの画像を爆発したものに変更する機能の追加
 - [ ]こうかとんに爆弾が当たると画面中央に"Game Over"と描画される機能の追加

## 第5回
### Pygameでゲーム実装
#### 3限 : 基本機能
- ゲーム概要 :
   - rensyu04/dodge_bomb.pyを実行すると、1440, 790のスクリーンに青空と草原が描画され、こうかとんを移動させ飛び回る5つの爆弾から逃げるゲーム
   - こうかとんが爆弾に接触するとゲームオーバーで終了する
- 操作方法 : 矢印キーでこうかとんを上下左右に移動する
- プログラムの説明
   - dodge_bomb.pyを実行すると、pygameの初期化、main関数の順に処理が進む
   - ゲームオーバーによりmain関数から抜けると、pygameの初期化を解除し、プログラムが終了する
   - main関数では、clockの生成、スクリーンの生成、背景画像の描画、こうかとんの描画、爆弾の描画を行う
   - main関数の無限ループでは、キー操作に応じたこうかとんの移動、指定速度に応じた爆弾の移動を行う
   - Rectクラスのcolliderectメソッドにより、こうかとんと爆弾の接触を判定する
   - check_bound関数では、こうかとんや爆弾の座標がスクリーン外にならないようにチェックする
#### 4限 : 追加機能
   - 爆弾の数と速さを変更してゲームとしての難易度をあげた
   - 背景も地獄のような背景にしてよりこうかとんが危機的状態になった
   - 爆弾の色を変更して背景に会うように火の粉のようにした
   - 背景に合わせて不穏なBGMが流れるようにした
### ToDo
- [ ]こうかとんが爆弾を撃ち落とす機能
- [ ]こうかとんが爆弾に当たると燃えるような画像の変更をする機能

## 第6回
### tkinterで横スクロールアクションゲーム実装
#### 基本機能
- ゲーム概要 :
   - game.kadai.pyを実行すると800×500のスクリーンに地獄とこうかとんと教科書が描画され、こうかとんを移動させ敵キャラの教科書を踏んで倒していき、ゴールの片柳研究所を目指すゲーム
   - こうかとんが教科書に接触すると落単してゲームオーバーで終了する
   - ゴールの片柳研究所にこうかとんが接触するとゴール判定となりゲームクリアになる
- 操作方法 : 矢印キーでこうかとんを移動する 
   - 右キーで右移動　左キーで左移動　上キーでジャンプ
- プログラムの説明
   - game.kadai.pyを実行するとキャンバスに自機キャラ、敵キャラ、ゴール、背景などの画像が描画されていく
   - 大きく分けて"Game","Screen","Character"の３つのクラスを使いゲームを作成した
   - "Player","Enemy","Goal"などのサブクラスも作成した
   - GameクラスがScreenクラスやCharacterクラスのオブジェクトの作成と、これらのオブジェクトに対する処理の依頼を行うように作成した
   - Screenクラスは画面の表示を行うためのウィジェットを作成したり、キャラクターや背景などの表示を行っている
   - Characterクラスは自機キャラ、敵キャラ、ゴールなどを作成するために使用した　キャラクターの当たり判定やキャラクターの位置変更などを行っている
   - ゲーム動作としては、tkinterがGameクラスに右キーが入力されたことを通知、GameクラスがCharacterクラスに右に動くことを依頼、GameクラスがCharacterクラスに当たり判定を依頼、必要に応じてGameクラスがCharacterクラスに当たった時の処理を依頼、というようにクラスが連携して成り立っている
   - 横スクロールのアクションゲームなので自機キャラの位置に応じて画面の表示領域も変化していくようになっている
   - 当たり判定を行うことで、自機キャラが敵キャラを踏んで倒したり、ぶつかってゲームオーバーになるなどという処理も行っている
   - ゴールを用意し、敵を倒して進みゴールに自機キャラが触れるとゲームクリアとなる
### 参考サイトのURL
- https://daeudaeu.com/tkinter_canvas_widget/
- https://daeudaeu.com/tkinter_canvas_draw/
### ToDo
- [ ]ゲームを盛り上げるようなBGMの追加
- [ ]制限時間の追加
## 追加　C0B21030　大野歩夢
- 音楽の追加
天国と地獄をBGMとして入れました。ゲームクリアかゲームオーバーで音楽は止まります。
https://youtu.be/8w59APKsBn8