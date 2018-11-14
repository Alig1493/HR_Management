from hr.users.permissions import IsHROrManagerPermitted


class HRManagerPermissionMixins:

    permission_classes = [IsHROrManagerPermitted]
