# -------------------------
# RISK CALCULATIONS
# -------------------------

def calculate_risk(
    severity,
    probability
):

    return severity * probability


# -------------------------
# RISK CLASSIFICATION
# -------------------------

def classify_risk(
    risk_score
):

    if risk_score <= 5:
        return "Low"

    elif risk_score <= 10:
        return "Medium"

    elif risk_score <= 15:
        return "High"

    else:
        return "Critical"