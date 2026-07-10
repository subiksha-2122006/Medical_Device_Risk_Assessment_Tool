def calculate_rpn(
    severity,
    occurrence,
    detection
):

    return (
        severity *
        occurrence *
        detection
    )


def classify_rpn(rpn):

    if rpn >= 150:
        return "Critical"

    elif rpn >= 80:
        return "High"

    elif rpn >= 40:
        return "Medium"

    else:
        return "Low"