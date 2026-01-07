import tkinter as tk
import os
from tkinter import ttk, messagebox
from datetime import datetime
from engine import infer_risk
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

# Store the last assessment so to generate a report for it
last_assessment = {
    "inputs": None,
    "risk_level": None,
    "explanation": None,
}

def on_assess():
    # Collect values
    user_inputs = {
        "age-group": age_var.get(),
        "smoking": "yes" if smoking_var.get() == "yes" else "no",
        "exposure": "yes" if exposure_var.get() == "yes" else "no",
        "breathing-issue": "yes" if breathing_var.get() == "yes" else "no",
        "chest-tightness": "yes" if chest_var.get() == "yes" else "no",
        "family-history": "yes" if family_var.get() == "yes" else "no",
        "long-term-illness": "yes" if illness_var.get() == "yes" else "no",
    }

    # Call engine
    risk_level, explanation = infer_risk(user_inputs)

    # Update risk label
    risk_text = risk_level.upper()
    color = {
        "high": "#c0392b",     
        "medium": "#f1c40f",   
        "low": "#27ae60"       
    }.get(risk_level.lower(), "#34495e")

    risk_value_label.config(text=risk_text, bg=color, fg="white")

    # Update explanation box
    explanation_text.config(state="normal")
    explanation_text.delete("1.0", tk.END)
    explanation_text.insert(tk.END, explanation)
    explanation_text.config(state="disabled")

    # Update status bar
    status_var.set(f"Last assessment: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    last_assessment["inputs"] = user_inputs
    last_assessment["risk_level"] = risk_level
    last_assessment["explanation"] = explanation

# Generate a simple PDF report for one assessment
def generate_pdf_report(assessment, filepath: str):
 
    inputs = assessment["inputs"]
    risk_level = assessment["risk_level"]
    explanation = assessment["explanation"]

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4
    y = height - 50

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Lung Disease Risk Assessment Report")
    y -= 30

    # Timestamp
    c.setFont("Helvetica", 10)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.drawString(50, y, f"Generated on: {now_str}")
    y -= 30

    # Risk Level box
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Risk Level:")
    
    # Choose color based on risk
    if risk_level == "high":
        box_color = colors.red
    elif risk_level == "medium":
        box_color = colors.orange
    else:
        box_color = colors.green

    c.setFillColor(box_color)
    c.rect(120, y - 5, 80, 18, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.drawString(130, y - 2, risk_level.upper())
    c.setFillColor(colors.black)
    y -= 40

    # Explanation
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Explanation:")
    y -= 18
    c.setFont("Helvetica", 10)

    # Simple line wrapping for explanation text
    max_width = 80  # characters per line (rough)
    words = explanation.split()
    line = ""
    for w in words:
        if len(line + " " + w) <= max_width:
            line = (line + " " + w).strip()
        else:
            c.drawString(60, y, line)
            y -= 14
            line = w
    if line:
        c.drawString(60, y, line)
        y -= 20

    # Patient input summary
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Patient Input Summary:")
    y -= 18
    c.setFont("Helvetica", 10)

    for key, value in inputs.items():
        text = f"- {key.replace('-', ' ').title()}: {value}"
        c.drawString(60, y, text)
        y -= 14
        if y < 50:  # new page if needed
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 10)

    y -= 10
    c.setFont("Helvetica", 9)

    c.showPage()
    c.save()

def on_clear():
    age_var.set("middle")
    smoking_var.set("no")
    exposure_var.set("no")
    breathing_var.set("no")
    chest_var.set("no")
    family_var.set("no")
    illness_var.set("no")

    risk_value_label.config(text="N/A", bg=content_bg, fg="#333333")
    explanation_text.config(state="normal")
    explanation_text.delete("1.0", tk.END)
    explanation_text.config(state="disabled")
    status_var.set("Ready")

def on_generate_report():
    if last_assessment["inputs"] is None:
        messagebox.showwarning("No Assessment", "Please perform a risk assessment first before generating a report.")
        return

    # Create reports folder if it doesn't exist
    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"risk_report_{timestamp}.pdf"
    filepath = os.path.join("reports", filename)

    try:
        generate_pdf_report(last_assessment, filepath)
        messagebox.showinfo("Report Generated", f"PDF report has been saved to:\n{filepath}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate report:\n{e}")


#  MAIN WINDOW 
root = tk.Tk()
root.title("Lung Disease Risk Expert System")

root.minsize(650, 450)

style = ttk.Style()
try:
    style.theme_use("clam")
except tk.TclError:
    pass

content_bg = "#f7f9fb"
root.configure(bg=content_bg)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

main_frame = ttk.Frame(root, padding=15)
main_frame.grid(row=0, column=0, sticky="nsew")
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)



#  HEADER
header_label = ttk.Label(
    main_frame,
    text="Lung Disease Risk Expert System",
    font=("Segoe UI", 16, "bold")
)
header_label.grid(row=0, column=0, columnspan=2, sticky="w")

subtitle_label = ttk.Label(
    main_frame,
    text="Fill in the patient information below and click “Assess Risk”.",
    font=("Segoe UI", 9)
)
subtitle_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 10))


#  PATIENT PROFILE (AGE)
profile_frame = ttk.LabelFrame(main_frame, text="Patient Profile", padding=10)
profile_frame.grid(row=2, column=0, sticky="nsew", padx=(0, 10), pady=(0, 10))
profile_frame.columnconfigure(1, weight=1)

ttk.Label(profile_frame, text="Age group:").grid(row=0, column=0, sticky="w")

age_var = tk.StringVar(value="middle")
age_frame = ttk.Frame(profile_frame)
age_frame.grid(row=0, column=1, sticky="w")

ttk.Radiobutton(age_frame, text="Young (0-30)", variable=age_var, value="young").grid(row=0, column=0, padx=(0, 5))
ttk.Radiobutton(age_frame, text="Middle (31-60)", variable=age_var, value="middle").grid(row=0, column=1, padx=(0, 5))
ttk.Radiobutton(age_frame, text="Old (61+)", variable=age_var, value="old").grid(row=0, column=2)

#  RISK FACTORS
factors_frame = ttk.LabelFrame(main_frame, text="Risk Factors", padding=10)
factors_frame.grid(row=3, column=0, sticky="nsew", padx=(0, 10), pady=(0, 10))
for i in range(3):
    factors_frame.columnconfigure(i, weight=1)


def add_yes_no(label_text, var, row):
    ttk.Label(factors_frame, text=label_text).grid(row=row, column=0, sticky="w", pady=2)

    btn_frame = ttk.Frame(factors_frame)
    btn_frame.grid(row=row, column=1, columnspan=2, sticky="w", pady=2)

    ttk.Radiobutton(btn_frame, text="Yes", variable=var, value="yes").grid(row=0, column=0, padx=(0, 10))
    ttk.Radiobutton(btn_frame, text="No", variable=var, value="no").grid(row=0, column=1)


smoking_var = tk.StringVar(value="no")
exposure_var = tk.StringVar(value="no")
breathing_var = tk.StringVar(value="no")
chest_var = tk.StringVar(value="no")
family_var = tk.StringVar(value="no")
illness_var = tk.StringVar(value="no")

add_yes_no("Smoking", smoking_var, 0)
add_yes_no("Exposure to pollution/chemicals", exposure_var, 1)
add_yes_no("Breathing issue", breathing_var, 2)
add_yes_no("Chest tightness", chest_var, 3)
add_yes_no("Family history of lung disease", family_var, 4)
add_yes_no("Long-term illness", illness_var, 5)


#  RESULT PANEL
result_frame = ttk.LabelFrame(main_frame, text="Assessment Result", padding=10)
result_frame.grid(row=2, column=1, rowspan=2, sticky="nsew", pady=(0, 10))
result_frame.columnconfigure(0, weight=1)
result_frame.rowconfigure(2, weight=1)

# Risk level label
risk_header_label = ttk.Label(
    result_frame,
    text="Risk Level:",
    font=("Segoe UI", 11, "bold")
)
risk_header_label.grid(row=0, column=0, sticky="w")

risk_value_label = tk.Label(
    result_frame,
    text="N/A",
    font=("Segoe UI", 14, "bold"),
    bg=content_bg,
    fg="#333333",
    padx=10,
    pady=5
)
risk_value_label.grid(row=1, column=0, sticky="w", pady=(2, 8))

# Explanation box with scrollbar
explanation_frame = ttk.Frame(result_frame)
explanation_frame.grid(row=2, column=0, sticky="nsew")
explanation_frame.columnconfigure(0, weight=1)
explanation_frame.rowconfigure(0, weight=1)

explanation_text = tk.Text(
    explanation_frame,
    height=10,
    wrap="word",
    font=("Segoe UI", 9),
    state="disabled"
)
explanation_text.grid(row=0, column=0, sticky="nsew")

scrollbar = ttk.Scrollbar(
    explanation_frame,
    orient="vertical",
    command=explanation_text.yview
)
scrollbar.grid(row=0, column=1, sticky="ns")
explanation_text.config(yscrollcommand=scrollbar.set)

#  BUTTONS
button_frame = ttk.Frame(main_frame)
button_frame.grid(row=4, column=0, columnspan=2, sticky="e", pady=(5, 0))

assess_button = ttk.Button(button_frame, text="Assess Risk", command=on_assess)
assess_button.grid(row=0, column=0, padx=(0, 5))

clear_button = ttk.Button(button_frame, text="Clear Form", command=on_clear)
clear_button.grid(row=0, column=1, padx=(0, 5))

btn_report = ttk.Button(button_frame, text="Generate PDF Report", command=on_generate_report)
btn_report.grid(row=0, column=2, padx=(5, 0))

#  STATUS BAR
status_var = tk.StringVar(value="Ready")
status_bar = ttk.Label(
    root,
    textvariable=status_var,
    anchor="w",
    padding=(8, 2)
)
status_bar.grid(row=1, column=0, sticky="we")


# Center window on screen 
root.update_idletasks()
w = root.winfo_width()
h = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (w // 2)
y = (root.winfo_screenheight() // 2) - (h // 2)
root.geometry(f"+{x}+{y}")

root.mainloop()
