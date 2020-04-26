from projects.models import Report,Project


def project_is_reported(projects):
    user_id=1
    for project in projects:
        is_reported = Report.objects.filter(project_id=project.id,user_id=user_id).count() != 0
        project.is_reported = is_reported
        # print(is_reported)
    return projects


def comment_is_reported(comments):
    user_id=1
    for comment in comments:
        is_reported = Report.objects.filter(comment_id=comment.id,project_id=comment.project.id,user_id=user_id).count() != 0
        comment.is_reported = is_reported
        # print(is_reported)
    return comments

def project_share_tag(tags):
    user_id=1
    projects=Project.objects.all()
    for project in projects:
        shares_tag = Report.objects.filter(project_id=project.id,tag=user_id).count() != 0
        project.is_reported = is_reported
        # print(is_reported)
    return projects