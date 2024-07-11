import tkinter as tk
from tkinter import messagebox
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

psychology_topics = {
    "Personality": [
        "What are your three biggest strengths?",
        "Describe a situation where you felt most stressed. How did you cope?",
        "Do you consider yourself introverted or extroverted? Why?",
        "What motivates you to achieve your goals?",
        "How do you typically handle conflict with others?"
    ],
    "Values": [
        "What are the most important things in life for you?",
        "Would you rather be rich and unhappy or poor and content? Why?",
        "What qualities do you admire most in others?",
        "If you could change one thing about the world, what would it be?",
        "What are some personal values you try to live by?"
    ],
    "Emotions": [
        "How would you describe your typical emotional state?",
        "What are some things that make you feel happy or fulfilled?",
        "How do you usually express anger or frustration?",
        "Can you recall a situation where you experienced a strong emotion? What was it?",
        "What are some things you do to manage stress or anxiety?"
    ],
    "Cognition": [
        "Do you consider yourself a logical or creative thinker?",
        "Describe your learning style. How do you best retain information?",
        "What are some of your interests and hobbies? Why do you enjoy them?",
        "How would you solve a complex problem? Describe your approach.",
        "Are you good at making decisions? What factors do you consider?"
    ]
}

class MindMappingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mind Mapping - Developed by Vasundhara Consulting Services")
        
        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.feeling_var = tk.IntVar()
        
        self.questions = []
        self.answers = []
        self.current_question_index = 0
        
        self.create_widgets()
        
    def create_widgets(self):
        tk.Label(self.root, text="Enter your name:").pack()
        tk.Entry(self.root, textvariable=self.name_var).pack()
        
        tk.Label(self.root, text="Enter your age:").pack()
        tk.Entry(self.root, textvariable=self.age_var).pack()
        
        tk.Label(self.root, text="Enter your gender:").pack()
        tk.Entry(self.root, textvariable=self.gender_var).pack()

        tk.Label(self.root, text="Enter your email:").pack()
        tk.Entry(self.root, textvariable=self.email_var).pack()
        
        tk.Label(self.root, text="How do you feel today on a scale of 1 to 5 (1: complete down, 2: down, 3: so-so, 4: fit & fine, 5: energetic)?").pack()
        tk.Entry(self.root, textvariable=self.feeling_var).pack()
        
        tk.Button(self.root, text="Start Questions", command=self.start_questions).pack()
        
        self.question_label = tk.Label(self.root, text="")
        self.question_label.pack()
        
        self.answer_text = tk.Text(self.root, width=50, height=5)
        self.answer_text.pack()
        
        self.next_button = tk.Button(self.root, text="Next", command=self.next_question)
        self.next_button.pack()
        
        self.thank_you_label = tk.Label(self.root, text="")
        self.thank_you_label.pack()
        
    def start_questions(self):
        self.questions = []
        for topic, questions in psychology_topics.items():
            self.questions.extend(questions)
        random.shuffle(self.questions)
        
        self.answers = []
        self.current_question_index = 0
        
        self.ask_question()
        
    def ask_question(self):
        if self.current_question_index < len(self.questions):
            self.question_label.config(text=self.questions[self.current_question_index])
        else:
            self.finish_questions()
        
    def next_question(self):
        answer = self.answer_text.get("1.0", tk.END).strip()
        if answer:
            self.answers.append(f"Q: {self.questions[self.current_question_index]}\nA: {answer}\n")
            self.current_question_index += 1
            self.answer_text.delete("1.0", tk.END)
            self.ask_question()
        else:
            messagebox.showwarning("Input Error", "Please enter an answer before proceeding.")
        
    def finish_questions(self):
        name = self.name_var.get()
        age = self.age_var.get()
        gender = self.gender_var.get()
        email = self.email_var.get()
        feeling = self.feeling_var.get()
        
        filename = f"{name}.txt"
        
        with open(filename, "w") as file:
            file.write(f"Name: {name}\nAge: {age}\nGender: {gender}\nFeeling: {feeling}\n\n")
            file.writelines(self.answers)
        
        self.send_email(email, filename)
        
        self.question_label.config(text="")
        self.answer_text.pack_forget()
        self.next_button.pack_forget()
        self.thank_you_label.config(text="You have done well - Thank you very much.")
        
    def send_email(self, to_email, filename):
        from_email = "arup.roy@vasundharaconsulting.com"
        password = "########"
        
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = from_email
        message['To'] = to_email
        message['Subject'] = "Your Mind Mapping Results"
        
        # Attach the body with the msg instance
        message.attach(MIMEText("Please find attached your mind mapping results.", 'plain'))
        
        # Open the file to be sent
        with open(filename, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        # Encode file in base64
        encoders.encode_base64(part)
        
        part.add_header('Content-Disposition', f"attachment; filename= {filename}")
        
        # Attach the instance 'part' to instance 'message'
        message.attach(part)
        
        # Create SMTP session
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()  # Enable security
            server.login(from_email, password)  # Login with mail_id and password
            text = message.as_string()
            server.sendmail(from_email, to_email, text)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = MindMappingApp(root)
    root.mainloop()
