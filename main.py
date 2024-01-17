# Import necessary libraries
import requests
from tkinter import *
from time import sleep
import html

# Define API class
class API:
    def __init__(self, url):
        self.url = url

    def fetch_data(self):
        r = requests.get(self.url)
        r = r.json()
        return r['results']

# Define Question class
class Question:
    def __init__(self, q_text, q_answer):
        self.text = q_text
        self.answer = q_answer

# Define QuizBrain class
class QuizBrain:
    def __init__(self, q_list):
        self.question_number = 0
        self.score = 0
        self.question_list = q_list
        self.current_question = None

    def still_has_questions(self):
        return self.question_number < len(self.question_list)

    def next_question(self):
        self.current_question = self.question_list[self.question_number]
        self.question_number += 1
        self.current_question.text = html.unescape(self.current_question.text)
        return f"Q.{self.question_number}: {self.current_question.text}"

    def check_answer(self, user_answer):
        correct_answer = self.current_question.answer
        if user_answer == correct_answer:
            self.score += 1
            return True
        else:
            return False

# Define QuizInterface class
class QuizInterface:
    def __init__(self, quizbrain: QuizBrain) -> None:
        self.quiz = quizbrain
        self.window = Tk()
        self.window.config(padx=20, pady=20, bg="white")
        self.scoreBoard = Label(text="Score: 0", bg="#375362", fg="black")
        self.scoreBoard.config(font=("Arial", 15))
        self.scoreBoard.grid(row=0, column=1)
        self.canvas = Canvas(width=300, height=250, bg="green")
        self.question_text = self.canvas.create_text(150, 125, text="Questions here", font=("Arial", 20, "italic"), width=250)
        self.canvas.grid(row=2, column=1, columnspan=2, pady=50)
        true_image = PhotoImage(file="images/true.png")
        false_image = PhotoImage(file="images/false.png")
        self.trueButton = Button(image=true_image, command=self.true_button_clicked).grid(row=3, column=1)
        self.falseButton = Button(image=false_image, command=self.false_button_clicked).grid(row=3, column=2)
        self.get_next_question()
        self.window.mainloop()

    def get_next_question(self):
        self.scoreBoard.config(text=f"Score: {self.quiz.score}")
        self.canvas.config(bg="grey")
        q_text = self.quiz.next_question()
        self.canvas.itemconfig(self.question_text, text=q_text)

    def true_button_clicked(self):
        self.check_answer("True")

    def false_button_clicked(self):
        self.check_answer("False")

    def check_answer(self, answer):
        is_correct = self.quiz.check_answer(answer)
        self.canvas.config(bg="Green" if is_correct else "Red")
        self.canvas.after(1000, self.get_next_question)

# Main program
def main():
    api = API("https://opentdb.com/api.php?amount=30&category=9&type=boolean")
    question_data = api.fetch_data()
    question_bank = []
    for question in question_data:
        question_text = question["question"]
        question_answer = question["correct_answer"]
        new_question = Question(question_text, question_answer)
        question_bank.append(new_question)

    quiz = QuizBrain(question_bank)
    QuizInterface(quiz)

if __name__ == "__main__":
    main()