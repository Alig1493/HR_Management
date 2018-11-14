from hr.users.config import ReviewType


class LogMixins:

    def _get_user(self):
        return self.context["request"].user

    def _get_review_type(self, instance, validated_data):
        if validated_data.get("status"):
            return ReviewType.HR_REVIEW
        return ReviewType.MANAGER_APPROVAL

    def _get_review_change(self, review_type, instance, validated_data):
        if review_type == ReviewType.HR_REVIEW:
            return instance.status, validated_data["status"]
        return instance.manager_approved, validated_data["manager_approved"]
