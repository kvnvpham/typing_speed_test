from tkinter import *
from tkinter import messagebox
import random
from data import paragraphs

FONT = ("Arial", 16)
TIMER_MIN = 1
COUNT_SEC = 0
high_score = 0
timer = None
wpm = 0


def reset():
    global wpm

    window.after_cancel(timer)
    text_box.delete("1.0", END)
    wpm = 0
    wpm_label.config(text=f"{wpm} words/minute")


def spell_check():
    start = "1.0"
    end = "end"

    rand_paragraph_list = rand_paragraph.split(" ")
    text_box_list = text_box.get("1.0", END).split(" ")

    text_box.tag_config("red", foreground="red")
    text_box.mark_set("matchStart", start)
    text_box.mark_set("matchEnd", start)
    text_box.mark_set("searchLimit", end)

    for index in range(0, len(text_box_list) - 1):
        if rand_paragraph_list[index] != text_box_list[index]:
            for word in text_box_list[index]:
                count = StringVar()

                while True:
                    index = text_box.search(word, "matchEnd", "searchLimit", count=count, regexp=True, exact=True)
                    if index == "":
                        break
                    if count.get() == 0:
                        break
                    text_box.mark_set("matchStart", index)
                    text_box.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                    text_box.tag_add("red", "matchStart", "matchEnd")


def start_count():
    global COUNT_SEC, high_score, timer

    if COUNT_SEC == 0:
        text_box.delete("1.0", END)

    COUNT_SEC += 1

    if COUNT_SEC <= TIMER_MIN*60:
        timer = window.after(1000, count_wpm)
    else:
        window.after_cancel(timer)
        if wpm > high_score:
            with open("high score.txt", mode="w") as file:
                file.write(str(wpm))
        text_box.delete("1.0", END)
        messagebox.showinfo(title="Time!", message=f"Your total words per minute was {wpm}!")


def count_wpm():
    global wpm

    words = text_box.get("1.0", END).split(" ")
    num_words = len(words) - 1

    wpm = round((num_words/COUNT_SEC) * 60)
    wpm_label.config(text=f"{wpm} words/minute")

    spell_check()
    start_count()


window = Tk()
window.title("Typing Speed Test")
window.config(padx=40, pady=40)

window.after(1000)
window.update()

try:
    with open("high score.txt") as file:
        prev_score = file.read()
except FileNotFoundError:
    score_label = Label(text="High Score:", font=FONT)
    high_score_label = Label(text=f"{high_score} words/minute", font=FONT)
    score_label.grid(column=0, row=0, padx=(300, 0))
    high_score_label.grid(column=1, row=0, padx=(0, 300))
else:
    print(high_score)
    high_score = int(prev_score)
    print(int(prev_score))

    score_label = Label(text="High Score:", font=FONT)
    high_score_label = Label(text=f"{high_score} words/minute", font=FONT)
    score_label.grid(column=0, row=0, padx=(300, 0))
    high_score_label.grid(column=1, row=0, padx=(0, 300))


current_score_label = Label(text="Current Score:", font=FONT)
wpm_label = Label(text=f"0 words/minute", font=FONT)
current_score_label.grid(column=0, row=1, padx=(300, 0), pady=(0, 20))
wpm_label.grid(column=1, row=1, padx=(0, 300), pady=(0, 20))

rand_paragraph = random.choice(paragraphs)
paragraph_label = Label(text=rand_paragraph, font=FONT, justify=LEFT)
paragraph_label.grid(column=0, row=2, columnspan=2)

text_box = Text(width=87, height=12, font=FONT)
text_box.grid(column=0, row=3, columnspan=2)
text_box.focus_set()

start_btn = Button(text="Start", font=FONT, command=start_count)
start_btn.grid(column=0, row=4, pady=(20, 0))

reset_btn = Button(text="Reset", font=FONT, command=reset)
reset_btn.grid(column=1, row=4, pady=(20, 0))

window.mainloop()
