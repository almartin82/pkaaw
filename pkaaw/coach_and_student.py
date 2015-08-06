"""Coach and Student classes"""

import requests
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

    def get_coach_details(self):
        r = self.make_request(pkaaw.constants.USER_URL)

        return r.json()

    def get_students(self):
        """Returns list of the coach's students' user ids"""
        r = self.make_request(pkaaw.constants.STUDENTS_URL)

        if r.status_code == requests.codes.ok:
            return [student['user_id'] for student in r.json()]
        else:
            print(r.reason)


class Student(object):

    def __init__(self, StoredAuth, user_id):
        if not hasattr(StoredAuth, 'oauth'):
            raise pkaaw.errors.ActiveSessionRequired

        self.oauth = StoredAuth.oauth
        self.make_request = StoredAuth.make_request
        self.id = user_id
        self.user_link = urllib.urlencode({'userId': self.id})

    def get_details(self):
        stu_url = '%s?%s' % (pkaaw.constants.USER_URL, self.user_link)
        r = self.make_request(stu_url)
        inner_dict = {}
        # if response is valid, build a dict of key fields
        if r.status_code == requests.codes.ok:
            resp_dict = r.json()
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
                if x.endswith("@teamstudents.org")
            ]

            inner_dict['identity_email'] = ', '.join(map(str, identity_email))

        return inner_dict

    def get_student_badges(self):
        """Gets earned status and count for every student/badge."""
        stu_badge_url = '%s?%s' % (pkaaw.constants.BADGES_URL, self.user_link)
        r = self.make_request(stu_badge_url)
        if r.status_code == requests.codes.ok:
            # returns a list of badges
            badge_list = r.json()
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

        return stu_list

    def get_composite_exercises(self):
        """Gets exercise status for every student/exercise."""
        stu_exercise_url = '%s?%s' % (pkaaw.constants.EXERCISES_URL,
                                      self.user_link)
        r = self.make_request(stu_exercise_url)
        stu_list = []
        if r.status_code == requests.codes.ok:
            resp = r.json()
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

            stu_list = [
                stu_dict
                for stu_dict in stu_list
                if stu_dict['exercise'] in self.exers
            ]

        return stu_list

    def get_exercise_states(self):
        """Gets exercise state changes for every student/exercise"""
        stu_states_url = '%s?%s' % (pkaaw.constants.EXERCISE_STATES_URL,
                                    self.user_link)
        r = self.make_request(stu_states_url)
        stu_list = []
        if r.status_code == requests.codes.ok:
            resp = r.json()
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

            stu_list = [
                item_dict
                for item_dict in stu_list
                if item_dict['exercise'] in self.exers
            ]

        return stu_list
