(deftemplate MAIN::patient
   (slot age-group)
   (slot smoking)
   (slot exposure)
   (slot breathing-issue)
   (slot chest-tightness)
   (slot family-history)
   (slot long-term-illness))

(deftemplate MAIN::risk-assessment
   (slot risk-level)
   (slot explanation))

(defrule MAIN::high-risk-1
   (declare (salience 40))
   (not (risk-assessment (risk-level ?l)))
   (patient (smoking yes) (breathing-issue yes) (chest-tightness yes))
   =>
   (assert (risk-assessment (risk-level high) (explanation "High risk based on smoking and severe respiratory symptoms. Please seek immediate medical consultation."))))

(defrule MAIN::high-risk-2
   (declare (salience 40))
   (not (risk-assessment (risk-level ?)))
   (patient (exposure yes) (long-term-illness yes) (breathing-issue yes))
   =>
   (assert (risk-assessment (risk-level high) (explanation "High risk with exposure plus chronic illness and breathing issues. Specialist consultation is recommended."))))

(defrule MAIN::high-risk-3
   (declare (salience 39))
   (not (risk-assessment (risk-level ?)))
   (patient (age-group old) (breathing-issue yes) (chest-tightness yes))
   =>
   (assert (risk-assessment (risk-level high) (explanation "High risk based on older age with significant respiratory symptoms. Urgent medical evaluation is advised."))))

(defrule MAIN::high-risk-4
   (declare (salience 38))
   (not (risk-assessment (risk-level ?)))
   (patient (breathing-issue yes) (chest-tightness yes) (smoking ?s) (exposure ?e) (family-history ?f) (long-term-illness ?ill))
   (test (>= (+ (if (eq ?s yes)
      then
      1
      else
      0) (if (eq ?e yes)
      then
      1
      else
      0) (if (eq ?f yes)
      then
      1
      else
      0) (if (eq ?ill yes)
      then
      1
      else
      0)) 2))
   =>
   (assert (risk-assessment (risk-level high) (explanation "High risk: severe symptoms with multiple risk factors. Seek medical assessment as soon as possible."))))

(defrule MAIN::medium-risk-1
   (declare (salience 30))
   (not (risk-assessment (risk-level ?)))
   (patient (breathing-issue ?b) (chest-tightness ?c))
   (test (or (eq ?b yes) (eq ?c yes)))
   =>
   (assert (risk-assessment (risk-level medium) (explanation "Moderate risk due to respiratory symptoms even without smoking history. You should consult a healthcare professional."))))

(defrule MAIN::medium-risk-2
   (declare (salience 26))
   (not (risk-assessment (risk-level ?)))
   (patient (smoking yes) (breathing-issue no) (chest-tightness no) (exposure no) (family-history no) (long-term-illness no))
   =>
   (assert (risk-assessment (risk-level medium) (explanation "Moderate risk: smoking increases long-term lung disease risk even without symptoms. Quitting and periodic check-ups are advised."))))

(defrule MAIN::medium-risk-3
   (declare (salience 25))
   (not (risk-assessment (risk-level ?l)))
   (patient (family-history yes) (exposure yes) (breathing-issue no) (chest-tightness no))
   =>
   (assert (risk-assessment (risk-level medium) (explanation "Moderate risk because of family history and environmental exposure. Consider screening and monitoring of symptoms."))))

(defrule MAIN::medium-risk-4
   (declare (salience 28))
   (not (risk-assessment (risk-level ?)))
   (patient (breathing-issue no) (chest-tightness no) (smoking ?s) (exposure ?e) (family-history ?f) (long-term-illness ?ill))
   (test (>= (+ (if (eq ?s yes)
      then
      1
      else
      0) (if (eq ?e yes)
      then
      1
      else
      0) (if (eq ?f yes)
      then
      1
      else
      0) (if (eq ?ill yes)
      then
      1
      else
      0)) 2))
   =>
   (assert (risk-assessment (risk-level medium) (explanation "Moderate risk: multiple risk factors even without symptoms. Consider screening and lifestyle risk reduction."))))

(defrule MAIN::medium-risk-5
   (declare (salience 22))
   (not (risk-assessment (risk-level ?l)))
   (patient (breathing-issue no) (chest-tightness yes) (smoking ?s) (exposure ?e) (family-history ?f) (long-term-illness ?ill))
   (test (or (eq ?s yes) (eq ?e yes) (eq ?f yes) (eq ?ill yes)))
   =>
   (assert (risk-assessment (risk-level medium) (explanation "Moderate risk due to chest discomfort combined with at least one risk factor. A check-up is recommended."))))

(defrule MAIN::medium-risk-6
   (declare (salience 27))
   (not (risk-assessment (risk-level ?)))
   (patient (age-group old) (breathing-issue no) (chest-tightness no) (smoking ?s) (exposure ?e) (family-history ?f) (long-term-illness ?ill))
   (test (>= (+ (if (eq ?s yes)
      then
      1
      else
      0) (if (eq ?e yes)
      then
      1
      else
      0) (if (eq ?f yes)
      then
      1
      else
      0) (if (eq ?ill yes)
      then
      1
      else
      0)) 1))
   =>
   (assert (risk-assessment (risk-level medium) (explanation "Moderate risk: older age with at least one risk factor. Regular monitoring and screening are recommended."))))

(defrule MAIN::low-risk-1
   (declare (salience 15))
   (not (risk-assessment (risk-level ?l)))
   (patient (smoking no) (exposure no) (long-term-illness no) (breathing-issue no) (chest-tightness no) (family-history no))
   =>
   (assert (risk-assessment (risk-level low) (explanation "Low risk as no symptoms and no major risk factors reported. Maintain a healthy lifestyle and routine check-ups."))))

(defrule MAIN::low-risk-2
   (declare (salience 15))
   (not (risk-assessment (risk-level ?l)))
   (patient (age-group young) (smoking no) (exposure no) (breathing-issue no) (chest-tightness no) (long-term-illness no))
   =>
   (assert (risk-assessment (risk-level low) (explanation "Low current risk. Continue avoiding smoking and high pollution exposure to keep your lungs healthy."))))

(defrule MAIN::low-risk-3
   (declare (salience 15))
   (not (risk-assessment (risk-level ?l)))
   (patient (age-group middle) (smoking no) (exposure no) (family-history no) (long-term-illness no) (breathing-issue no) (chest-tightness no))
   =>
   (assert (risk-assessment (risk-level low) (explanation "Low risk profile. Maintaining current habits and periodic health checks is recommended."))))

(defrule MAIN::low-risk-4
   (declare (salience 12))
   (not (risk-assessment (risk-level ?l)))
   (patient (smoking no) (exposure no) (breathing-issue no) (chest-tightness no) (long-term-illness no) (family-history yes))
   =>
   (assert (risk-assessment (risk-level low) (explanation "Currently low symptom burden but with family history. Staying alert for new symptoms and regular screening is advised."))))

(defrule MAIN::low-risk-5
   (declare (salience 14))
   (not (risk-assessment (risk-level ?l)))
   (patient (breathing-issue no) (chest-tightness no) (smoking ?s) (exposure ?e) (family-history ?f) (long-term-illness ?ill))
   (test (<= (+ (if (eq ?s yes)
      then
      1
      else
      0) (if (eq ?e yes)
      then
      1
      else
      0) (if (eq ?f yes)
      then
      1
      else
      0) (if (eq ?ill yes)
      then
      1
      else
      0)) 1))
   =>
   (assert (risk-assessment (risk-level low) (explanation "Low overall risk with at most one minor risk factor and no symptoms."))))

(defrule MAIN::default-risk
   (declare (salience 0))
   (not (risk-assessment (risk-level ?level)))
   (patient)
   =>
   (assert (risk-assessment (risk-level medium) (explanation "Insufficient pattern detected. Defaulting to MEDIUM risk as a precaution. Please consult a healthcare professional."))))

