from accounts.models import DoctorProfile, StaffProfile, PatientProfile


class UserProfileFactory:
    """Factory Method Pattern for creating user profiles."""

    @staticmethod
    def create_profile(user, profile_data):
        """Create appropriate profile based on user role."""
        profile_creators = {
            'Doctor': lambda: DoctorProfile.objects.create(
                user=user,
                specialization=profile_data.get('specialization'),
                department=profile_data.get('department')
            ),
            'Staff': lambda: StaffProfile.objects.create(
                user=user,
                position=profile_data.get('position')
            ),
            'Patient': lambda: PatientProfile.objects.create(
                user=user,
                full_name=profile_data.get('full_name'),
                date_of_birth=profile_data.get('date_of_birth'),
                gender=profile_data.get('gender'),
                email=profile_data.get('email'),
                phone=profile_data.get('phone'),
                medical_history_summary=profile_data.get('medical_history_summary', '')
            ),
        }

        creator = profile_creators.get(user.role)
        return creator() if creator else None


user_profile_factory = UserProfileFactory()