import tkinter as tk
import tkinter.messagebox as tkm

def button_click(event):
    btn = event.widget
    num = btn["text"]  # クリックされたボタンの数字
    # tkm.showinfo(num, f"{num}のボタンがクリックされました")
    entry.insert(tk.END, num)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x450")

    entry = tk.Entry(root, 
                    justify="right", 
                    width=10, 
                    font=("Times New Roman", 40)
                    )
    entry.grid(row=0, column=0, columnspan=4)

    r, c = 1, 1
    for i, num in enumerate([9,8,7,6,5,4,3,2,1,0,"+"], 1):
        btn = tk.Button(root, text=num, font=("Times New Roman", 30))
        btn.bind("<1>", button_click)
        btn.grid(row=r, column=c, padx=10, pady=10)
        if i%3 == 0:
            r += 1
            c = 0
        c += 1
        
    root.mainloop()
