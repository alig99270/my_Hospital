from accounts.models import DoctorProfile, StaffProfile, PatientProfile

class UserProfileFactory:
    """Factory Method Pattern for creating user profiles"""
    @staticmethod
    def create_profile(user, profile_data):
        if user.role == 'Doctor':
            return DoctorProfile.objects.create(
                user=user,
                specialization=profile_data.get('specialization'),
                department=profile_data.get('department')
            )
        elif user.role == 'Staff':
            return StaffProfile.objects.create(
                user=user,
                position=profile_data.get('position')
            )
        elif user.role == 'Patient':
            return PatientProfile.objects.create(
                user=user,
                full_name=profile_data.get('full_name'),
                date_of_birth=profile_data.get('date_of_birth'),
                gender=profile_data.get('gender'),
                email=profile_data.get('email'),
                phone=profile_data.get('phone'),
                medical_history_summary=profile_data.get('medical_history_summary')
            )
        return None

user_profile_factory = UserProfileFactory()