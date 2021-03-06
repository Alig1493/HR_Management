class Config:

    HR = 1
    MANAGER = 2
    REGULAR = 3

    CHOICES = (
        (HR, "HR"),
        (MANAGER, "MANAGER"),
        (REGULAR, "REGULAR"),
    )

    DOMAINS = ["misfit.tech"]


class Status:

    OPEN = 1
    PROCESSED = 2
    HR_REVIEWED = 3

    CHOICES = (
        (OPEN, "Open"),
        (PROCESSED, "Processed"),
        (HR_REVIEWED, "HR reviewed")
    )


class ReviewType:

    MANAGER_APPROVAL = 1
    HR_REVIEW = 2

    CHOICES = (
        (MANAGER_APPROVAL, "Manager Approval"),
        (HR_REVIEW, "HR Review")
    )
