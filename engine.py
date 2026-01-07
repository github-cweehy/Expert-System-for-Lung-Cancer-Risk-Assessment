# engine.py
import clips
import logging

# Create global environment
logging.basicConfig(level=logging.INFO,format='%(message)s')
env = clips.Environment()
router = clips.LoggingRouter()
env.add_router(router)

# templates
env.build("""
(deftemplate patient
  (slot age-group)
  (slot smoking)
  (slot exposure)
  (slot breathing-issue)
  (slot chest-tightness)
  (slot family-history)
  (slot long-term-illness)
)
""")

env.build("""
(deftemplate risk-assessment
  (slot risk-level)
  (slot explanation)
)
""")

# Build Rules

# High risk 

# H1: smoker + breathing issue + chest tightness 
env.build("""
(defrule high-risk-1
  (declare (salience 40))
  (not (risk-assessment (risk-level ?l)))
  (patient (smoking yes)
           (breathing-issue yes)
           (chest-tightness yes))
=>
  (assert (risk-assessment
    (risk-level high)
    (explanation "High risk based on smoking and severe respiratory symptoms. Please seek immediate medical consultation.")))
)
""")

# H2: Exposure + long-term illness + breathing issue
env.build("""
(defrule high-risk-2
  (declare (salience 40))
  (not (risk-assessment (risk-level ?)))
  (patient (exposure yes)
           (long-term-illness yes)
           (breathing-issue yes))
=>
  (assert (risk-assessment
    (risk-level high)
    (explanation "High risk with exposure plus chronic illness and breathing issues. Specialist consultation is recommended.")))
)
""")

# H3: Older + both symptoms (even if risks unknown)
env.build("""
(defrule high-risk-3
  (declare (salience 39))
  (not (risk-assessment (risk-level ?)))
  (patient (age-group old)
           (breathing-issue yes)
           (chest-tightness yes))
=>
  (assert (risk-assessment
    (risk-level high)
    (explanation "High risk based on older age with significant respiratory symptoms. Urgent medical evaluation is advised.")))
)
""")

# H4: Severe symptoms + at least TWO major risk factors
env.build("""
(defrule high-risk-4
  (declare (salience 38))
  (not (risk-assessment (risk-level ?)))
  (patient (breathing-issue yes)
           (chest-tightness yes)
           (smoking ?s)
           (exposure ?e)
           (family-history ?f)
           (long-term-illness ?ill))
  (test (>= (+ (if (eq ?s yes) then 1 else 0)
               (if (eq ?e yes) then 1 else 0)
               (if (eq ?f yes) then 1 else 0)
               (if (eq ?ill yes) then 1 else 0)) 2))
=>
  (assert (risk-assessment
    (risk-level high)
    (explanation "High risk: severe symptoms with multiple risk factors. Seek medical assessment as soon as possible.")))
)
""")

# Medium Risk

# M1: respiratory symptoms but non-smoker
env.build("""
(defrule medium-risk-1
  (declare (salience 30))
  (not (risk-assessment (risk-level ?)))
  (patient (breathing-issue ?b)
           (chest-tightness ?c))
  (test (or (eq ?b yes) (eq ?c yes)))
=>
  (assert (risk-assessment
    (risk-level medium)
    (explanation "Moderate risk due to respiratory symptoms even without smoking history. You should consult a healthcare professional.")))
)
""")

# M2: smoker only
env.build("""
(defrule medium-risk-2
  (declare (salience 26))
  (not (risk-assessment (risk-level ?)))
  (patient (smoking yes)
           (breathing-issue no)
           (chest-tightness no)
           (exposure no)
           (family-history no)
           (long-term-illness no))
=>
  (assert (risk-assessment
    (risk-level medium)
    (explanation "Moderate risk: smoking increases long-term lung disease risk even without symptoms. Quitting and periodic check-ups are advised.")))
)
""")

# M3: family history + some exposure, but no strong current symptoms
env.build("""
(defrule medium-risk-3
  (declare (salience 25))
  (not (risk-assessment (risk-level ?l)))
  (patient (family-history yes)
           (exposure yes)
           (breathing-issue no)
           (chest-tightness no))
=>
  (assert (risk-assessment
    (risk-level medium)
    (explanation "Moderate risk because of family history and environmental exposure. Consider screening and monitoring of symptoms.")))
)
""")

# M4: No symptoms, but TWO or more risk factors
env.build("""
(defrule medium-risk-4
  (declare (salience 28))
  (not (risk-assessment (risk-level ?)))
  (patient (breathing-issue no)
           (chest-tightness no)
           (smoking ?s)
           (exposure ?e)
           (family-history ?f)
           (long-term-illness ?ill))
  (test (>= (+ (if (eq ?s yes) then 1 else 0)
               (if (eq ?e yes) then 1 else 0)
               (if (eq ?f yes) then 1 else 0)
               (if (eq ?ill yes) then 1 else 0)) 2))
=>
  (assert (risk-assessment
    (risk-level medium)
    (explanation "Moderate risk: multiple risk factors even without symptoms. Consider screening and lifestyle risk reduction.")))
)
""")

# M5: chest tightness alone with at least one risk factor
env.build("""
(defrule medium-risk-5
  (declare (salience 22))
  (not (risk-assessment (risk-level ?l)))
  (patient (breathing-issue no)
           (chest-tightness yes)
           (smoking ?s)
           (exposure ?e)
           (family-history ?f)
           (long-term-illness ?ill))
  (test (or (eq ?s yes)
            (eq ?e yes)
            (eq ?f yes)
            (eq ?ill yes)))
=>
  (assert (risk-assessment
    (risk-level medium)
    (explanation "Moderate risk due to chest discomfort combined with at least one risk factor. A check-up is recommended.")))
)
""")

# M6: Older + at least one risk factor (even without symptoms)
env.build("""
(defrule medium-risk-6
  (declare (salience 27))
  (not (risk-assessment (risk-level ?)))
  (patient (age-group old)
           (breathing-issue no)
           (chest-tightness no)
           (smoking ?s)
           (exposure ?e)
           (family-history ?f)
           (long-term-illness ?ill))
  (test (>= (+ (if (eq ?s yes) then 1 else 0)
               (if (eq ?e yes) then 1 else 0)
               (if (eq ?f yes) then 1 else 0)
               (if (eq ?ill yes) then 1 else 0)) 1))
=>
  (assert (risk-assessment
    (risk-level medium)
    (explanation "Moderate risk: older age with at least one risk factor. Regular monitoring and screening are recommended.")))
)
""")

# Low Risk

# L1: no smoking, no major symptoms, no family history
env.build("""
(defrule low-risk-1
  (declare (salience 15))
  (not (risk-assessment (risk-level ?l)))
  (patient (smoking no)
           (exposure no)
           (long-term-illness no)
           (breathing-issue no)
           (chest-tightness no)
           (family-history no))
=>
  (assert (risk-assessment
    (risk-level low)
    (explanation "Low risk as no symptoms and no major risk factors reported. Maintain a healthy lifestyle and routine check-ups.")))
)
""")

# L2: young non-smoker, no exposure, no long-term illness
env.build("""
(defrule low-risk-2
  (declare (salience 15))
  (not (risk-assessment (risk-level ?l)))
  (patient (age-group young)
           (smoking no)
           (exposure no)
           (breathing-issue no)
           (chest-tightness no)
           (long-term-illness no))
=>
  (assert (risk-assessment
    (risk-level low)
    (explanation "Low current risk. Continue avoiding smoking and high pollution exposure to keep your lungs healthy.")))
)
""")

# L3: middle age non-smoker, no exposure, no family history, no long-term illness, no symptoms
env.build("""
(defrule low-risk-3
  (declare (salience 15))
  (not (risk-assessment (risk-level ?l)))
  (patient (age-group middle)
           (smoking no)
           (exposure no)
           (family-history no)
           (long-term-illness no)
           (breathing-issue no)
           (chest-tightness no))
=>
  (assert (risk-assessment
    (risk-level low)
    (explanation "Low risk profile. Maintaining current habits and periodic health checks is recommended.")))
)
""")

# L4: mild single risk factor without symptoms (family history only)
env.build("""
(defrule low-risk-4
  (declare (salience 12))
  (not (risk-assessment (risk-level ?l)))
  (patient (smoking no)
           (exposure no)
           (breathing-issue no)
           (chest-tightness no)
           (long-term-illness no)
           (family-history yes))
=>
  (assert (risk-assessment
    (risk-level low)
    (explanation "Currently low symptom burden but with family history. Staying alert for new symptoms and regular screening is advised.")))
)
""")

# L4: single weak factor
env.build("""
(defrule low-risk-5
  (declare (salience 14))
  (not (risk-assessment (risk-level ?l)))
  (patient (breathing-issue no)
           (chest-tightness no)
           (smoking ?s)
           (exposure ?e)
           (family-history ?f)
           (long-term-illness ?ill))
  (test (<= (+ (if (eq ?s yes) then 1 else 0)
               (if (eq ?e yes) then 1 else 0)
               (if (eq ?f yes) then 1 else 0)
               (if (eq ?ill yes) then 1 else 0)) 1))
=>
  (assert (risk-assessment
    (risk-level low)
    (explanation "Low overall risk with at most one minor risk factor and no symptoms.")))
)
""")

# Default rule: if no specific rule fired
env.build("""
(defrule default-risk
  (declare (salience 0))
  (not (risk-assessment (risk-level ?level)))
  (patient)
=>
  (assert (risk-assessment
    (risk-level medium)
    (explanation "Insufficient pattern detected. Defaulting to MEDIUM risk as a precaution. Please consult a healthcare professional.")))
)
""")


def infer_risk(user_inputs):

    env.reset()

    fact_str = f"""(patient
      (age-group {user_inputs['age-group']})
      (smoking {user_inputs['smoking']})
      (exposure {user_inputs['exposure']})
      (breathing-issue {user_inputs['breathing-issue']})
      (chest-tightness {user_inputs['chest-tightness']})
      (family-history {user_inputs['family-history']})
      (long-term-illness {user_inputs['long-term-illness']})
    )"""

    logging.info("Asserting fact: %s", fact_str.strip())
    env.assert_string(fact_str)
    env.run()

    risk_level = "unknown"
    explanation = "No result."

    for fact in env.facts():
        if fact.template.name == "risk-assessment":
            risk_level = fact["risk-level"]
            explanation = fact["explanation"]
            break

    logging.info("Inference result: %s - %s", risk_level, explanation)
    return risk_level, explanation

# Save the current environment to a .clp file 
env.save("rules.clp")
