from projects.models import Report


def project_is_reported(projects):
    user_id=1
    for project in projects:
        is_reported = Report.objects.filter(project_id=project.id,user_id=user_id).count() != 0
        project.is_reported = is_reported
        # print(is_reported)
    return projects