from .models import InterviewRoundRatingSheet, RatingAspect


def create_interview_sheet_from_template(interview_round, template):
    sheet = InterviewRoundRatingSheet.objects.create(
        name=f"Sheet for {interview_round}",
        round_name=interview_round,
        template=template,
    )
    for aspect_template in template.aspects.all():
        RatingAspect.objects.create(
            name=aspect_template.name,
            comment="",
            points=0,
            expected_points=aspect_template.expected_points,
            interview_rating_sheet=sheet,
            template=aspect_template,
        )
    return sheet
