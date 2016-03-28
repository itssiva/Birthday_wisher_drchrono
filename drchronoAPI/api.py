import requests
import urllib


def get_user_details(access_token):
    """
    Get the details of the user, the first time, after login with drchrono
    Create a Greeting object for the user, also check if a staff's doctor already subscibed.
    """
    response = requests.get('https://drchrono.com/api/users/current',
                            headers={'Authorization': 'Bearer %s' % access_token})
    return response


def get_patients_of_doctor(doctor_id, access_token, filters={}):
    """
    input: User, filter parameters
    output : patients list for that doctor
    """
    patients = []
    filters['doctor'] = doctor_id
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    patients_url = 'https://drchrono.com/api/patients?'
    patients_url += urllib.urlencode(filters)
    while patients_url:
        data = requests.get(patients_url, headers=headers).json()
        patients.extend(data['results'])
        patients_url = data['next']
    return patients


def get_doctor_details(doctor_id, access_token):
    """
    Given the User of a doctor, returns the details of the doctor
    """
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    doctor_url = 'https://drchrono.com/api/doctors/{}'.format(doctor_id)
    data = requests.get(doctor_url, headers=headers).json()
    filtered_data = {
         'website': data['website'],
         'first_name': data['first_name'],
         'last_name': data['last_name'],
         'suffix': data['suffix'],
         'specialty': data['specialty'],
         'email': data['email'],
         'office_phone': data['office_phone'],
         'home_phone': data['home_phone'],
         'cell_phone': data['cell_phone'],
         'id': data['id'],
         'job_title': data['job_title']
    }
    return filtered_data
