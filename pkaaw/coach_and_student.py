"""Coach and Student classes"""
from __future__ import print_function, unicode_literals
import urllib
import pkaaw.constants
import pkaaw.errors


class Coach(object):

    def __init__(self, StoredAuth):
        if not hasattr(StoredAuth, 'oauth'):
            raise pkaaw.errors.ActiveSessionRequired

        self.oauth = StoredAuth.oauth
        self.get_oauth = StoredAuth.get_oauth
        self.make_request = StoredAuth.make_request

    def get_students_raw(self):
        r = self.make_request(pkaaw.constants.STUDENTS_URL)
        return r

    def get_students(self):
        """Returns list of the coach's students' user ids"""
        resp = self.get_students_raw()

        return [student['user_id'] for student in resp]


class Student(object):

    def __init__(self, StoredAuth, user_id):
        if not hasattr(StoredAuth, 'oauth'):
            raise pkaaw.errors.ActiveSessionRequired

        self.oauth = StoredAuth.oauth
        self.make_request = StoredAuth.make_request
        self.id = user_id
        self.user_link = urllib.urlencode({'userId': self.id})

    def get_details_raw(self):
        stu_url = '%s?%s' % (pkaaw.constants.USER_URL, self.user_link)
        r = self.make_request(stu_url)
        return r

    def get_details(self, email_domain):
        resp_dict = self.get_details_raw()
        # convert keys to string from unicode
        resp_dict = dict([(str(k), v) for k, v in resp_dict.items()])
        # build an inner dict with desired fields
        inner_dict = {
            # collapse json to string
            'student': self.id,
            'all_proficient_exercises': ', '.join(map(
                str, resp_dict['all_proficient_exercises'])
            ),
            'badge_lev0': resp_dict['badge_counts'][u'0'],
            'badge_lev1': resp_dict['badge_counts'][u'1'],
            'badge_lev2': resp_dict['badge_counts'][u'2'],
            'badge_lev3': resp_dict['badge_counts'][u'3'],
            'badge_lev4': resp_dict['badge_counts'][u'4'],
            'badge_lev5': resp_dict['badge_counts'][u'5'],
            'coaches': ', '.join(map(str, resp_dict['coaches'])),
            'first_visit': str(resp_dict['first_visit']),
            'joined': str(resp_dict['joined']),
            'registration_date': str(resp_dict['registration_date']),
            'nickname': resp_dict['nickname'].encode('ascii', 'ignore'),
            'points': resp_dict['points'],
            'proficient_exercises': ', '.join(map(
                str, resp_dict['proficient_exercises'])
            ),
            'profile_root': str(resp_dict['profile_root']),
            'total_seconds_watched': resp_dict['total_seconds_watched'],
            'username': resp_dict['username'].encode('ascii', 'ignore'),
        }
        identity_email = [
            str(x)
            for x in resp_dict['auth_emails']
            if x.endswith(email_domain)
        ]

        # inner_dict['identity_email'] = ', '.join(map(str, identity_email))
        inner_dict['identity_email'] = identity_email[0].split(':')[1]

        return inner_dict

    def get_student_badges_raw(self):
        stu_badge_url = '%s?%s' % (pkaaw.constants.BADGES_URL, self.user_link)
        r = self.make_request(stu_badge_url)
        return r

    def get_student_badges(self):
        """Gets earned status and count for every student/badge."""
        badge_list = self.get_student_badges_raw()
        stu_list = []
        stu_list_detail = []
        for badge in badge_list:
            # make a dict of each badge
            dict([(str(k), v) for k, v in badge.items()])
            int_dict = {
                'student': self.id,
                'slug': str(badge['slug']),
                'owned': badge['is_owned'],
                'count': 0
            }
            # API only returns user badges if badge is owned
            if badge['is_owned']:
                try:
                    int_dict['count'] = len(badge['user_badges'])
                    # iterate over user badges and store date & context
                    # (badges can be earned multiple times)
                    for detail in badge['user_badges']:
                        dict([(str(k), v) for k, v in detail.items()])
                        int_detail_dict = {
                            'student': self.id,
                            'slug': str(badge['slug']),
                            'date_earned': detail['date'],
                            'context': str(detail['target_context_name'])
                        }
                        stu_list_detail.append(int_detail_dict)
                except Exception:
                    int_dict['count'] = 1
                # append to student dict
                stu_list.append(int_dict)

        return stu_list, stu_list_detail

    def get_composite_exercises_raw(self):
        stu_exercise_url = '%s?%s' % (pkaaw.constants.USER_EXERCISES_URL,
                                      self.user_link)
        r = self.make_request(stu_exercise_url)
        return r

    def get_composite_exercises(self):
        """Gets exercise status for every student/exercise."""
        resp = self.get_composite_exercises_raw()
        stu_list = []
        for ex in resp:
            ex_dict = dict([(str(k), v) for k, v in ex.items()])
            int_dict = {
                'student': self.id,
                'exercise': str(ex_dict['exercise']),
                'maximum_exercise_progress_dt': ex_dict[
                    'maximum_exercise_progress_dt'
                ],
                'streak': ex_dict['streak'],
                'progress': ex_dict['exercise_progress']['level'],
                'practiced_date': ex_dict['practiced_date'],
                'proficient_date': ex_dict['proficient_date'],
                'total_done': ex_dict['total_done'],
                'struggling': ex_dict['exercise_states']['struggling'],
                'proficient': ex_dict['exercise_states']['proficient'],
                'practiced': ex_dict['exercise_states']['practiced'],
                'mastered': ex_dict['exercise_states']['mastered'],
                'level': str(
                    ex_dict['maximum_exercise_progress']['level']
                ),
                'total_correct': ex_dict['total_correct'],
                'last_done': ex_dict['last_done'],
                'longest_streak': ex_dict['longest_streak']
            }
            stu_list.append(int_dict)

        return stu_list

    def get_exercise_states_raw(self):
        stu_states_url = '%s?%s' % (pkaaw.constants.EXERCISE_STATES_URL,
                                    self.user_link)
        r = self.make_request(stu_states_url)
        return r

    def get_exercise_states(self):
        """Gets exercise state changes for every student/exercise"""
        resp = self.get_exercise_states_raw()
        stu_list = []
        for ex_st in resp:
            change_dict = dict([(str(k), v) for k, v in ex_st.items()])
            int_dict = {
                'student': self.id,
                'exercise': str(change_dict['exercise_name']),
                'date': change_dict['date'],
                'change_type': None,
                'exercise_status': change_dict['to_progress']['level'],
                'mastery_flag': change_dict['to_progress']['mastered']
            }
            stu_list.append(int_dict)

        return stu_list
